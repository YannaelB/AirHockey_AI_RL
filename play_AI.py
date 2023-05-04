# Import the model with which you want to play

from paddle_defens import Paddle
#from paddle_attack import Paddle
#from paddle_obstacle import Paddle

import numpy as np
import matplotlib.pyplot as plt
import pickle
from tensorflow import keras



env = Paddle()


# Use the model you want to see in action
model = keras.models.load_model('model_defens_newmodel')


def act2(state):
        
        act_values = model.predict(state, verbose = 0)
        return np.argmax(act_values[0])

def play_AI(episode):

    loss = []
    nb_hit = []
    nb_goal = []

    action_space = 3
    state_space = 5
    max_steps = 9001
    max_hit = 301
    record = 0
    hit = 0

    for e in range(episode):
        state = env.reset()
        state = np.reshape(state, (1, state_space))
        score = 0
        itera = 0
        while itera < max_steps and hit < max_hit:
            action = act2(state)
            reward, next_state, done,hit,goal,total_hit = env.step(action)
            score += reward
            if goal > record: #or score_goal
                record = goal
                print("record = ",record)
            next_state = np.reshape(next_state, (1, state_space))
            state = next_state
            if done: 
                print("episode: {}/{}, score: {}".format(e, episode, score))
                break
            
            
            itera += 1
        loss.append(score)
        nb_hit.append(total_hit)
        nb_goal.append(goal)

                        
    return loss,nb_hit,nb_goal


if __name__ == '__main__':

    ep = 50
    loss,nb_hit,nb_goal = play_AI(ep)
    
    with open("model_file.pkl", "wb") as binary_file:
        pickle.dump(model,binary_file,pickle.HIGHEST_PROTOCOL)
    plt.plot([i for i in range(len(loss))], loss,label = "loss")
    plt.plot([i for i in range(len(nb_hit))], nb_hit,label = "hit")
    plt.plot([i for i in range(len(nb_goal))], nb_goal,label = "goal")
    plt.xlabel('episodes')
    plt.ylabel('reward')
    plt.legend()
    plt.show()