#
#  Copyright © Sorbonne University.
#
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
#

import copy
import numpy as np
from typing import Callable, List

import hydra
import optuna
from omegaconf import DictConfig

# %%
import torch
import torch.nn as nn

# %%
import gymnasium as gym
from gymnasium import Env
from gymnasium.wrappers import AutoResetWrapper

# %%
from bbrl import get_arguments, get_class
from bbrl.agents import TemporalAgent, Agents
from bbrl.workspace import Workspace
from bbrl.agents.gymnasium import ParallelGymAgent

from bbrl_algos.models.exploration_agents import EGreedyActionSelector
from bbrl_algos.models.critics import DiscreteQAgent
from bbrl_algos.models.loggers import Logger
from bbrl_algos.models.utils import save_best
from bbrl_algos.models.envs import get_eval_env_agent_rich

from bbrl.visu.plot_critics import plot_discrete_q

from bbrl.utils.functional import gae
from bbrl.utils.chrono import Chrono

# HYDRA_FULL_ERROR = 1
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")


# %%
def compute_critic_loss(
    discount_factor, gae_factor, reward, must_bootstrap, q_values, 
):
    """Compute critic loss
    Args:
        discount_factor (float): The discount factor
        reward (torch.Tensor): a (2 × T × B) tensor containing the rewards
        must_bootstrap (torch.Tensor): a (2 × T × B) tensor containing 0 if the episode is completed at time $t$
        action (torch.LongTensor): a (2 × T) long tensor containing the chosen action
        q_values (torch.Tensor): a (2 × T × B × A) tensor containing Q values
        q_target (torch.Tensor, optional): a (2 × T × B × A) tensor containing target Q values

    Returns:
        torch.Scalar: The loss
    """
    v_values = q_values.max(axis=-1)[0]
    # print(reward.shape, must_bootstrap.shape, v_values.shape)
    advantage = gae(
        v_values,
        reward,
        must_bootstrap,
        discount_factor,
        gae_factor,
    )
    td_error = advantage**2
    critic_loss = td_error.mean()
    return critic_loss


# %%
def make_wrappers(
    autoreset: bool,
) -> List[Callable[[Env], Env]]:
    return [AutoResetWrapper] if autoreset else []


# %%
def make_env(
    identifier: str,
    autoreset: bool,
    **kwargs,
) -> Env:
    env: Env = gym.make(id=identifier, **kwargs)
    wrappers = make_wrappers(
        autoreset=autoreset,
    )
    for wrapper in wrappers:
        env = wrapper(env)
    return env


# %%
def build_mlp(sizes, activation, output_activation=nn.Identity()):
    layers = []
    for j in range(len(sizes) - 1):
        act = activation if j < len(sizes) - 2 else output_activation
        layers += [nn.Linear(sizes[j], sizes[j + 1]), act]
    return nn.Sequential(*layers)


# %%
def create_dqn_agent(cfg_algo, train_env_agent, eval_env_agent):
    # obs_space = train_env_agent.get_observation_space()
    # obs_shape = obs_space.shape if len(obs_space.shape) > 0 else obs_space.n

    # act_space = train_env_agent.get_action_space()
    # act_shape = act_space.shape if len(act_space.shape) > 0 else act_space.n

    state_dim, action_dim = train_env_agent.get_obs_and_actions_sizes()

    critic = DiscreteQAgent(
        state_dim=state_dim,
        hidden_layers=list(cfg_algo.architecture.hidden_sizes),
        action_dim=action_dim,
        seed=cfg_algo.seed.q,
    )

    explorer = EGreedyActionSelector(
        name="action_selector",
        epsilon=cfg_algo.explorer.epsilon_start,
        epsilon_end=cfg_algo.explorer.epsilon_end,
        epsilon_decay=cfg_algo.explorer.decay,
        seed=cfg_algo.seed.explorer,
    )
    q_agent = TemporalAgent(critic)

    tr_agent = Agents(train_env_agent, critic, explorer)
    ev_agent = Agents(eval_env_agent, critic)

    # Get an agent that is executed on a complete workspace
    train_agent = TemporalAgent(tr_agent)
    eval_agent = TemporalAgent(ev_agent)

    return train_agent, eval_agent, q_agent


# %%
# Configure the optimizer over the q agent
def setup_optimizer(optimizer_cfg, q_agent):
    optimizer_args = get_arguments(optimizer_cfg)
    parameters = q_agent.parameters()
    optimizer = get_class(optimizer_cfg)(parameters, **optimizer_args)
    return optimizer


