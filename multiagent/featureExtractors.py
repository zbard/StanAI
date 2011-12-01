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

def numCloseObjects(pos, objects, walls,max_dist):
  fringe = [(pos[0], pos[1], 0)]
  expanded = set()
  num = 0
  while fringe:
    pos_x, pos_y, dist = fringe.pop(0)
    if (pos_x, pos_y) in expanded:
      continue
    if dist > max_dist:
      return num
    expanded.add((pos_x, pos_y))
    # if we find a target object at then add to num
    if (pos_x,pos_y) in objects:
        num += 1
    # otherwise spread out from the location to its neighbours
    nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
    for nbr_x, nbr_y in nbrs:
      fringe.append((nbr_x, nbr_y, dist+1))
  return 0

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
    features["#-of-ghosts-1-step-away"] = 1 / (
            1 + sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts))

    dist = closestFood((next_x, next_y), food, walls)
    if dist is None:
        dist = 0
    features["closest-food"] = 1 / ( 1+ (float(dist) / (walls.width * walls.height)) )
    
    return features.totalCount()



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
    tot_size = walls.width*walls.height
    num_close_ghosts = numCloseObjects((next_x, next_y), ghosts, walls,3)
    temp = (1.0 + num_close_ghosts) / 10
    features["no-of-close-ghosts"] = num_close_ghosts / 10.0

    # dist of closest capsule (slow)
    dist = closestObject((next_x, next_y), capsules, walls)
    if dist is not None:
      features["closest-capsule"] = float(dist) / (walls.width * walls.height) 


    # Possibly trapped
    poss_actions =  Actions.getLegalNeighbors((next_x,next_y),walls)
    poss_actions = set(poss_actions)
    poss_ghost_positions = []
    for g in ghosts:
        poss_ghost_positions += Actions.getLegalNeighbors(g, walls)
    remaining_action = poss_actions - set(poss_ghost_positions)
    if not remaining_action:
        features["trapped"] = 1 / 10.0

    return features
