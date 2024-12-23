from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        if self.mdp.is_terminal(state):
            return 0
        max_utility = float('-inf')
        for action in self.mdp.get_actions(state):
            possible_expected_utility = 0
            for next_state, probability in self.mdp.get_successor(state, action).items():
                possible_expected_utility += probability * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state])
            max_utility = max(max_utility, possible_expected_utility)
        return max_utility
    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        utilities = self.utilities.copy()
        max_diff = 0
        is_converged = False
        for state in self.mdp.get_states():
            # print("/////////////////")
            # print(self.utilities[state])
            # print("/////////////////")
            utilities[state] = self.compute_bellman(state)
            max_diff = max(abs(utilities[state] - self.utilities[state]), max_diff)
        self.utilities = utilities
        return max_diff <= tolerance

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iterations
        # or until the utilities converge
        for i in range(1,iterations+1):
            if self.update(tolerance):
                return i
        return iterations
            
            
    
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        if self.mdp.is_terminal(state): 
            return None
        best_action = None
        best_utility = float('-inf')
        for action in self.mdp.get_actions(state):
            utility = self.utilities[state]
            for next_state, probability in self.mdp.get_successor(state, action).items():
                utility += probability * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state])
            if utility > best_utility:
                best_utility = utility
                best_action = action
        return best_action
        
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
