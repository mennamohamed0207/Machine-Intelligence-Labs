from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any built in modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None
    
    if max_depth == 0:
        return heuristic(game, state, 0), None
    
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    
    if agent == 0:
        optimized_solution = float('-inf')
        optimized_action = None
        for action, state in actions_states:
            value, actionmax = minimax(game, state, heuristic, max_depth - 1)
            if value > optimized_solution:
                optimized_solution = value
                optimized_action = action
        return optimized_solution, optimized_action
    else:
        optimized_solution = float('inf')
        optimized_action = None
        for action, state in actions_states:
            value, actionmin = minimax(game, state, heuristic, max_depth - 1)
            if value < optimized_solution:
                optimized_solution = value
                optimized_action = action
        return optimized_solution, optimized_action


# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def maxValue(game,state,alpha,beta):
    terminal, values = game.is_terminal(state)

    if terminal:
        return values[0]
    v = float('-inf')
    for action in game.get_actions(state):
        v = max(v,minValue(game,state,alpha,beta))
        if v >= beta:
            return v
        alpha = max(alpha,v)
    return v
def minValue(game,state,alpha,beta): 
    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0]
    v = float('inf')
    for action in game.get_actions(state):
        v = min(v,maxValue(game,state,alpha,beta))
        if v <= alpha:
            return v
        beta = min(beta,v)
    return v
def alphabetapruningWithParameters(game: Game[S, A], state: S, heuristic: HeuristicFunction,alpha=-float('inf'),beta=float('inf'), max_depth: int = -1,sortedcondition:bool=False) -> Tuple[float, A]:
    
        
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None
    
    if max_depth == 0:
        return heuristic(game, state, 0), None
    optimized_solution=0
    if agent ==0:
        optimized_solution=-float('inf')
    else:
        optimized_solution=float('inf')
    optimized_action = None
    actions_states = game.get_actions(state)
    if sortedcondition:
        # print(actions_states)
        # print(type(actions_states[0]))
        #order the actions based on the heuristic value
        
        actions_states = sorted(actions_states,key=lambda x: heuristic(game,game.get_successor(state,x),agent),reverse=True)
        
    for action in actions_states:
        value=alphabetapruningWithParameters(game, game.get_successor(state,action), heuristic,alpha,beta,max_depth - 1,sortedcondition)
        if agent == 0:
            if value[0] > optimized_solution:
                optimized_solution = value[0]
                optimized_action = action
            alpha = max(alpha,optimized_solution)
            if alpha>=beta:
                break
        else:
            
            if value[0] < optimized_solution:
                optimized_solution = value[0]
                optimized_action = action
            beta = min(beta,optimized_solution)
            if beta<=alpha:
                break
    return optimized_solution, optimized_action 
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function   
    alpha,beta=-float('inf'),float('inf')
    value,action=alphabetapruningWithParameters(game,state,heuristic,alpha,beta,max_depth)
    return value,action
    

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    alpha,beta=-float('inf'),float('inf')
    value,action=alphabetapruningWithParameters(game,state,heuristic,alpha,beta,max_depth,True)
    return value,action

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    NotImplemented()