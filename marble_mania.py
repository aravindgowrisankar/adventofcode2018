#!/usr/bin/env python
import collections

class Marbles(object):
    def __init__(self):
        self.head=0
        self.data=[0]
    
    def get_head(self):
        return self.head

    def update_head(self,special_case=False):
        current_size=len(self.data)
        if special_case:
            self.head=(self.head-7)%current_size
            return
        if current_size==1:
            self.head=1
        else:
            i=self.head+1
            j=self.head+2
            if i>=current_size:
                i=i%current_size
                j=j%current_size
            self.head=j
            
    def add(self,x):
        self.data.insert(self.head,x)

    def get_data(self):
        return self.data

    def remove(self):
        """Remove item at current head and return it."""
        return self.data.pop(self.head)

    def play(self,x):
        score=0
        if x%23!=0:
            self.update_head()
            self.add(x)
        else:
            self.update_head(special_case=True)
            score=x
            score=score+self.remove()
        return score


class FancyMarbles(Marbles):
    """Same game play as Marbles with a fancier deque datastructure underneath."""
    def __init__(self):
        self.data=collections.deque([0])

    def update_head(self,special_case=False):
        if special_case:
            for i in range(7):
                self.data.rotate()
        else:
            self.data.rotate(-1)

    def add(self,x):
        self.data.append(x)

    def remove(self):
        y=self.data.pop()
        self.data.rotate(-1)
        return y


SIMPLE=False
NUM_PLAYERS=9#473
LAST_MARBLE=25#7090400
    
scores=[0.0 for i in range(NUM_PLAYERS)]

if SIMPLE:
    n=Marbles()
else:
    n=FancyMarbles()

for i in xrange(1,LAST_MARBLE+1):
    current_player=(i-1)%NUM_PLAYERS
    scores[current_player]+=n.play(i)
    #print n.get_data()
    
print "Scores",scores
print "Maximum score",max(scores)
    