# %%
def run_dqn(cfg, logger, trial=None):
    best_reward = float("-inf")

    # 1) Create the environment agent
    train_env_agent = ParallelGymAgent(
        make_env_fn=get_class(cfg.gym_env_train),
        num_envs=cfg.algorithm.n_envs_train,
        make_env_args=get_arguments(cfg.gym_env_train),
        seed=cfg.algorithm.seed.train,
    )
    eval_env_agent = get_eval_env_agent_rich(cfg)

    # 2) Create the DQN-like Agent
    train_agent, eval_agent, q_agent = create_dqn_agent(
        cfg.algorithm, train_env_agent, eval_env_agent
    )

    # 3) Create the training workspace
    train_workspace = Workspace()  # Used for training

    # 5) Configure the optimizer
    optimizer = setup_optimizer(cfg.optimizer, q_agent)

    # 6) Define the steps counters
    nb_steps = 0
    tmp_steps_target_update = 0
    tmp_steps_eval = 0

    while nb_steps < cfg.algorithm.n_steps:
        # Decay the explorer epsilon
        explorer = train_agent.agent.get_by_name("action_selector")
        assert len(explorer) == 1, "There should be only one explorer"
        explorer[0].decay()

        # Execute the agent in the workspace
        if nb_steps > 0:
            train_workspace.zero_grad()
            train_workspace.copy_n_last_steps(1)
            train_agent(
                train_workspace,
                t=1,
                n_steps=cfg.algorithm.n_steps_train - 1,
            )
        else:
            train_agent(
                train_workspace,
                t=0,
                n_steps=cfg.algorithm.n_steps_train,
            )

        transition_workspace: Workspace = train_workspace.get_transitions(
            filter_key="env/done"
        )

        # Only get the required number of steps
        steps_diff = cfg.algorithm.n_steps - nb_steps
        if transition_workspace.batch_size() > steps_diff:
            for key in transition_workspace.keys():
                transition_workspace.set_full(
                    key, transition_workspace[key][:, :steps_diff]
                )

        nb_steps += transition_workspace.batch_size()


        # The q agent needs to be executed on the rb_workspace workspace (gradients are removed in workspace).
        q_agent(transition_workspace, t=0, n_steps=2, choose_action=False)

        q_values, terminated, truncated, reward, action = transition_workspace[
                "critic/q_values",
                "env/terminated",
                "env/truncated",
                "env/reward",
                "action",
            ]

        # Determines whether values of the critic should be propagated
        # True if the episode reached a time limit or if the task was not terminated.
        must_bootstrap = torch.logical_or(~terminated, truncated)


        
        critic_loss = compute_critic_loss(
            cfg.algorithm.discount_factor,
            cfg.algorithm.gae_factor,
            reward,
            must_bootstrap,
            q_values,
        )

                # Store the loss
        logger.add_log("critic_loss", critic_loss, nb_steps)

        optimizer.zero_grad()
        critic_loss.backward()
        torch.nn.utils.clip_grad_norm_(
            q_agent.parameters(), cfg.algorithm.max_grad_norm)
                
        optimizer.step()

        # Evaluate the agent
        if nb_steps - tmp_steps_eval > cfg.algorithm.eval_interval:
            tmp_steps_eval = nb_steps
            eval_workspace = Workspace()  # Used for evaluation
            eval_agent(
                eval_workspace,
                t=0,
                stop_variable="env/done",
                choose_action=True,
            )
            rewards = eval_workspace["env/cumulated_reward"][-1]
            logger.log_reward_losses(rewards, nb_steps)
            mean = rewards.mean()

            if mean > best_reward:
                best_reward = mean

            # print(f"nb_steps: {nb_steps}, reward: {mean:.0f}, best: {best_reward:.0f}")

            if trial is not None:
                trial.report(mean, nb_steps)
                if trial.should_prune():
                    raise optuna.TrialPruned()

            if cfg.save_best and best_reward == mean:
                save_best(
                    eval_agent,
                    cfg.gym_env_eval.identifier,
                    best_reward,
                    "./dqn_best_agents/",
                    "dqn",
                )
                if cfg.plot_agents:
                    critic = eval_agent.agent.agents[1]
                    plot_discrete_q(
                        critic,
                        eval_env_agent,
                        best_reward,
                        "./dqn_plots/",
                        cfg.gym_env_eval.identifier,
                        input_action="policy",
                    )

    return best_reward


# %%
@hydra.main(
    config_path="configs/",
    config_name="continuous_maze.yaml",
    # config_name="cartpole.yaml",
)  # , version_base="1.3")
def main(cfg_raw: DictConfig):
    torch.random.manual_seed(seed=cfg_raw.algorithm.seed.torch)
    c = Chrono()

    logger = Logger(cfg_raw)
    n=2
    for gae in range(n-1):
        k=2
        scores = np.zeros(k)
        cfg_raw.algorithm.gae_factor = (gae + 1)/n
        for seed in range(k):
            cfg_raw.algorithm.seed.train = seed
            scores[seed] = run_dqn(cfg_raw, logger)
            # print("score", scores[seed])
        print(f"gae: {cfg_raw.algorithm.gae_factor}, mean score: {scores.mean()}, std: {scores.std()}")
    c.stop()

if __name__ == "__main__":
    main()
