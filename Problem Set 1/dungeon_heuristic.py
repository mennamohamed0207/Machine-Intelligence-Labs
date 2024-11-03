from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

#TODO: Import any modules and write any functions you want to use
from search import BreadthFirstSearch
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
#     maxDistance = float('inf')
#     exit = problem.layout.exit
#     if len(coins) == 0:
#         maxDistance = manhattan_distance(state.player, exit)
#         problem.cache()[state] = maxDistance
#         return maxDistance
#     currentdist = 0
#     for step in coins:
#         currentdist= manhattan_distance(state.player, step)
#         currentdist += manhattan_distance(step, exit)
#         maxDistance = min(maxDistance, currentdist)
#     problem.cache()[state] = maxDistance
#     return maxDistance

from collections import deque

def bfs_distance(start: Point, targets: set[Point], walkable: set[Point]) -> dict[Point, int]:
    """Find the shortest distance from start to each target in targets using BFS."""
    queue = deque([(start, 0)])
    visited = {start}
    distances = {}
    
    while queue:
        current, dist = queue.popleft()
        
        # If we reached a target, save the distance
        if current in targets:
            distances[current] = dist
            if len(distances) == len(targets):
                break  # Stop if we found all target distances

        # Explore neighbors (up, down, left, right)
        for direction in Direction:
            neighbor = current + direction.to_vector()
            if neighbor in walkable and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return distances

def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    # Check cache first
    if state in problem.cache():
        return problem.cache()[state]

    # No coins left, return distance to exit
    if not state.remaining_coins:
        distance_to_exit = manhattan_distance(state.player, problem.layout.exit)
        problem.cache()[state] = distance_to_exit
        return distance_to_exit

    # Get BFS distances from player to all coins and to the exit
    coin_distances = bfs_distance(state.player, state.remaining_coins, problem.layout.walkable)
    exit_distances = bfs_distance(problem.layout.exit, state.remaining_coins, problem.layout.walkable)

    # Estimate cost by selecting the coin that minimizes the path: player -> coin -> exit
    min_cost = 0
    
    for coin in state.remaining_coins:
        cost_to_coin = coin_distances.get(coin, 0)
        cost_to_exit = exit_distances.get(coin, 0)
        min_cost = max(min_cost, cost_to_coin + cost_to_exit)

    # Cache and return the heuristic value
    problem.cache()[state] = min_cost
    return min_cost
