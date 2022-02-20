import gym
import numpy as np

from Agent import *
from EnvManager import *

import matplotlib.pyplot as plt


def main():
    # env = EnvMananger()
    # print(env.getState()[:, :, 0])

    # env.step(1)

    # plt.imshow(env.getState()[:, :, 0], cmap="gray")
    # plt.show()

    # plt.imshow(env.getState()[:, :, 1], cmap="gray")
    # plt.show()
    # exit()
    # Logging
    file_path = "test_logs/test"
    train_summary_writer = tf.summary.create_file_writer(file_path)

    num_episods = 500
    update = 10

    # env = gym.make('LunarLander-v2')
    # agent = Agent(input_dims=env.observation_space.shape,
    #             num_actions=env.action_space.n, batch_size=64)

    env = EnvMananger()  # gym.make('LunarLander-v2')
    agent = Agent(input_dims=env.observation_space_shape,
                  num_actions=2, batch_size=64)

    agent.q_net.summary()

    with train_summary_writer.as_default():

        for episode in range(num_episods):

            done_flag = False

            score = 0  # sum of rewards
            rewards = []

            cnt_steps = 0
            state = env.reset()
            while not done_flag:
                action = agent.select_action(state)
                next_state, reward, done_flag = env.step(action)

                agent.store_experience(state, action, next_state, reward, done_flag)

                state = next_state
                agent.train_step()

                score += reward

                rewards.append(reward)
                cnt_steps += 1

            if episode % update == 0:
                agent.update_target()

            tf.summary.scalar(f"Average reward", np.mean(rewards), step=episode)
            tf.summary.scalar(f"Score", score, step=episode)
            tf.summary.scalar(f"Epsilon (EpsilonGreedyStrategy)", agent.strategy.get_exploration_rate(), step=episode)
            tf.summary.scalar(f"Steps per episode", cnt_steps, step=episode)

            print(f"Episode {episode} with score {round(score, 2)} and avg reward {round(np.mean(rewards), 2)}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received")
