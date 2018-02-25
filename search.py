# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def graphSearch(problem, fringe):
    """
    Search through the successors of the problem to find a goal. The argument
    fringe should be an empty queue.
    """
    startState = problem.getStartState()
    fringe.push(Node(startState))
    try:
        startState.__hash__() #TODO: Does this identify elements of the startstate as unique?
        visited = set()
    except:
        visited = list()

    while not fringe.isEmpty():
        currentNode = fringe.pop()
        #print type(currentNode.state[1])
        if problem.isGoalState(currentNode.state):
                return [node.action for node in currentNode.nodePath()][1:]
        try: 
            inVisited = currentNode.state in visited 
        except:
            visited = list(visited)
            inVisited = currentNode.state in visited 
        if not inVisited:
            if isinstance(visited, list): 
                visited.append(currentNode.state)
            else:
                visited.add(currentNode.state)
            for node in currentNode.expand(problem):
                fringe.push(node)
    return None

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    
    util.raiseNotDefined()
    """
    return graphSearch(problem, util.Stack())

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    #util.raiseNotDefined()
    return graphSearch(problem, util.Queue())

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    #util.raiseNotDefined()
    return graphSearch(problem, util.PriorityQueueWithFunction(lambda x: x.path_cost))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first.
    "*** YOUR CODE HERE ***"
    """
    return graphSearch(problem, util.PriorityQueueWithFunction(
        lambda node: node.path_cost + heuristic(
            node.state, problem)))

class Node:
    """ 
    AIMA: A node in a search tree. Contains a pointer to the parent of this node, 
    the state of this node, the action that got us to this node, the path leading to
    this node, and the total cost of that path. 

    This class was taken from Dr. Yoon's lecture slides, which took the class from the 
    recommended textbook.
    """

    def __init__(self, state, parent=None, action=None, path_cost=0):
        # Create a search tree Node, derived from a parent by an action
        self.state = state
        self.parent = parent
        self.action = action 
        if parent:
            self.path_cost = parent.path_cost + path_cost
            self.depth = parent.depth + 1
        else:
            self.path_cost = path_cost
            self.depth = 0

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def nodePath(self):
        # Create a list of nodes from the root to this node
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        result.reverse()
        return result

    def expand(self, problem):
        """
        Return a list of nodes reachable from this node
        """
        return [Node(next, self, act, cost)
                for (next, act, cost) in problem.getSuccessors(self.state)]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
