'''
1.Scenario setup 
#     Route(Nodes): Manufacture Factory - > Warehouse - > Retailer
#     Goal: Minimize Transportation Cost
#     Factories : 2 places ( Constraints : produce limit)
#     Warehouse : 3 places ( Constraints : storage and pass capacity limit)
#     Retailer : 5 places ( Fixed Demand )
#     Cost : transport cost for each edge
2. Mathmatical Model
#    Decision Variable:
#     X(i,j) : Package amount moving from Factory i to Storage j
#     Y(j,k) : Package amount moving from Storage j to Retailer k
#    Objective Function:
#     Minimize all route total cost ( Package amount * cost to travel ) 
#     # Objective: min ΣΣ (C_i,j * x_i,j) + ΣΣ (C_j,k * y_j,k)
#    Constraints: 
#     Supply limit : factory outbound amount <= Manufacturing Capacity
#     Demand limit : retailer stock amount >= Demanding amount
#     Flow Conservation : Total package amount entered storage = Total package left storage
'''
from pyomo.environ import *

# 1. 모델 초기화
model = ConcreteModel(name="SupplyChainOptimization")

# 2. Set 설정 (Index)
model.I = Set(initialize=['Factory1', 'Factory2'], doc='Factories')
model.J = Set(initialize=['WH1', 'WH2', 'WH3'], doc='Warehouses')
model.K = Set(initialize=['Retail1', 'Retail2', 'Retail3', 'Retail4', 'Retail5'], doc='Retailers')

# 3. Parameter 설정 (Data)
# 생산 용량 (Capacity)
supply = {'Factory1': 500, 'Factory2': 500}
# 소매점 수요 (Demand)
demand = {'Retail1': 100, 'Retail2': 150, 'Retail3': 200, 'Retail4': 100, 'Retail5': 150}

# 단위당 운송 비용 (Cost) - 예시 데이터
costs_factory_wh = {
    ('Factory1', 'WH1'): 2, ('Factory1', 'WH2'): 4, ('Factory1', 'WH3'): 5,
    ('Factory2', 'WH1'): 3, ('Factory2', 'WH2'): 2, ('Factory2', 'WH3'): 6
}
costs_wh_retail = {
    ('WH1', 'Retail1'): 10, ('WH1', 'Retail2'): 7, ('WH1', 'Retail3'): 4, ('WH1', 'Retail4'): 2, ('WH1', 'Retail5'): 8,
    ('WH2', 'Retail1'): 1,  ('WH2', 'Retail2'): 4, ('WH2', 'Retail3'): 7, ('WH2', 'Retail4'): 3, ('WH2', 'Retail5'): 5,
    ('WH3', 'Retail1'): 5,  ('WH3', 'Retail2'): 3, ('WH3', 'Retail3'): 2, ('WH3', 'Retail4'): 6, ('WH3', 'Retail5'): 9
}

# 4. 결정 변수 (Variables)
model.x = Var(model.I, model.J, domain=NonNegativeReals) # Factory -> WH
model.y = Var(model.J, model.K, domain=NonNegativeReals) # WH -> Retailer


# 5. 목적 함수 (Objective)
def obj_rule(model):
    transport_cost1 = sum(costs_factory_wh[i, j] * model.x[i, j] for i in model.I for j in model.J)
    transport_cost2 = sum(costs_wh_retail[j, k] * model.y[j, k] for j in model.J for k in model.K)
    return transport_cost1 + transport_cost2
model.objective = Objective(rule=obj_rule, sense=minimize)

# 6. 제약 조건 (Constraints)
# (1) Supply Constraint
def supply_rule(model, i):
    return sum(model.x[i, j] for j in model.J) <= supply[i]
model.supply_con = Constraint(model.I, rule=supply_rule)

# (2) Demand Constraint
def demand_rule(model, k):
    return sum(model.y[j, k] for j in model.J) >= demand[k]
model.demand_con = Constraint(model.K, rule=demand_rule)

# (3) Flow Conservation (In = Out at Warehouse)
def flow_rule(model, j):
    inflow = sum(model.x[i, j] for i in model.I)
    outflow = sum(model.y[j, k] for k in model.K)
    return inflow == outflow
model.flow_con = Constraint(model.J, rule=flow_rule)

# 7. 풀이 (Solver)
# 환경에 설치된 solver 지정 (예: glpk, CBC, gurobi)
solver = SolverFactory('glpk')
results = solver.solve(model)

# 8. 결과 출력
print(f"Total Cost: {model.objective()}")
for i in model.I:
    for j in model.J:
        if model.x[i, j].value > 0:
            print(f"Flow {i} -> {j}: {model.x[i, j].value}")

print(model.y.pprint())
print(model.x.pprint())
print(model.I.pprint())
print(model.J.pprint())
print(model.K.pprint())
            


'''

