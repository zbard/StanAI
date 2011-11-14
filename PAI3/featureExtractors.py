# featureExtractors.py
# --------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"Feature extractors for Pacman game states"

from game import Directions, Actions
import util

class FeatureExtractor:  
  def getFeatures(self, state, action):    
    """
      Returns a dict from features to counts
      Usually, the count will just be 1.0 for
      indicator functions.  
    """
    util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
  def getFeatures(self, state, action):
    feats = util.Counter()
    feats[(state,action)] = 1.0
    return feats

def closestFood(pos, food, walls):
  """
  closestFood -- this is similar to the function that we have
  worked on in the search project; here its all in one place
  """
  fringe = [(pos[0], pos[1], 0)]
  expanded = set()
  while fringe:
    pos_x, pos_y, dist = fringe.pop(0)
    if (pos_x, pos_y) in expanded:
      continue
    expanded.add((pos_x, pos_y))
    # if we find a food at this location then exit
    if food[pos_x][pos_y]:
      return dist
    # otherwise spread out from the location to its neighbours
    nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
    for nbr_x, nbr_y in nbrs:
      fringe.append((nbr_x, nbr_y, dist+1))
  # no food found
  return None

def closestObject(pos, objects, walls):
  fringe = [(pos[0], pos[1], 0)]
  expanded = set()
  while fringe:
    pos_x, pos_y, dist = fringe.pop(0)
    if (pos_x, pos_y) in expanded:
      continue
    expanded.add((pos_x, pos_y))
    # if we find a target object at this location then exit
    if (pos_x,pos_y) in objects:
      return dist
    # otherwise spread out from the location to its neighbours
    nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
    for nbr_x, nbr_y in nbrs:
      fringe.append((nbr_x, nbr_y, dist+1))
  return None

def distAllObject(pos, objects, walls):
  fringe = [(pos[0], pos[1], 0)]
  expanded = set()
  all_distances = []
  while fringe:
    pos_x, pos_y, dist = fringe.pop(0)
    if (pos_x, pos_y) in expanded:
      continue
    expanded.add((pos_x, pos_y))
    # Found object
    if (pos_x,pos_y) in objects:
      all_distances.append(dist)
      objects.remove((pos_x,pos_y))
      if not objects:
        return all_distances
    # otherwise spread out from the location to its neighbours
    nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
    for nbr_x, nbr_y in nbrs:
      fringe.append((nbr_x, nbr_y, dist+1))
  if all_distances:
    return all_distances
  return None

  
class SimpleExtractor(FeatureExtractor):
  """
  Returns simple features for a basic reflex Pacman:
  - whether food will be eaten
  - how far away the next food is
  - whether a ghost collision is imminent
  - whether a ghost is one step away
  """
  
  def getFeatures(self, state, action):
    # extract the grid of food and wall locations and get the ghost locations
    food = state.getFood()
    walls = state.getWalls()
    ghosts = state.getGhostPositions()

    features = util.Counter()
    
    features["bias"] = 1.0
    
    # compute the location of pacman after he takes the action
    x, y = state.getPacmanPosition()
    dx, dy = Actions.directionToVector(action)
    next_x, next_y = int(x + dx), int(y + dy)
    
    # count the number of ghosts 1-step away
    features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

    # if there is no danger of ghosts then add the food feature
    if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
      features["eats-food"] = 1.0
    
    dist = closestFood((next_x, next_y), food, walls)
    if dist is not None:
      # make the distance a number less than one otherwise the update
      # will diverge wildly
      features["closest-food"] = float(dist) / (walls.width * walls.height) 
    features.divideAll(10.0)
    return features



