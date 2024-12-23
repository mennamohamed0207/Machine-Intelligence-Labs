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
    - The noise is 0 to make the agent to the direction that it wants to go to 
    - the discount factor to make it care about the nearest values so i set it to 0.2 which is close  more to 0 so it is quite greedy to
        reach a reward
    - i chose -0.2 to the living reward to make the agent take the shortest path to +1 with willing to take risk and 
        move beside -10 if it is the shortest path to +1
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
        as we want it to go to nearest terminal with safe path so it may go to another terminal so i set it to 0.1 to give a chance to reach this terminal state either
    - the discount factor is 0.1 to make it care about the closest cells around it to be more greedy 
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
    - the living reward is -1 to make it choose the shortest path to the +10 with the risk of moving besides the -10 reward
    '''
    return {
        
        "noise": 0,
        "discount_factor": 0.9,
        "living_reward": -1
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
        '''
        we want the policy to seek the far terminal state (reward +10) via the long
        safe path (moving away from the row of -10 state).
        
        Comment:
        - the noise is 0.2 to make it move to the direction that it wants to go to but with a little chance to move to another direction
        to make it go to random cells and explore it to reach the +10 reward
        - the discount factor is 1 as we want to reach the +10 reward and we want to consider it even if it is far away to go to it 
        - the living reward is -0.02 to make it avoid the -10 cells and choose the safe path to +10
        '''
        return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.02
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    '''
    we want the policy to avoid any terminal state and keep the episode going on
    forever.
    
    Comment:
    - what matters here is to make the living_reward large so the agent is pleasent and 
    do not want to reach any terminal state so i set it to 100 
    - the noise is 0 to make it in the direction that it wants to go to without going by randomness to terminal state
    - the discount factor whatever the value that it is equal to it will make the agent to avoid the terminal state 
    because of the living reward 
    '''
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": 100
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    '''
    we want the policy to seek any terminal state (even ones with the -10 penalty) and
    try to end the episode in the shortest time possible.
    
    Comment:
    - it is the opposite of the case of question 5 so i will make the living reward to be -100(which is less than any penalty in the grid)
    to make the agent to reach the terminal state as soon as possible to end the episode as it has large penalty on every state it goes to 
    -  the noise is 0 to make it in the direction that it wants to avoid making agent suffer in non terminal instead of going to terminal 
    state and to determinstic about its actions
    - the discount factor can't be 0 as it will not consider any other state reward and this may make it far from the terminal state
    but it can be set to any other value greater than 0 i make it 1 to consider all rewards in the future to go to terminal state 
    '''
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -100
    }