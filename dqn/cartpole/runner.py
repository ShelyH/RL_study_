#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26 下午3:10
# @Site    : 
# @File    : runner.py
# @Software: PyCharm
import os
import gym
import numpy as np
import parl
from parl.utils import logger, ReplayMemory
from model import CartpoleModel
from agent import CartpoleAgent
from parl.algorithms import DQN

# learning frequency
LEARN_FREQ = 5
MEMORY_SIZE = 200000
MEMORY_WARMUP_SIZE = 200
BATCH_SIZE = 64
LEARNING_RATE = 0.0005
GAMMA = 0.99


# train an episode
def run_train_episode(agent, env, rpm):
    total_reward = 0
    obs = env.reset()
    step = 0
    while True:
        step += 1
        action = agent.sample(obs)
        next_obs, reward, done, _ = env.step(action)
        rpm.append(obs, action, reward, next_obs, done)

        # train model
        if (len(rpm) > MEMORY_WARMUP_SIZE) and (step % LEARN_FREQ == 0):
            (batch_obs, batch_action, batch_reward, batch_next_obs, batch_done) = rpm.sample_batch(BATCH_SIZE)
            train_loss = agent.learn(batch_obs, batch_action, batch_reward, batch_next_obs, batch_done)
        total_reward += reward
        obs = next_obs
        if done:
            break

    return total_reward


# evaluate 5 episodes
def run_evaluate_episodes(agent, env, eval_episodes=5, render=False):
    eval_reward = []
    for i in range(eval_episodes):
        obs = env.reset()
        episode_reward = 0
        while True:
            action = agent.predict(obs)
            obs, reward, done, _ = env.step(action)
            episode_reward += reward
            if render:
                env.render()
            if done:
                break

        eval_reward.append(episode_reward)
    return np.mean(eval_reward)


def main():
    env = gym.make('CartPole-v0')
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.n
    logger.info('obs_dim {},act_dim {}'.format(obs_dim, act_dim))

    rpm = ReplayMemory(MEMORY_SIZE, obs_dim, 0)

    model = CartpoleModel(obs_dim, act_dim)
    alg = DQN(model, gamma=GAMMA, lr=LEARNING_RATE)
    agent = CartpoleAgent(alg, act_dim, e_greed=0.1, e_greed_decrement=1e-6)

    # warmup memory
    while len(rpm) < MEMORY_WARMUP_SIZE:
        run_train_episode(agent, env, rpm)

    max_episode = 800

    # start training
    episode = 0
    while episode < max_episode:
        for i in range(50):
            total_reward = run_train_episode(agent, env, rpm)
            episode += 1

        eval_reward = run_evaluate_episodes(agent, env, render=False)
        logger.info('episode:{}    e_greed:{}   Test reward:{}'.format(episode, agent.e_greed, eval_reward))
    save_path = './model.ckpt'
    agent.save(save_path)


if __name__ == '__main__':
    main()
