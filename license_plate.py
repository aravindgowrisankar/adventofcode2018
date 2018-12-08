#!/usr/bin/env python
import sys

class Node(object):
    def __init__(self):
        self.metadata =[]
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def set_metadata(self, metadata):
        self.metadata=metadata

    def get_metadata_sum(self):
        return sum(self.metadata)
        
    def get_complex_metadata_sum(self):
        if len(self.children)==0:
            return sum(self.metadata)
        else:
            s=0
            for x in self.metadata:
                if x<=len(self.children):
                    s+=self.children[x-1].get_complex_metadata_sum()
            return s

def parse(node,data):
    """return a child node with the populated data"""
    num_children=data.pop(0)
    num_metadata=data.pop(0)

    for i in range(num_children):
        child=Node()
        child=parse(child,data)
        node.add_child(child)

    metadata=[]
    for j in range(num_metadata):
        metadata.append(data.pop(0))

    node.set_metadata(metadata)
    return node

def metadata_sum(root):
    node=root
    s=node.get_metadata_sum()
    for child in root.children:
        s+=metadata_sum(child)
    return s

if "__main__"==__name__:
    text=sys.stdin.readline()
    data=[int(x) for x in text.split()]
    print data
    root=Node()
    parse(root,data)
    print "sum",metadata_sum(root)
    print "complex sum",root.get_complex_metadata_sum()
