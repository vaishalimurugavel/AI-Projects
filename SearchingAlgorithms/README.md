# Uninformed Searching Algorithms
Uninformed Searching Algorithms are strategies where the is no full information is provided. We only know if it is the goal state by expanding and reaching that state.
The different type of algorithms are differentiated based on the order in which they are expand the states.

## 1. Depth First Fearch (DFS)
Always expands the deepest node of the current frontier node. 

DATA STRUCTURE: LIFO - Stack.


## 2. Breadth First Search (BFS)
Here the root node is expanded first and then all the successor of the root node are expanded next. 

DATA STRUCTURE: FIFO - Queue. 


## 3. Uniform Cost Search (UCS)
Used for wighted graph, particularly useful when all the weights are different. Is a variant of Dijkstra's Algorithm. 
Similar to BFS, but select the node with the least cost to expand next.

DATA STRUCTURE: FIFO - Priority Queue.

## 4. A* Search Algorithm
