# This file contains the options that you should modify to solve Question 2

# IMPORTANT NOTE:
# Comment your code explaining why you chose the values you chose.
# Uncommented code will be penalized.

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    '''
    we want the policy to seek the near terminal state (reward +1) via the short
    dangerous path (moving besides the row of -10 state).
    
    Comment: 
    - The noise is 0 to make sure the agent will always move to the direction that it wants to go to 
    - the discount factor to make it care about the nearest values so i set it to 0.2 which is close  more to 0
    - i chose -0.2 to the living reward to make the agent take the shortest path to +10 with willing to take risk and 
        move beside -10 if it is the shortest path to +10
    '''
    return {
        "noise": 0,
        "discount_factor": 0.2,
        "living_reward":-0.2
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    '''
    we want the policy to seek the near terminal state (reward +1) via the long safe path
    (moving away from the row of -10 state).
    
    Comment:
    - the noise is 0.1 to make it move to the direction that it wants to go to but with a little chance to move to another direction
        as we want it to go to nearest terminal with safe path so it may go to another terminal 
    - the discount factor is 0.1 to make it care about the closest cells around it with smaller ratio to be more greedy 
    to make sure it chooses +1 reward
    - the living reward is -0.1 to make it avoid the -10 cells and choose the safe path to +1
    '''
    return {
        "noise": 0.1,
        "discount_factor": 0.1,
        "living_reward": -0.1
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    ''''
    we want the policy to seek the far terminal state (reward +10) via the short
    dangerous path (moving besides the row of -10 state).
    
    Comment:
    - the noise is 0 to make it move to the direction that it wants to go to
    - the discount factor is 0.9 to make it care about the total reward for future states so it may consider the +10 reward
    because it is high compared to other rewards and will make the utility higher
    - the living reward is -1 to make choose the shortest path to the +10 with the risk of moving besides the -10 reward
    '''
    return {
        
        "noise": 0,
        "discount_factor": 0.9,
        "living_reward": -1
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
        return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.02
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 0.1,
        "living_reward": 100
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 0.1,
        "living_reward": -100
    }