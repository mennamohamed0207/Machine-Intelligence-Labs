from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

#TODO: Import any modules and write any functions you want to use

def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.is_goal" HERE.
    # Calling it here will mess up the tracking of the explored nodes count
    # which is considered the number of is_goal calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function

    if state in problem.cache():
        return problem.cache()[state]

    coins = state.remaining_coins
    minDistance = 0
    maxDistance = float('inf')
    wal = problem.layout.walkable
    exit = problem.layout.exit
    if len(coins) == 0:
        minDistance = manhattan_distance(state.player, exit)
        maxDistance = manhattan_distance(state.player, exit)
        problem.cache()[state] = minDistance+maxDistance
        return minDistance
    currentdist = 0
    for step in coins:
        currentdist= manhattan_distance(state.player, step)
        currentdist += manhattan_distance(step, exit)
        minDistance = max(minDistance, currentdist)
        
    
    
    problem.cache()[state] = minDistance
    return minDistance
