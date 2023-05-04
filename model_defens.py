#Import the model you want to train
from paddle_defens import Paddle
#from paddle_vs_paddle import Paddle

import random
import numpy as np
from keras import Sequential
from collections import deque
from keras.layers import Dense
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import pickle
import sys
from tensorflow import keras


env = Paddle()
np.random.seed(0)





class DQN:

    """ Implementation of deep q learning algorithm """

    def __init__(self, action_space, state_space):

        self.action_space = action_space
        self.state_space = state_space
        self.epsilon = 1
        self.gamma = .97
        self.batch_size = 64
        self.epsilon_min = .005
        self.epsilon_decay = .998
        self.learning_rate = 0.001
        self.memory = deque(maxlen=100000)

        # If you want to train from scratch, put False
        if False:
            self.model = keras.models.load_model('model_attack5')
        else:
            self.model = self.build_model()

        

    # model structure, classical NN
    def build_model(self):

        model = Sequential()
        model.add(Dense(16, input_shape=(self.state_space,), activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(self.action_space, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):

        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model.predict(state, verbose = 0)
        return np.argmax(act_values[0])

    def replay(self):

        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in  minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def train_dqn(episode):

    loss = []
    nb_hit = []

    action_space = 3
    state_space = 5
    max_steps = 9001
    max_hit = 301
    record = 0
    hit = 0

    agent = DQN(action_space, state_space)
    for e in range(episode):
        state = env.reset()
        state = np.reshape(state, (1, state_space))
        score = 0
        itera = 0
        while itera < max_steps and hit < max_hit:
            action = agent.act(state)
            reward, next_state, done,hit,total_hit = env.step(action)
            score += reward
            if hit > record : 
                record = hit
                agent.model.save('model_defens_newmodel')
                print("save + record = ", hit)
            next_state = np.reshape(next_state, (1, state_space))
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            agent.replay()
            if done:
                print("episode: {}/{}, score: {}".format(e, episode, score))
                break
            itera += 1
        if e%(int(episode/10)) == (int(episode/10)-1):
            agent.model.save('model_defens_newmodel')
            print("save + episode = ", e)

        loss.append(score)
        nb_hit.append(total_hit)
            

        # Quit game
        #if e > episode :
            #sys.exit()

    agent.model.save('model_defens_newmodel.1')

    
    return loss, agent,nb_hit


if __name__ == '__main__':

    ep = 207 #number of games played for training
    loss, model,nb_hit = train_dqn(ep)
    
    with open("model_file.pkl", "wb") as binary_file:
        pickle.dump(model,binary_file,pickle.HIGHEST_PROTOCOL)
    plt.plot([i for i in range(len(loss))], loss,label = "loss")
    plt.plot([i for i in range(len(nb_hit))], nb_hit,label = "hit")
    plt.xlabel('episodes')
    plt.ylabel('reward')
    plt.legend()
    plt.show()