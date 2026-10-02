# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# # Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in obj-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()


def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# def addSuccessors(problem, addCost=True):

class SearchNode:
    def __init__(self, parent, node_info):
        """
            parent: parent SearchNode.

            node_info: tuple with three elements => (coord, action, cost)

            coord: (x,y) coordinates of the node position

            action: Direction of movement required to reach node from
            parent node. Possible values are defined by class Directions from
            game.py

            cost: cost of reaching this node from the starting node.
        """

        self.__state = node_info[0]
        self.action = node_info[1]
        self.cost = node_info[2] if parent is None else node_info[2] + parent.cost
        self.parent = parent

    # The coordinates of a node cannot be modified, se we just define a getter.
    # This allows the class to be hashable.
    @property
    def state(self):
        return self.__state

    def get_path(self):
        path = []
        current_node = self
        while current_node.parent is not None:
            path.append(current_node.action)
            current_node = current_node.parent
        path.reverse()
        return path
    
    # Consider 2 nodes to be equal if their coordinates are equal (regardless of everything else)
    # def __eq__(self, __o: obj) -> bool:
    #     if (type(__o) is SearchNode):
    #         return self.__state == __o.__state
    #     return False

    # # def __hash__(self) -> int:
    # #     return hash(self.__state)

def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.get_start_state())
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    # Keep each node's parent and incoming action so the final route can be rebuilt.
    start_node = SearchNode(None, (problem.get_start_state(), None, 0))
    fringe = util.Stack()
    fringe.push(start_node)
    explored = set()

    while not fringe.is_empty():
        node = fringe.pop()
        # Skip duplicate paths so each state is expanded at most once.
        if node.state in explored:
            continue

        explored.add(node.state)
        if problem.is_goal_state(node.state):
            return node.get_path()

        # Push successors in the problem's order; the stack explores the last first.
        for successor, action, step_cost in problem.get_successors(node.state):
            if successor not in explored:
                fringe.push(SearchNode(node, (successor, action, step_cost)))

    # An empty stack means no route to a goal exists.
    return []



def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    start_node = SearchNode(None, (problem.get_start_state(), None, 0))
    fringe = util.Queue()
    fringe.push(start_node)
    explored = set()

    while not fringe.is_empty():
        node = fringe.pop()
        # Ignore duplicate paths so each state is expanded at most once.
        if node.state in explored:
            continue

        explored.add(node.state)
        if problem.is_goal_state(node.state):
            return node.get_path()

        # FIFO ordering ensures all shallower states are processed first.
        for successor, action, step_cost in problem.get_successors(node.state):
            if successor not in explored:
                fringe.push(SearchNode(node, (successor, action, step_cost)))

    # An empty queue means no route to a goal exists.
    return []

def uniform_cost_search(problem):
    """Search the node of least total cost first."""
    start_node = SearchNode(None, (problem.get_start_state(), None, 0))
    fringe = util.PriorityQueue()
    fringe.push(start_node, start_node.cost)
    best_cost = {start_node.state: start_node.cost}
    explored = set()

    while not fringe.is_empty():
        node = fringe.pop()
        # Ignore outdated paths and states that have already been expanded.
        if node.cost != best_cost[node.state] or node.state in explored:
            continue

        explored.add(node.state)
        if problem.is_goal_state(node.state):
            return node.get_path()

        # Keep only a cheaper route to each state; priorities use total path cost.
        for successor, action, step_cost in problem.get_successors(node.state):
            if successor in explored:
                continue

            successor_node = SearchNode(node, (successor, action, step_cost))
            if successor_node.cost < best_cost.get(successor, float('inf')):
                best_cost[successor] = successor_node.cost
                fringe.push(successor_node, successor_node.cost)

    # An empty priority queue means no route to a goal exists.
    return []

def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def a_star_search(problem, heuristic=null_heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()

# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
