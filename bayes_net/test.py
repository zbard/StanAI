from bayes_net import *


def sanity_test():
    A_prob_table = [.5,.5]
    node1 = Event("A",[],A_prob_table)
    B_prob_table = [.4,.6,.7,.3]
    node2 = Event("B",[node1],B_prob_table)
    bn = Bayes_net([node1,node2])
    query = [("A",True)]
    evidence = [("B",True)]

    print enumeration_custom(query,evidence, bn)


sanity_test()

