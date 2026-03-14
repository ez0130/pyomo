# pyomo
## Core Algorithms of GLPK1. 
#### Primal and Dual Simplex Method
Used for: Solving LP (Linear Programming) problems
Principle: It navigates through the vertices (corners) of the feasible region (a polyhedron formed by constraints) one by one, moving toward the vertex that improves the objective function value the most.
Characteristics: This is a time-tested and highly stable method. GLPK intelligently selects between the 'Primal' and 'Dual' approaches based on the specific structure of the problem to maximize efficiency.

#### 2. Interior Point Method (Primal-Dual Barrier)
Principle: Unlike the Simplex method which moves along the edges, the Interior Point Method cuts across the interior of the feasible region to reach the optimal solution. 
It uses a 'Barrier Function' to navigate from the center toward the optimal direction without touching the boundaries prematurely.
Characteristics: It is often significantly faster than the Simplex method for large-scale problems with tens of thousands of variables. 
GLPK's inclusion of this method makes it highly effective for complex, large-scale network modeling.
#### 3. Branch and Bound Method
Used for: Solving MIP (Mixed Integer Programming) problems
Principle: This algorithm is activated when Integer Constraints are involved (e.g., "We cannot send 0.5 trucks; it must be exactly 1 or 2").LP Relaxation: First, it solves the problem as a standard LP, ignoring the integer requirement (yielding a decimal result like 1.5).
Branching: If the result is a decimal, it creates branches by splitting the search space (e.g., $x \le 1$ and $x \ge 2$).
Bounding: It prunes (cuts off) branches that are proven to be incapable of providing a better solution than the one already found, narrowing down the search.Characteristics: While integer constraints exponentially increase computational complexity, this algorithm efficiently manages the search process by systematically eliminating non-optimal sub-problems.


###1.Scenario setup 
#### Route(Nodes): Manufacture Factory - > Warehouse - > Retailer
#### Goal: Minimize Transportation Cost
#### Factories : 2 places ( Constraints : produce limit)
#### Warehouse : 3 places ( Constraints : storage and pass capacity limit)
#### Retailer : 5 places ( Fixed Demand )
#### Cost : transport cost for each edge
###2. Mathmatical Model
#### Decision Variable:
#### X(i,j) : Package amount moving from Factory i to Storage j
#### Y(j,k) : Package amount moving from Storage j to Retailer k
#### Objective Function:
##### Minimize all route total cost ( Package amount * cost to travel ) 
##### Objective: min ΣΣ (C_i,j * x_i,j) + ΣΣ (C_j,k * y_j,k)
