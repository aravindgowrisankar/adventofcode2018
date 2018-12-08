#!/usr/bin/env python
import sys

def build_graph(graph,
                vertices=[],
                input="Step R must be finished before step X can begin."):

    words=input.split()
    start=ord(words[1][0])-ord("A")
    end=ord(words[7][0])-ord("A")
    #print "start",start,"end",end
    graph[start][end]=1
    if start not in vertices:
        vertices.append(start)
    if end not in vertices:
        vertices.append(end)
    return graph,vertices

def display(graph):
    for x in  graph:
        print x

def print_vertices(vertices):
    for x in  vertices:
        print chr(x+65),

def in_degree(graph,vertex):
    degree=0
    for v in range(26):
        if graph[v][vertex]==1:
            degree+=1
    return degree

def neighbors(graph,vertex):
    "Return list of neighbors"
    n=[]
    for v in range(26):
        if graph[vertex][v]==1:
            n.append(v)
    return n

def comparison_criteria(graph,vertex):
    """ comparison criteria: Use the in-degree.
    if two vertices have same in-degree, prioritize the lower vertex(alphabetical order) """
    return (in_degree(graph,vertex),vertex)

def is_requirement_met(graph,vertices,vertex,visited=[]):
    for req in vertices:
        if graph[req][vertex]==1:
            if req not in visited:
                return False
    return True

def next_vertex(graph,vertices,visited=[]):
    candidates=set(vertices)-set(visited)
    requirements_met=[v for v in candidates if is_requirement_met(graph,vertices,v,visited)]
    return min(requirements_met)

def solve_basic(graph,vertices):
    answer=[]
    visited=[]
    for i in range(len(vertices)):
        #print "in degree of ",chr(vertex+65),in_degree(graph,vertex)
        v=next_vertex(graph,vertices,visited)
        #print "visited",v
        visited.append(v)
        answer.append(chr(v+65))
    return answer

def simulate_time_passing(workers):

    for worker in workers:
        if worker["task"] is not None:
            worker["remaining"]-=1#reduce time remaining by 1 
    
    return workers

def get_completed_tasks(workers):
    completed_tasks=[]
    for worker in workers:
        if worker["remaining"]==0 and worker["task"] is not None:
            completed_tasks.append(worker["task"])
            worker["task"]=None
    return completed_tasks

def get_next_free_worker(workers):
    #print "Get next free worker: workers",workers
    for i in range(len(workers)):
        if workers[i]["task"] is None:
            return i
    return None

def next_vertex_advanced(graph,vertices,workers,visited=[]):
    candidates=set(vertices)-set(visited)

    requirements_met=[v for v in candidates if is_requirement_met(graph,vertices,v,visited)]

    current_jobs=[worker["task"] for worker in workers if worker["task"] is not None]

    new_jobs=set(requirements_met)-set(current_jobs)

    #print "Requirements met",requirements_met
    jobs_assigned=0

    for next_job in new_jobs:
        next_free_worker=get_next_free_worker(workers)
        if next_free_worker is not None:
            workers[next_free_worker]["task"]=next_job
            workers[next_free_worker]["remaining"]=next_job+61#time in seconds=ordinal position+1
            jobs_assigned+=1

    return workers

def solve_advanced(graph,vertices,num_workers=2):
    answer=[]
    visited=[]
    unexplored=list(vertices) #copy
    time=0
    workers=[]

    for i in range(num_workers):
        #None means worker is available
        #Track remaining seconds on job
        workers.append({"task":None,
                        "remaining":0})

    while (len(unexplored)>0):
        #print "in degree of ",chr(vertex+65),in_degree(graph,vertex)

        workers=next_vertex_advanced(graph,vertices,workers,visited)

        answer.append([time,[dict(w) for w in workers],list(visited)])#copies
        #simulate time passing 

        workers=simulate_time_passing(workers)
        
        completed_tasks=get_completed_tasks(workers)

        for completed in completed_tasks:
            visited.append(completed)

        time+=1
        unexplored=set(vertices)-set(visited)
    answer.append([time,[dict(w) for w in workers],list(visited)])#copies
    return answer

SIMPLE=False
    
if "__main__"==__name__:
    graph=[[0 for i in range(26)] for j in range(26)]
    vertices=[]
    while True:
        line=sys.stdin.readline()
    
        if not line:
            break
        graph,vertices=build_graph(graph,vertices,line)

    print "Finished loading graph with vertices: "
    print_vertices(vertices)
    display(graph)

    if SIMPLE:
        visit_list=solve_basic(graph,vertices)
        print "Answer=","".join(visit_list)
    else:
        answer=solve_advanced(graph,vertices,5)
        for t,ws,v in answer:
            print "Time",t,
            for w in ws:
                if w["task"] is None:
                    print ".",
                else:
                    print chr(w["task"]+65),
            print_vertices(v)
            print
        print "Time to solve",t

