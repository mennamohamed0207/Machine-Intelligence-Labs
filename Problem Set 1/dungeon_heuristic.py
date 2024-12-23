from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils
from collections import deque
import heapq

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)


def a_star_cost_distance(start, goals, walkable):
    def get_neighbors(node):
        neighbors = []
        for direction in Direction:
            neighbor = node+direction.to_vector()
            if neighbor in walkable:
                neighbors.append(neighbor)
        return neighbors

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: min(manhattan_distance(start, goal) for goal in goals)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current in goals:
            return g_score[current]

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + min(manhattan_distance(neighbor, goal) for goal in goals)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return float('inf')

def prim_mst(points, distances):
    mst_cost = 0
    visited = set()
    min_heap = [(0, points[0])]  # Start with an arbitrary point

    while min_heap:
        cost, point = heapq.heappop(min_heap)
        if point in visited:
            continue
        visited.add(point)
        mst_cost += cost

        for neighbor in points:
            if neighbor not in visited:
                heapq.heappush(min_heap, (distances[point][neighbor], neighbor))

    return mst_cost

def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    if state in problem.cache():
        return problem.cache()[state]

    coins = state.remaining_coins
    exit = problem.layout.exit
    walkable = problem.layout.walkable

    if len(coins) == 0:
        exitDistance = manhattan_distance(state.player, exit)
        problem.cache()[state] = exitDistance
        return exitDistance

    playerToCoins = {coin: a_star_cost_distance(state.player, [coin], walkable) for coin in coins}
    coinsToExit = {coin: a_star_cost_distance(exit, [coin], walkable) for coin in coins}

    # Create a complete graph with coins and calculate MST using Prim's algorithm
    coins_list = list(coins)
    distances = {point: {} for point in coins_list}
    for i, point1 in enumerate(coins_list):
        for j, point2 in enumerate(coins_list):
            if i != j:
                distances[point1][point2] = a_star_cost_distance(point1, [point2], walkable)

    mst_cost = prim_mst(coins_list, distances)

    maxDistance = 0
    for coin in coins:
        playerToCoinCost = playerToCoins.get(coin)
        coinToExitCost = coinsToExit.get(coin)
        maxDistance = max(maxDistance, playerToCoinCost + coinToExitCost + mst_cost)

    problem.cache()[state] = maxDistance
    return maxDistance