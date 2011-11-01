from util import Counter
from bayes_net import *


class bag_of_words:
    def __init__(self,classes,k=1,file_suffix=".txt"):
        # k is laplacian smoothing parameter
        # classes is list of class names (strings)
        self.no_of_classes = len(classes)
        self.classes = classes
        self.classes_no = Counter()
        # classes_no is msgs/lines in that class
        self.classes_wc = { }
        # classes_wc is dictionary of counters(which count class vocab)
        self.vocabulary = set([])
        # whole vocab

        for class_name in classes:
            filename = class_name + file_suffix
            f = open(filename,'r')
            no_of_lines = k
            self.classes_wc[class_name] = Counter()
            for line in f:
                no_of_lines += 1
                words = line.split()
                for word in words:
                    self.vocabulary.add(word)
                    self.classes_wc[class_name][word] += 1
            self.classes_no[class_name] = no_of_lines

        for word in self.vocabulary:
            for class_name in classes:
                self.classes_wc[class_name][word] += k


    def create_bayes_net(self):
        all_nodes = []

        prob_table = []
        # insert root possible of taking on multiple vals (classes eg; spam,ham etc)
        for class_name in self.classes:
            prob_true = self.classes_no[class_name] 
            prob_true = float(prob_true) / self.classes_no.totalCount()
            prob_table.append(prob_true)
        
        # Message type is value of node "MSG"
        root = Event("MSG",[],prob_table,self.classes)
        all_nodes.append(root)

        # insert words
        for word in self.vocabulary:
            prob_table = []
            for class_name in self.classes:
                class_vocab = self.classes_wc[class_name]
                prob_true = class_vocab[word]  
                prob_true = float(prob_true) / class_vocab.totalCount()
                prob_false = 1 - prob_true
                prob_table += [prob_false,prob_true]
            node = Event(word,[root],prob_table)
            all_nodes.append(node)

        self.bn =  Bayes_net(all_nodes)

    def probability_of_word(self,word,root_class = None):
        query = [(word,True)]
        if root_class:
            evidence = [("MSG",root_class)]
        else:
            evidence = []
        print enumeration_custom(query,evidence,self.bn)
        
    def probability_of_not_word(self,word,root_class = None):
        # Can simply return 1 - probability_of_word(..)
        query = [(word,False)]
        if root_class:
            evidence = [("MSG",root_class)]
        else:
            evidence = []
        print enumeration_custom(query,evidence,self.bn)
    
    def probability_of_msg(self,wordlist,msg_class):
        evidence = []
        wordlist = set(wordlist)
        for word in wordlist:
            evidence.append((word,True))
        # Shouldn't we ideally for each word not in wordlist 
        # do evidence.append(word,False) ? Assumping simplistic (Thrum) way here.
        query = [("MSG",msg_class)]
        print enumeration_custom(query,evidence,self.bn)

                    
print "Example 1"
example = bag_of_words(["spam","ham"],0)
example.create_bayes_net()
example.probability_of_word("SPORT","spam")
example.probability_of_msg(["SPORT"],"spam")

print "Example 2"
example = bag_of_words(["spam","ham"],1)
example.create_bayes_net()
example.probability_of_msg([],"spam")
example.probability_of_msg([],"ham")
example.probability_of_word("TODAY","spam")
example.probability_of_word("TODAY","ham")


print "Example 3"
example = bag_of_words(["spam","ham"],1)
example.create_bayes_net()
example.probability_of_msg(["TODAY","IS","SECRET"],"spam")


print "HW3 - Q1 and Q2"
example = bag_of_words(["movie","song"],1)
example.create_bayes_net()
example.probability_of_msg([],"movie")
example.probability_of_msg([],"song")
example.probability_of_word("PERFECT","movie")
example.probability_of_word("PERFECT","song")
example.probability_of_word("STORM","movie")
example.probability_of_word("STORM","song")
example.probability_of_msg(["PERFECT","STORM"],"movie")



