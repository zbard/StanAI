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

def two_cancer_example():
    C_prob_table = [0.99,0.01]
    node1 = Event("C",[],C_prob_table)
    Test_prob_table = [0.8,0.2,0.1,0.9]
    node2 = Event("T1",[node1],Test_prob_table)
    node3 = Event("T2",[node1],Test_prob_table)
    bn = Bayes_net([node1,node2,node3])

    query = [("C",True)]
    evidence = [("T1",True),("T2",True)]
    print enumeration_custom(query,evidence, bn)
    
    evidence = [("T1",True),("T2",False)]
    print enumeration_custom(query,evidence, bn)

def hw2_bayes_net():
    A_prob_table = [0.5,0.5]
    node1 = Event("A",[],A_prob_table)
    X_prob_table = [0.4,0.6,0.8,0.2]
    node2 = Event("X1",[node1],X_prob_table)
    node3 = Event("X2",[node1],X_prob_table)
    node4 = Event("X3",[node1],X_prob_table)
    bn = Bayes_net([node1,node2,node3,node4])

    query = [("A",True)]
    evidence = [("X1",True),("X2",True),("X3",False)]
    print enumeration_custom(query,evidence, bn)

    query = [("X3",True)]
    evidence = [("X1",True)]
    print enumeration_custom(query,evidence, bn)

sanity_test()
two_cancer_example()
hw2_bayes_net()

