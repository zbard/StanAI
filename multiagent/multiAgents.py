# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
import featureExtractors

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
      self. evalclass = featureExtractors.SimpleExtractor()

  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    #Use reinforcment feat extractor
    f = self.evalclass.getFeatures(currentGameState,action)
    e = successorGameState.getScore() 
    e += f
    return e

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getValue(self,gameState,agent,current_depth):
      val = None
      
      if agent >= gameState.getNumAgents() :
          agent = agent % gameState.getNumAgents()
          current_depth += 1
      
      # if max depth is reached
      if current_depth > self.depth:
          val = self.evaluationFunction(gameState)

      # if leaf node:
      if gameState.isWin() or gameState.isLose():
          val = self.evaluationFunction(gameState)

      if not val == None:
          return val

      # identify next level of nodes; increase depth if needed
      if agent == 0:
          val = self.maxValue(gameState,agent,current_depth)
      else:
          val = self.minValue(gameState,agent,current_depth)
      
      return val

  def maxValue(self,gameState,agent,current_depth,return_best_action = 0 ):
      maxval = []
      best_action = Directions.STOP

      pos_actions = gameState.getLegalActions(agent)
      pos_actions.remove(Directions.STOP)

      for action in pos_actions:
          newState = gameState.generateSuccessor(agent,action)
          value = self.getValue(newState,agent+1,current_depth)
          maxval = [max(maxval + [value])]
          if (return_best_action) and (maxval[0] == value):
              best_action = action
   
      if return_best_action:
          return best_action
      else:
          return maxval[0]


  def minValue(self,gameState,agent,current_depth):
      minval = []

      pos_actions = gameState.getLegalActions(agent)

      for action in pos_actions:
          newState = gameState.generateSuccessor(agent,action)
          value = self.getValue(newState,agent+1,current_depth)
          minval = [min(minval + [value])]
    
      return minval[0]


  def getAction(self, gameState):
      return self.maxValue(gameState,0,1,1)


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  def getValue(self,gameState,agent,current_depth,alpha,beta):
      val = None
      
      if agent >= gameState.getNumAgents() :
          agent = agent % gameState.getNumAgents()
          current_depth += 1
      
      # if max depth is reached
      if current_depth > self.depth:
          val = self.evaluationFunction(gameState)

      # if leaf node:
      if gameState.isWin() or gameState.isLose():
          val = self.evaluationFunction(gameState)

      if not val == None:
          return val

      # identify next level of nodes; increase depth if needed
      if agent == 0:
          val = self.maxValue(gameState,agent,current_depth,alpha,beta)
      else:
          val = self.minValue(gameState,agent,current_depth,alpha,beta)
      
      return val

  def maxValue(self,gameState,agent,current_depth,alpha,beta,return_best_action=0):
      best_action = Directions.STOP

      pos_actions = gameState.getLegalActions(agent)
      pos_actions.remove(Directions.STOP)

      for action in pos_actions:
          newState = gameState.generateSuccessor(agent,action)
          value = self.getValue(newState,agent+1,current_depth,alpha,beta)
          alpha = max([alpha,value])
          if (return_best_action) and (alpha == value):
              # Should randomly break ties ?
              best_action = action
          if alpha >= beta:
              if return_best_action : return best_action
              else : return alpha
   
      if return_best_action: return best_action
      else: return alpha


  def minValue(self,gameState,agent,current_depth,alpha,beta):
      pos_actions = gameState.getLegalActions(agent)

      for action in pos_actions:
          newState = gameState.generateSuccessor(agent,action)
          value = self.getValue(newState,agent+1,current_depth,alpha,beta)
          beta = min([beta,value])
          if alpha >= beta:
              return beta
      
      return beta

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    return self.maxValue(gameState,0,1,-10000, +10000, 1)

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  def getValue(self,gameState,agent,current_depth,alpha,beta):
      val = None
      
      if agent >= gameState.getNumAgents() :
          agent = agent % gameState.getNumAgents()
          current_depth += 1
      
      # if max depth is reached
      if current_depth > self.depth:
          val = self.evaluationFunction(gameState)

      # if leaf node:
      if gameState.isWin() or gameState.isLose():
          val = self.evaluationFunction(gameState)

      if not val == None:
          return val

      # identify next level of nodes; increase depth if needed
      if agent == 0:
          val = self.maxValue(gameState,agent,current_depth,alpha,beta)
      else:
          val = self.stochasticValue(gameState,agent,current_depth,alpha,beta)
      
      return val

  def maxValue(self,gameState,agent,current_depth,alpha,beta,return_best_action=0):
      best_action = Directions.STOP

      pos_actions = gameState.getLegalActions(agent)
      pos_actions.remove(Directions.STOP)

      for action in pos_actions:
          newState = gameState.generateSuccessor(agent,action)
          value = self.getValue(newState,agent+1,current_depth,alpha,beta)
          alpha = max([alpha,value])
          if (return_best_action) and (alpha == value):
              # Should randomly break ties ?
              best_action = action
          if alpha >= beta:
              if return_best_action : return best_action
              else : return alpha
   
      if return_best_action: return best_action
      else: return alpha


  def stochasticValue(self,gameState,agent,current_depth,alpha,beta):
      pos_actions = gameState.getLegalActions(agent)
      prob = 1.0 / (len(pos_actions))
      value = 0

      for action in pos_actions:
          newState = gameState.generateSuccessor(agent,action)
          value += prob*self.getValue(newState,agent+1,current_depth,alpha,beta)
      
      return value

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    return self.maxValue(gameState,0,1,-10000, +10000, 1)

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

