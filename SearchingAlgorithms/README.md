# Uninformed Searching Algorithms
Uninformed Searching Algorithms are strategies where the is no full information is provided. We only know if it is the goal state by expanding and reaching that state.
The different type of algorithms are differentiated based on the order in which they are expand the states.

## 1. Depth first search (DFS)
HOW: Always expands the deepest node of the current frontier node.

DATA STRUCTURE: LIFO - Stack.

NOTE:


## 2. Breadth first search (BFS)
HOW: Here the root node is expanded first and then all the successor of the root node are expanded next. 

DATA STRUCTURE: FIFO - Queue. 

NOTE:
1. Here the goal test (testing whether the state is a goal state or not) is tested when generating the new state, rather than when selecting.
2. 