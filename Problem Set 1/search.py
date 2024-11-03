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
    index:int
    totalcost:float
    def __init__(self,state,cumlative_successful_path,cost=0,index=0,totalcost=0):
        self.state=state
        self.cumlative_successful_path=cumlative_successful_path
        self.cost=cost
        self.index=index
        self.totalcost=totalcost
    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        if self.cost == other.cost:
            return self.index < other.index
        return False
    def __gt__(self, other):
        if self.cost > other.cost:
            return True
        if self.cost == other.cost:
            return self.index > other.index
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
        explored.add(node.state)
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
            
            if child not in explored and child not in frontier_handle_duplicates:
    
                frontier.put(child_node)
                frontier_handle_duplicates.add(child)
                
                #replace the frontier with the child node if the child node has a lower cost than the one in the frontier
            elif child_node in frontier.queue: 
                #get child index
                frontierPosition=frontier.queue.index(child_node)
                frontier_top=frontier.queue[frontierPosition]
                if child_cost<=frontier_top.cost:
                    frontier.queue[frontierPosition]=child_node          
    
    return None  

def AStarSearch(problem: Problem[S, A], initial: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    node=Node(initial,[],0,index=0)
    frontier = queue.PriorityQueue()
    frontier_handle_duplicates=set()
    frontier.put(node)
    #this set is added as we are implementing the graph version of the algorithm so we need to handle duplicates states that enters the frontier
    frontier_handle_duplicates.add(node.state)
    explored = set()
    index=0
    while not frontier.empty():
        node = frontier.get()
        explored.add(node.state)
        if problem.is_goal(node.state):
            return node.cumlative_successful_path
        
        for action in problem.get_actions(node.state):
            child = problem.get_successor(node.state, action)
            child_path = node.cumlative_successful_path + [action]
            child_AStar_cost = problem.get_cost(node.state, action)+node.totalcost
            child_cost=child_AStar_cost+heuristic(problem,child)
            child_node = Node(child, child_path, child_cost,totalcost=child_AStar_cost)
            child_node.index=index
            index+=1
            if child not in explored and child_node not in frontier.queue:
                frontier.put(child_node)
                frontier_handle_duplicates.add(child)
                #replace the frontier with the child node if the child node has a lower cost than the one in the frontier
            elif child_node in frontier.queue: 
                #get child index
                frontierPosition=frontier.queue.index(child_node)
                frontier_top=frontier.queue[frontierPosition]
                if child_cost < frontier_top.cost:
                    frontier.queue[frontierPosition]=frontier_top 
                    frontier.queue[frontierPosition]=child_node
                elif child_cost == frontier_top.cost:
                    if child_node.index < frontier_top.index:
                        frontier.queue[frontierPosition]=frontier_top
                        frontier.queue[frontierPosition]=child_node

    return None  

def BestFirstSearch(problem: Problem[S, A], initial: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    node=Node(initial,[],0)
    frontier = queue.PriorityQueue()
    frontier.put(node)
    #this set is added as we are implementing the graph version of the algorithm so we need to handle duplicates states that enters the frontier
    explored = set()
    index=0
    while frontier.queue:
        node = frontier.get()
        explored.add(node.state)
        if problem.is_goal(node.state):
            return node.cumlative_successful_path
        for action in problem.get_actions(node.state):
            child = problem.get_successor(node.state, action)
            child_path = node.cumlative_successful_path + [action]
            child_cost = heuristic(problem, child)
            
            child_node = Node(child, child_path, child_cost,index=node.index+1)
            child_node.index=index   
            index+=1
            if child not in explored and child_node not in frontier.queue:
    
                frontier.put(child_node)
                
            elif child_node in frontier.queue: #replace the frontier with the child node if the child node has a lower cost than the one in the frontier
                #get child index
                frontierPosition=frontier.queue.index(child_node)
                frontier_top=frontier.queue[frontierPosition]
                if child_cost < frontier_top.cost:
                    frontier.queue[frontierPosition]=child_node  
                    frontier.queue[frontierPosition]=child_node
                elif child_cost == frontier_top.cost:
                    if child_node.index < frontier_top.index:
                        frontier.queue[frontierPosition]=child_node
                        frontier.queue[frontierPosition]=child_node      
    
    return None  
