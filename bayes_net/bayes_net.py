# Code for a Bayes net


class Event:
    def __init__(self, name, parents, prob_table):
        # conditions of event, and all their probabilities.
        self.name = name
        # parents = [parent_events]
        self.parents = parents
        self.values = [False,True]
        # prob table is row wise list of lists. It represents 
        # row [parent1=val1,parent2=val1 ....,self=value]
        self.prob_table = prob_table
        #check if all conditions have probability    
    
    def get_probability(self,all_events):
        var_values = all_events
        condition = ""

        for parent in self.parents:
            #for values in parents.values <if there were multiple vals>
            if (parent.name,False) in var_values:
                condition += '0'
            elif (parent.name,True) in var_values:
                condition += '1'
            else:
                print "Unable to calculate conditional prob"
                return 1

        if (self.name,False) in var_values:
            condition += '0'
        else:
            condition += '1'
        
        cond_index = 0

        for i in condition:
            cond_index = cond_index*2 + int(i)
       
        return self.prob_table[cond_index]
        
    

class Bayes_net:
    def __init__(self,events):
        # should really check if DAG
        self.events = events

    def getHidden(self,evidence):
        # evidence is list of tuples (var_name, value[either True or False])
        #returns node not having a value in evidence
        hidden = []

        for event in self.events:
            is_present = False
            for var_name,value in evidence:
                if event.name == var_name:
                    is_present = True
                    break
            if not is_present:    
                hidden.append(event)

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




