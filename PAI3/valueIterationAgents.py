# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    # Init : Not required

    # Value iteration
    for i in range(iterations):
        old_values = self.values.copy()
        for state in mdp.getStates():
            value_state_action = []
            for action in mdp.getPossibleActions(state):
                val = 0 
                transition = mdp.getTransitionStatesAndProbs(state,action)
                for sstate,prob_s_a_ss in transition:
                    val += prob_s_a_ss*(mdp.getReward(state,action,sstate) + discount*old_values[sstate])
                value_state_action.append(val)
            if value_state_action : self.values[state] = max(value_state_action)
            

    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    qvalue = 0
    transition = self.mdp.getTransitionStatesAndProbs(state,action)
    for sstate,prob_s_a_ss in transition:
        qvalue += prob_s_a_ss*(self.mdp.getReward(state,action,sstate) + self.discount*self.values[sstate])
    return qvalue


  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    actions = self.mdp.getPossibleActions(state)

    if not actions:
        return None
    
    best_action = actions[0]
    best_QValue = self.getQValue(state,actions[0])
    for action in actions[1:]:
        temp = self.getQValue(state,action)
        if temp > best_QValue :
            best_QValue = temp
            best_action = action
    
    return best_action
    

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
