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
    
def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    node=Node(initial_state,[])
    if problem.is_goal(node.state):
        return node.cumlative_successful_path
    frontier = queue.Queue()
    frontier_handle_duplicates=set()
    frontier.put(Node(initial_state,[]))
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

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    node = Node(initial_state, [])
    if problem.is_goal(node.state):
        return node.cumlative_successful_path

    # Use LifoQueue to implement a stack
    frontier = queue.LifoQueue()
    frontier_handle_duplicates = set()
    frontier.put(Node(initial_state, []))
    frontier_handle_duplicates.add(node.state)

    explored = set()
    
    while not frontier.empty():
        node = frontier.get()
        explored.add(node.state)

        for action in problem.get_actions(node.state):
            child_state = problem.get_successor(node.state, action)

            if child_state not in explored and child_state not in frontier_handle_duplicates:
                if problem.is_goal(child_state):
                    return node.cumlative_successful_path + [action]
                
                # Push the child node onto the stack (LifoQueue)
                frontier.put(Node(child_state, node.cumlative_successful_path + [action]))
                frontier_handle_duplicates.add(child_state)

    return None
    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    utils.NotImplemented()

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    utils.NotImplemented()

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    utils.NotImplemented()