# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
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
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  from game import Directions
  from util import Stack
  Explored = {}
  Frontier = Stack()
  
  node = 0
  current = problem.getStartState()
  Explored[current] = 1;
  succ = problem.getSuccessors(current)
  for k in succ:
    #print "initial push",k
    Frontier.push([k]);
    Explored[k[0]] = 1;

  while not (Frontier.isEmpty()):
      current = Frontier.pop()
      node = current[-1][0]
      #print "curr path and node",current,node,"explored status",(node in Explored),"\n"
      # check if done
      if (problem.isGoalState(node)):
          break
      succ = problem.getSuccessors(node)
      for k in succ:
          if not (k[0] in Explored):
            Frontier.push(current + [k]);
            Explored[k[0]] = 1;
 
  sol = []
  #print current
  for k in current:
    sol += [k[1]]    

  # print sol
  return  sol
 
  # temporary
  # return  [s,s,w,s,w,w,s,w]

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  from game import Directions
  from util import Queue
  Explored = {}
  Frontier = Queue()
  
  node = 0
  current = problem.getStartState()
  #print "bfs first state", current
  Explored[current] = 1
  succ = problem.getSuccessors(current)
  for k in succ:
    #print "initial push",k
    Frontier.push([k]);
    Explored[k[0]] = 1;

  while not (Frontier.isEmpty()):
      current = Frontier.pop()
      node = current[-1][0]
      #print "curr path and node",current,node,"explored status",(node in Explored),"\n"
      # check if done
      if (problem.isGoalState(node)):
          break
      #print node
      succ = problem.getSuccessors(node)
      for k in succ:
          if not (k[0] in Explored):
              #if not (Frontier.isPresent(current + [k])):
                Frontier.push(current + [k]);
                Explored[k[0]] = 1;
 
  sol = []
  for k in current:
    sol += [k[1]]

  #print current
  #print "action sol", sol
  return  sol
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  from game import Directions
  from util import PriorityQueue
  Explored = {}
  Frontier = PriorityQueue()
  
  node = 0
  current = problem.getStartState()
  Explored[current] = 1;
  succ = problem.getSuccessors(current)
  for k in succ:
    t = [k[2],k]  
    #print "initial push",t
    Frontier.push(t,t[0]);
    Explored[k[0]] = 1;

  while not (Frontier.isEmpty()):
      current = Frontier.pop()
      dist = current[0]
      #print "prior", priority
      node = current[-1][0]
      #print "curr path and node",current,node,"explored status",(node in Explored),"\n"
      # check if done
      if (problem.isGoalState(node)):
          break
      succ = problem.getSuccessors(node)
      for k in succ:
          if not (k[0] in Explored):
            t = [] + current + [k]
            t[0] += k[2] 
            Frontier.push(t,t[0]);
            Explored[k[0]] = 1;
 
  sol = []
  #print current
  for k in current[1:]:
    sol += [k[1]]    

  #print sol
  return  sol

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  from game import Directions
  from util import PriorityQueue
  Explored = {}
  Frontier = PriorityQueue()
  
  node = 0
  current = problem.getStartState()
  #print "started astar at",current
  Explored[current] = 1
  succ = problem.getSuccessors(current)
  for k in succ:
    t = [k[2],k]  
    #print "initial push",t
    Frontier.push(t,t[0]+heuristic(k[0],problem));
    Explored[k[0]] = 1;

  #return 0
  while not (Frontier.isEmpty()):
      current = Frontier.pop()
      dist = current[0]
      #print "prior", priority
      node = current[-1][0]
      #print "curr path and node",current,node,"explored status",(node in Explored),"\n"
      # check if done
      if (problem.isGoalState(node)):
          break
      succ = problem.getSuccessors(node)
      for k in succ:
          if not (k[0] in Explored):
            t = [] + current + [k]
            #add cost
            t[0] += k[2]
            Frontier.push(t,t[0]+heuristic(k[0],problem));
            Explored[k[0]] = 1; #can I do this - or is it only for uniform cost searches ? VERIFY
            #check for consistency - 
            if(heuristic(node,problem) - heuristic(k[0],problem)) > k[2]:
                print "Warning - inconsistencey. Heuristic decreases by greater than cost"
                print "Original node ",node,",and its h:",heuristic(node,problem,True)
                print "Successor node ",k[0],",and its h:",heuristic(k[0],problem,True)

 
  sol = []
  #print current
  for k in current[1:]:
    sol += [k[1]]    

  #print sol
  return  sol
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
