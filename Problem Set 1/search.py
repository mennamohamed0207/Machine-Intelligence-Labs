from problem import HeuristicFunction, Problem, S, A, Solution
from helpers import utils

#TODO: Import any modules you want to use
import queue

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution
class Node:
    state: S
    cumlative_successful_path:list
    cost:float
    def __init__(self,state,cumlative_successful_path,cost=0):
        self.state=state
        self.cumlative_successful_path=cumlative_successful_path
        self.cost=cost
    def __lt__(self, other):
        return self.cost < other.cost
    def __gt__(self, other):
        if self.cost > other.cost:
            return True
        if self.cost == other.cost:
            return self.order > other.order
        return False
    def __eq__(self, other):
        return self.state == other.state
    
def BreadthFirstSearch(problem: Problem[S, A], initial: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    node=Node(initial,[])
    if problem.is_goal(node.state):
        return node.cumlative_successful_path
    frontier = queue.Queue()
    frontier_handle_duplicates=set()
    frontier.put(Node(initial,[]))
    #this set is added as we are implementing the graph version of the algorithm so we need to handle duplicates states that enters the frontier
    frontier_handle_duplicates.add(node.state)
    explored = set()
    while not frontier.empty():
        node = frontier.get()
        explored.add(node)
        for action in problem.get_actions(node.state):
            child=problem.get_successor(node.state,action)
            
            if child not in explored and child not in frontier_handle_duplicates :
                if problem.is_goal(child):
                    return node.cumlative_successful_path+[action]
                frontier.put(Node(child,node.cumlative_successful_path+[action]))
                frontier_handle_duplicates.add(child)
    return None

def DepthFirstSearch(problem: Problem[S, A], initial: S) -> Solution:
    node = Node(initial, [])


    frontier = queue.LifoQueue()
    frontier_handle_duplicates = set()
    frontier.put(Node(initial, []))
    frontier_handle_duplicates.add(node.state)

    explored = set()
    
    while not frontier.empty():
        node = frontier.get()
        # nodeFromSet=frontier_handle_duplicates.pop()
    
        explored.add(node.state)
        if problem.is_goal(node.state):
            return node.cumlative_successful_path

        for action in problem.get_actions(node.state):
            child = problem.get_successor(node.state, action)

            if child not in explored and child not in frontier_handle_duplicates: 
                frontier.put(Node(child, node.cumlative_successful_path + [action]))
                frontier_handle_duplicates.add(child)

    return None
    
def UniformCostSearch(problem: Problem[S, A], initial: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    node=Node(initial,[],0)
    frontier = queue.PriorityQueue()
    frontier_handle_duplicates=set()
    frontier.put(node)
    #this set is added as we are implementing the graph version of the algorithm so we need to handle duplicates states that enters the frontier
    frontier_handle_duplicates.add(node.state)
    explored = set()
    while not frontier.empty():
        node = frontier.get()
        explored.add(node.state)
        if problem.is_goal(node.state):
            return node.cumlative_successful_path
        for action in problem.get_actions(node.state):
            child = problem.get_successor(node.state, action)
            child_path = node.cumlative_successful_path + [action]
            child_cost = node.cost + problem.get_cost(node.state, action)
            child_node = Node(child, child_path, child_cost)
            
            # Check if child is in explored or frontier
            if child not in explored and child not in frontier_handle_duplicates:
    
                frontier.put(child_node)
                frontier_handle_duplicates.add(child)
                
            elif child_node in frontier.queue:
                #get frontier index
                frontierPosition=frontier.queue.index(child_node)
                frontier_top=frontier.queue[frontierPosition]
                if child_cost<=frontier_top.cost:
                    frontier.queue[frontierPosition]=child_node          
    
    return None  

def AStarSearch(problem: Problem[S, A], initial: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    utils.NotImplemented()

def BestFirstSearch(problem: Problem[S, A], initial: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    utils.NotImplemented()