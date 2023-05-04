#Import the model you want to train
#from paddle_defens import Paddle
#from paddle_vs_paddle import Paddle
from paddle_Ai_vs_Ai import Paddle

import numpy as np
import matplotlib.pyplot as plt
import pickle
from tensorflow import keras


env = Paddle()
np.random.seed(0)




# Use the model you want to see in action
model1 = keras.models.load_model('model_Ai1')
model2 = keras.models.load_model('model_Ai2')

def act1(state):
        
        act_values = model1.predict(state, verbose = 0)
        return np.argmax(act_values[0])

def act2(state):
        
        act_values = model2.predict(state, verbose = 0)
        return np.argmax(act_values[0])


def Play_Ai(episode):

    loss = []
    nb_hit1 = []
    nb_hit2 = []

    action_space = 3
    state_space = 5
    max_steps = 9001
    max_hit = 301
    record1,record2 = 0,0
    hit = 0

    for e in range(episode):
        state1,state2 = env.reset()
        state1,state2 = np.reshape(state1, (1, state_space)),np.reshape(state2, (1, state_space))
        score = 0
        itera = 0
        while itera < max_steps and hit < max_hit:
            action1 = act1(state1)
            action2 = act2(state2)
            reward1,reward2, next_state1,next_state2, done1,done2,hit1,hit2,total_hit1,total_hit2 = env.step(action1,action2)
            score += reward1 + reward2
            next_state1 = np.reshape(next_state1, (1, state_space))
            next_state2 = np.reshape(next_state2, (1, state_space))
            state1 = next_state1
            state2 = next_state2
            if done1 or done2:
                print("episode: {}/{}, score: {}".format(e, episode, score))
                break
            itera += 1
        
        loss.append(score)
        nb_hit1.append(total_hit1)
        nb_hit2.append(total_hit2)
            

    
    return loss,nb_hit1,nb_hit2


if __name__ == '__main__':

    ep = 207 #number of games played for training
    loss,nb_hit1,nb_hit2 = Play_Ai(ep)
    
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