class MyExtractor(FeatureExtractor):
  def getFeatures(self, state, action):
    foodpos = state.getFood()
    foodpos = foodpos.asList()
    walls = state.getWalls()
    capsules = state.getCapsules()
    ghosts = state.getGhostPositions()
    
    SimpleExtractorObject = SimpleExtractor()
    # All this to avoid StaticMethod decorator, or subclassing
    features = SimpleExtractorObject.getFeatures(state,action)

    # compute the location of pacman after he takes the action
    x, y = state.getPacmanPosition()
    dx, dy = Actions.directionToVector(action)
    next_x, next_y = int(x + dx), int(y + dy)
    
    ghostStates =  state.getGhostStates()
    """
    if ghostStates:
        #if ghostStates[0].scaredTimer > 0:
        if ghostStates[0].scaredTimer > 1:
            #features["ghosts-are-scared-till"] = ghostStates[0].scaredTimer
            #features["can-ghosts-eat-me"] = 0
            if features["#-of-ghosts-1-step-away"]:
                features["can-i-eat-ghosts"] = 1
    """
    
    time_left_for_all_neighbour_ghosts = []
    min_time_left_for_all_neighbour_ghosts = 0
    # Find time left for all neighbouring ghosts
    for ghost in ghostStates:
        if (next_x,next_y) in Actions.getLegalNeighbors(ghost.getPosition(),walls):
            time_left_for_all_neighbour_ghosts += [ghost.scaredTimer]
    # Find min time left for ghosts to remain eatable
    if time_left_for_all_neighbour_ghosts:
        min_time_left_for_all_neighbour_ghosts = min(time_left_for_all_neighbour_ghosts)
    if min_time_left_for_all_neighbour_ghosts > 1:
        features["can-i-eat-ghosts"] = 1 / 10.0
        features["#-of-ghosts-1-step-away"] = 0

    # dist of closest ghost - (slow ?) A useless feature ?
    """
    dist = closestObject((next_x, next_y), ghosts, walls)
    if dist is not None:
      features["closest-ghost"] = float(dist) / (walls.width * walls.height * 100) 
    """

    # dist of closest capsule (slow)
    dist = closestObject((next_x, next_y), capsules, walls)
    if dist is not None and features["#-ghosts-1-step-away"]:
      # only eat when u need
      features["closest-capsule"] = float(dist) / (walls.width * walls.height) 

    # dist of all ghosts
    """
    all_dist = distAllObject((next_x,next_y), ghosts, walls)
    if all_dist is not None:
      for index in range(len(all_dist)):
        features["dist_of_ghost"+str(index)] = float(all_dist[index]) / (walls.width * walls.width * 100)
    """

    # Normalize closest-food by danger - all the kewl kids are doing it
    #if all_dist is not None:
    #    cost_norm = sum(disti < 4 for disti in all_dist)
    #    features["closest-food"] = features["closest-food"]/(1+cost_norm)

    # Possible next actions - hardcoded 4 as MAX_NO_ACTIONS. <BAD BAD BAD FEATURE>
    #features["possible-next-actions"] =  (float(len(Actions.getLegalNeighbors((next_x,next_y),walls)))
    #                                     / (4.0 * 100) )

    # Possibly trapped
    poss_actions =  set(Actions.getLegalNeighbors((next_x,next_y),walls))
    poss_ghost_positions = []
    for g in ghosts:
        poss_ghost_positions += Actions.getLegalNeighbors(g, walls)
    remaining_action = poss_actions.difference_update(set(poss_ghost_positions))
    if not remaining_action:
        features["trapped"] = 1 / 10.0
    
    # Bad positions ?
    features[(next_x,next_y)] =  features["#-of-ghosts-1-step-away"] / 100


    # Ghosts in each quadrant
    """
    if features["can-i-eat-ghosts"]:
      for g in ghosts:
        if g[0] > next_x and g[1] > next_y:
            features["top_right_g"] += (1.0/len(ghosts)) /100.0
        if g[0] <= next_x and g[1] > next_y:
            features["top_left_g"] += (1.0/len(ghosts)) /100.0
        if g[0] > next_x and g[1] <= next_y:
            features["bottom_right_g"] += (1.0/len(ghosts)) /100.0
        if g[0] <= next_x and g[1] <= next_y:
            features["bottom_left_g"] += (1.0/len(ghosts)) /100.0
    """
    # food in each quadrant
    """
    for f in foodpos:
        if f[0] > next_x and f[1] > next_y:
            features["top_right_f"] += (1.0/len(foodpos)) /100.0
        if f[0] <= next_x and f[1] > next_y:
            features["top_left_f"] += (1.0/len(foodpos)) /100.0
        if f[0] > next_x and f[1] <= next_y:
            features["bottom_right_f"] += (1.0/len(foodpos)) /100.0
        if f[0] <= next_x and f[1] <= next_y:
            features["bottom_left_f"] += (1.0/len(foodpos)) /100.0
    """

    return features
