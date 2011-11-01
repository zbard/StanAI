# Code for a Bayes net


class Event:
    def __init__(self, name, parents, prob_table,values=[False,True]):
        # conditions(parents) of event, and its cond probabilities.
        # prob_table is list of probabilities.
        # prob_table(i) is the i'th probability in the -
        # probability matrix [Parent1.value Parent2.value .... Self.Value]
        self.name = name
        # parents = [parent_events]
        self.parents = parents
        self.values = values
        self.prob_table = prob_table
        #check if all conditions have probability    
    
    def get_probability(self,all_events):
        var_values = all_events
        condition = 0

        nodes = self.parents + [self]

        for node in nodes:
            is_node_present = False
            for value in node.values:
                if (node.name,value) in var_values:
                    condition = condition*len(node.values)
                    condition += node.values.index(value)
                    is_node_present = True
                    break
            if not is_node_present:
                print "Can't compute conditional value"
                return 1

        return self.prob_table[condition]
        
    

class Bayes_net:
    def __init__(self,events):
        # should really check if DAG
        self.events = events

    def getHidden(self,evidence):
        # evidence is list of tuples (var_name, value[either True or False])
        #returns node not having a value in evidence
        hidden = []
        # check for unknown nodes
        evidence_check = evidence + []

        for event in self.events:
            is_present = False
            for var_name,value in evidence:
                if event.name == var_name:
                    is_present = True
                    evidence_check.remove((var_name,value))
                    break
            if not is_present:    
                hidden.append(event)

        if evidence_check:
            print "Warning : Unknown var,value tuples.",evidence_check

        return hidden

# actual evil evil evil code now begins


def enumeration_all(var_values, bn):
    # var_values is list of tuples (var_name, value[either True or False])
    prob = 1

    for event in bn.events:
        prob = prob * event.get_probability(var_values) 

    return prob

def enumeration_ask(evidence, rest, bn):
    # evidence is list of tuples (var_name, value[either True or False])
    # rest is unassigned hidden variables list
    prob = 0

    # if all variable values are known
    if not rest:
        return enumeration_all(evidence,bn)

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




