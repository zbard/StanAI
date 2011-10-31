# Code for a Bayes net


class Event:
    def __init__(self, name, parents, prob_table):
        # conditions of event, and their probabilities. This needs all probabilities
        self.name = name
        # parents = [parent_events]
        self.parents = parents
        self.values = [True,False]
        self.prob_table = {}
        for condition, probability in prob_table:
            # condition is a set: (parent_name,parent_value)*,value) tuples
            self.prob_table[set(condition)] = probability
        #check if all conditions have probability    

class Bayes_net:
    def __init__(self,events):
        # should really check if DAG
        self.events = events

    def getHidden(self,evidence):
        # evidence is list of tuples (var_name, value[either True or False])
        #returns node not having a value in evidence
        hidden = []

        for event in self.events:
            for var_name,value in evidence:
                if event.name = var_name:
                    hidden.append(event)
                    break

        return hidden

# actual evil evil evil code now begins


def enumeration_all(var_values, bn):
    # var_values is list of tuples (var_name, value[either True or False])
    prob = 1

    for event in bn.events:
        condition = []
        # Should probably move this to Event class. 
        for parent in event.parents:
            #for values in parents.values <if there were multiple vals>
            if (parent.name,True) in var_values:
                condition.append((parent.name,True))
            else
                #if (parent.name,False) in var_values
                condition.append((parent.name,False))
        if (event.name,True) in var_values:
            condition.append(True)
        else
            condition.append(False)
        prob = prob * event.prob_table(set(condition))


def enumeration_ask(evidence, rest, bn):
    # evidence is list of tuples (var_name, value[either True or False])
    # rest is unassigned hidden variables list
    prob = 0


    # if all variable values are known
    if not rest:
        return enumeration_all(evidence,bn):

    next_event = rest[0]

    for val in next_event.values:
        prob += enumeration_ask(evidence + [(next_event.name,val)],rest[1:],bn)

    return prob        


def enumeration_custom(query,evidence,bn):
    # query is list of tuples (var_name, value[either True or False])
    # evidence is list of tuples (var_name, value[either True or False])

    # A general query of the form P(x=X,y=Y,z=Z|a=A,b=B,c=C)
    # has sol : P(x=X,y=Y,z=Z,a=A,b=B,c=C) / P(a=A,b=B,c=C)

    # Alternatively for P(X+|a+,b-,c+) I can calculate 
    # P(X+,a+,b-,c+) and P(X-,a+,b-,c+) : and normalize 

    prob_intersection = enumeration_ask(query + evidence, bn.getHidden(query+evidence),bn)
    prob_normalise = enumeration_ask(evidence, bn.getHidden(evidence),bn)

    return (prob_intersection/prob_normalise)

