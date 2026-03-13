# pyomo
'''
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
