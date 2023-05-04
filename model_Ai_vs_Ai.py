#Import the model you want to train :

from paddle_Ai_vs_Ai import Paddle

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
        self.epsilon_decay = .995
        self.learning_rate = 0.001
        self.memory1 = deque(maxlen=100000)
        self.memory2 = deque(maxlen=100000)

        # If you want to train from scratch, put False, otherwise put True
        if False:
            self.model = keras.models.load_model('model_attack5')
        else:
            self.model1 = self.build_model()
            self.model2 = self.build_model()

        

    # model structure, classical NN
    def build_model(self):

        model = Sequential()
        model.add(Dense(18, input_shape=(self.state_space,), activation='relu'))
        model.add(Dense(12, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(self.action_space, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember1(self, state, action, reward, next_state, done):
        self.memory1.append((state, action, reward, next_state, done))
    
    def remember2(self, state, action, reward, next_state, done):
        self.memory2.append((state, action, reward, next_state, done))

    #Predict and act for AI 1
    def act1(self, state):

        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model1.predict(state, verbose = 0)
        return np.argmax(act_values[0])

    #Predict and act for AI 2
    def act2(self, state):

        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model2.predict(state, verbose = 0)
        return np.argmax(act_values[0])

    def replay1(self):

        if len(self.memory1) < self.batch_size:
            return

        minibatch = random.sample(self.memory1, self.batch_size)
        states = np.array([i[0] for i in  minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.model1.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model1.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model1.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def replay2(self):

        if len(self.memory2) < self.batch_size:
            return

        minibatch = random.sample(self.memory2, self.batch_size)
        states = np.array([i[0] for i in  minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.model2.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model2.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model2.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def train_dqn(episode):

    loss = []
    nb_hit1 = []
    nb_hit2 = []

    action_space = 3
    state_space = 5
    max_steps = 9001
    max_hit = 301
    record1,record2 = 0,0
    hit = 0

    #We use a very elementary but easy solution to train an AI against an AI. We could have trained just one AI and then make it play against himself 
    #but i thought it could have been interesting to compare their speed learning
    agent1 = DQN(action_space, state_space) #create IA 1
    agent2 = DQN(action_space, state_space) # create IA 2
    for e in range(episode):
        state1,state2 = env.reset()
        state1,state2 = np.reshape(state1, (1, state_space)),np.reshape(state2, (1, state_space))
        score = 0
        itera = 0
        while itera < max_steps and hit < max_hit:
            action1 = agent1.act1(state1)
            action2 = agent2.act2(state2)
            reward1,reward2, next_state1,next_state2, done1,done2,hit1,hit2,total_hit1,total_hit2 = env.step(action1,action2)
            score += reward1 + reward2
            if hit1 > record1 and hit1 > 5 :
                record1 = hit1
                agent1.model1.save('model_Ai1.1')
                print("save1 + record1 = ", hit1)
            if hit2 > record2 and hit2 > 5: 
                record2 = hit2
                agent2.model2.save('model_Ai2.1')
                print("save2 + record2 = ", hit2)
            next_state1 = np.reshape(next_state1, (1, state_space))
            next_state2 = np.reshape(next_state2, (1, state_space))
            agent1.remember1(state1, action1, reward1, next_state1, done1)
            agent2.remember2(state2, action2, reward2, next_state2, done2)
            state1 = next_state1
            state2 = next_state2
            agent1.replay1()
            agent2.replay2()
            if done1 or done2:
                print("episode: {}/{}, score: {}".format(e, episode, score))
                break
            itera += 1
        if e%(int(episode/10)) == (int(episode/10)-1):
            agent1.model1.save('model_Ai1.1')
            agent2.model2.save('model_Ai2.1')
            print("save1&2 + episode = ", e)

        loss.append(score)
        nb_hit1.append(total_hit1)
        nb_hit2.append(total_hit2)
            


    agent1.model1.save('model_Ai1.1')
    agent2.model2.save('model_Ai2.1')

    
    return loss, agent1,agent2,nb_hit1,nb_hit2


if __name__ == '__main__':

    ep = 207 #number of games played for training
    loss, model1,model2,nb_hit1,nb_hit2 = train_dqn(ep)
    
    with open("model_file.pkl", "wb") as binary_file:
        pickle.dump(model1,binary_file,pickle.HIGHEST_PROTOCOL)
        pickle.dump(model2,binary_file,pickle.HIGHEST_PROTOCOL)
    plt.plot([i for i in range(len(loss))], loss,label = "loss")
    plt.plot([i for i in range(len(nb_hit1))], nb_hit1,label = "hit1")
    plt.plot([i for i in range(len(nb_hit2))], nb_hit2,label = "hit2")
    plt.xlabel('episodes')
    plt.ylabel('reward')
    plt.legend()
    plt.show()