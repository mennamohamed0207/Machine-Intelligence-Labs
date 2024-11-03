from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils


# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

#TODO: Import any modules and write any functions you want to use
from collections import deque

# 2/12 of testcase passed 
'''
in this function I am trying to make use of problem cashe that each state has a distance which is the min distance between player and coin and coin and exit 
the min distance of all coins is the one that is in the problem cache 
if there is no coins then manhattan_distance between player and exit 
and here the distance is calculated through manhattan_distance
but obviously it is not the best one 
'''
# def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
#     #TODO: ADD YOUR CODE HERE
#     #IMPORTANT: DO NOT USE "problem.is_goal" HERE.
#     # Calling it here will mess up the tracking of the explored nodes count
#     # which is considered the number of is_goal calls during the search
#     #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
#     # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function

#     if state in problem.cache():
#         return problem.cache()[state]

#     coins = state.remaining_coins
#     minDistance = float('inf')
#     exit = problem.layout.exit
#     if len(coins) == 0:
#         minDistance = manhattan_distance(state.player, exit)
#         problem.cache()[state] = minDistance
#         return minDistance
#     currentdist = 0
#     for step in coins:
#         currentdist= manhattan_distance(state.player, step)
#         currentdist += manhattan_distance(step, exit)
#         minDistance = min(minDistance, currentdist)
#     problem.cache()[state] = minDistance
#     return minDistance


'''
in this function I am trying to make use of problem cashe that each state has a distance which is the max distance between player and coin and coin and exit 
the max distance of all coins is the one that is in the problem cache 
if there is no coins then manhattan_distance between player and exit 
and here the distance is calculated through manhattan_distance
just using the max coin with manhattan_distance between player and coin and coin and exit made a little better
'''
# 6/12 of testcase passed 
# def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
#     #TODO: ADD YOUR CODE HERE
#     #IMPORTANT: DO NOT USE "problem.is_goal" HERE.
#     # Calling it here will mess up the tracking of the explored nodes count
#     # which is considered the number of is_goal calls during the search
#     #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
#     # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function

#     if state in problem.cache():
#         return problem.cache()[state]

#     coins = state.remaining_coins
#     maxDistance = 0
#     exit = problem.layout.exit
#     if len(coins) == 0:
#         maxDistance = manhattan_distance(state.player, exit)
#         maxDistance = manhattan_distance(state.player, exit)
#         problem.cache()[state] = maxDistance
#         return maxDistance
#     currentdist = 0
#     for step in coins:
#         currentdist= manhattan_distance(state.player, step)
#         currentdist += manhattan_distance(step, exit)
#         maxDistance = max(maxDistance, currentdist)
#     problem.cache()[state] = maxDistance
#     return maxDistance


def bfs_cost_distance(start: Point, targets: set[Point], walkable: set[Point]) -> dict[Point, int]:
    queue = deque([(start, 0)])
    visited = {start}
    distances = {}
    while queue:
        current, dist = queue.popleft()
        # If we reached a coin then save the distance to that coin in the distances dict
        if current in targets:
            distances[current] = dist
            if len(distances) == len(targets):
                break
        for direction in Direction:
            neighbor = current + direction.to_vector()
            if neighbor in walkable and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return distances

''''
what i made different here is that i have used different distance fucntion which is bfs instead of using manhathan_distance 
which makes much better results

'''
# 8/12 of testcase passed 
def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    if state in problem.cache():
        return problem.cache()[state]

    coins= state.remaining_coins
    exit= problem.layout.exit
    walkable= problem.layout.walkable
    if len(coins) == 0:
        exitDistance = manhattan_distance(state.player, exit)
        problem.cache()[state] = exitDistance
        return exitDistance

    playerToCoins = bfs_cost_distance(state.player, coins, walkable)
    coinsToExit = bfs_cost_distance(exit, coins, walkable)

    maxDistance = 0
    
    for coin in coins:
        playerToCoinCost = playerToCoins.get(coin)
        coinToExitCost = coinsToExit.get(coin)
        maxDistance = max(maxDistance, playerToCoinCost + coinToExitCost)

    problem.cache()[state] = maxDistance
    return maxDistance
