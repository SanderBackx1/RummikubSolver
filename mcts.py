
import math
from collections import defaultdict
from abc import ABC, abstractmethod


class MCTS:
    "Monte Carlo tree searcher"

    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)
        self.N = defaultdict(int)
        self.children = dict()
        self.exploration_weight = exploration_weight

    
    def choose(self, node):
        if node.is_terminal():
            raise RuntimeError(f"choose called terminal on node {node}")
        
        if node not in self.children:
            return node.find_random_child()
        
        def score(n):
            if self.N[n]==0:
                return float("-inf")
            return self.Q[n]/self.N[n]
        return max(self.children[node], key=score)
    

    def do_rollout(self,node):
        path= self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path,reward)
    
    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self,node):
        if node in self.children:
            return #already expanded
        
        self.children[node] = node.find_children()

    def _simulate(self, node):
        invert_reward = True

        while True:
            if node.is_terminal():
                reward = node.reward()
                return 1-reward if invert_reward else reward

            node = node.find_random_child()
            invert_reward = not invert_reward

    def _backpropagate(self,path,reward):
        for node in reversed(path):
            self.N[node]+=1
            self.Q[node]+=reward
            reward = 1-reward
    
    def _uct_select(self,node):
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            return self.Q[n]/self.N[n]+self.exploration_weight*math.sqrt(log_N_vertex/self.N[n])
        
        return max (self.children[node], key=uct)
    

class Node(ABC):
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """

    @abstractmethod
    def find_children(self):
        "All possible successors of this board state"
        return set()

    @abstractmethod
    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        return None

    @abstractmethod
    def is_terminal(self):
        "Returns True if the node has no children"
        return True

    @abstractmethod
    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        return 0

    @abstractmethod
    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True



