import csv
import networkx as nx
import matplotlib.pyplot as plt
import copy 


class Node:
    def __init__(self, data):
        self.data = data
        self.selected = False
        self.level=None
        self.clusterhead= None
        self.C_Intra=0
        self.C_Inter=0
    def IsSelected(self):
        return self.selected

def insertion(x: Node,y: Node):
    chl=[]
    if not x.IsSelected() and not y.IsSelected():
        chl.append(x.data)
        x.clusterhead=x.data
        x.level=0
        y.level=1
        y.clusterhead=x.data
        x.C_Intra=1
        y.C_Intra=1
        x.selected=True
        y.selected=True
        members_list[get_cluster_head(x.data)].append(y.data)
    elif not x.IsSelected() or not y.IsSelected():
        if not x.IsSelected():
            if(y.level<=l-1):
                x.level=y.level+1
                x.C_Intra=1
                y.C_Intra+=1
                x.clusterhead=y.data
                x.selected=True
                members_list[get_cluster_head(y.data)].append(x.data)
            else:
                chl.append(y.data)
                y.clusterhead=y.data
                y.level=0
                x.level=1
                x.clusterhead=y.data
                y.C_Inter=y.C_Intra
                x.C_Intra=1
                y.C_Intra=1
                x.selected=True
                members_list[get_cluster_head(y.data)].append(x.data)
        else:
            if(x.level<=l-1):
                y.level=x.level+1
                y.C_Intra=1
                x.C_Intra+=1
                y.clusterhead=x.data
                y.selected=True
                members_list[get_cluster_head(x.data)].append(y.data)
            else:
                chl.append(x.data)
                x.clusterhead=x.data
                x.level=0
                y.level=1
                y.clusterhead=x.data
                x.C_Inter=x.C_Intra
                y.C_Intra=1
                x.C_Intra=1
                y.selected=True
                members_list[get_cluster_head(x.data)].append(y.data)
    else:
        if(x.clusterhead==y.clusterhead):
            y.C_Intra+=1
            x.C_Intra+=1
        else:
            x.C_Inter+=1
            y.C_Inter+=1
    return chl



# MAIN FUNCTION

W_temp=0
W=4
l=3
theta=0.5
cluster_list_heads=[]
number_of_nodes=62
node_list=[None]*number_of_nodes
members_list=[[] for _ in range(number_of_nodes)]

def detachbility_index(x,memberslist,nodelist):
    members=memberslist[x]
    if x not in members:
        members.append(x)
    intra=0
    inter=0
    for member in members:
        intra+=nodelist[member].C_Intra
        inter+=nodelist[member].C_Inter
    return intra/(intra+inter)


def get_cluster_head(x: int):
    head = node_list[x].clusterhead
    while(head != node_list[head].clusterhead):
        head=node_list[head].clusterhead
    return head

def get_elements_with_max_frequency(arr):
    freq = {}
    for i in arr:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1

    max_freq = max(freq.values())

    result = [k for k, v in freq.items() if v == max_freq]

    return result

def merge(i,z):
    ndlst=copy.deepcopy(node_list)
    memlst=copy.deepcopy(members_list)
    clslst=copy.deepcopy(cluster_list_heads)
    z_lst=members_list[z]
    z_lst.append(z)
    i_lst=members_list[i]
    i_lst.append(i)
    for node in z_lst:
        neigbours = g[node]
        for neigbour in neigbours:
            if neigbour in i_lst:
                ndlst[node].C_Inter-=1
                ndlst[node].C_Intra+=1
    for node in i_lst:
        neigbours = g[node]
        for neigbour in neigbours:
            if neigbour in z_lst:
                ndlst[node].C_Inter-=1
                ndlst[node].C_Intra+=1
    memlst[i]=list(set(z_lst) | set(i_lst))
    memlst[z]=[]
    clslst.remove(z)
    return ndlst,memlst,clslst
    
    
def detachind(i,z):
    ndlist,memlist,clslst=merge(i,z)
    return detachbility_index(i,memlist,ndlist)
dataset="dolphins.csv" # The name of dataset
g=nx.Graph()
with open(dataset, mode ='r')as file:
    csvFile = csv.DictReader(file)
    for line in csvFile:
        s=int(line['Source'])-1
        t=int(line['Target'])-1
        g.add_edge(s,t)
        if node_list[s]==None:
            node_list[s]=Node(s)
        if node_list[t]==None:
            node_list[t]=Node(t)
        cluster_list_heads=list(set(cluster_list_heads) | set(insertion(node_list[s],node_list[t])))
        W_temp+=1
        if(W_temp==W):
            for Cz in cluster_list_heads:
                if(detachbility_index(Cz, members_list, node_list)<theta):
                    NE=members_list[Cz] #line 13
                    CS=get_elements_with_max_frequency(NE) #line 14,15,16
                    MID= float('-inf')
                    for head in CS:
                        if head!=Cz:
                            TID=detachind(head,Cz)-detachbility_index(head,members_list,node_list)
                            if(TID>MID):
                                MID=TID
                                t=head
                    node_list,members_list,cluster_list_heads=merge(t,Cz)
            W_temp=0


print(members_list)
print(cluster_list_heads)
nodes_colors = [0]*number_of_nodes
i=1
for head in cluster_list_heads:
    nodes_colors[head]=i
    for node in members_list[head]:
        nodes_colors[node]=i
    i+=1
nx.draw_networkx(g,with_labels=True,node_color=nodes_colors,font_size=8)
plt.savefig("graph.png")


