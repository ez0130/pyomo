from xml.parsers.expat import model

import traci
import pyomo.environ as aml
from pyomo.environ import SolverFactory

# [A] 최적화 함수 정의 (데이터를 받아 녹색 시간을 반환)
def solve_signal_optimization(q_data, cycle_time=120):
    model = aml.ConcreteModel()
    model.directions = aml.Set(initialize=list(q_data.keys()))
    
    # Param 설정 시 데이터 타입 일치 확인
    model.q = aml.Param(model.directions, initialize=q_data)
    model.s = aml.Param(model.directions, initialize={'N2C': 1800, 'E2C': 1600})
    
    # 결정 변수 (Variable)
    model.g = aml.Var(model.directions, bounds=(10, 100), initialize=30) # 초기값(initialize) 권장
    
    # 제약식: sum(g) + loss <= cycle
    model.con = aml.Constraint(expr= sum(model.g[d] for d in model.directions) + 12 <= cycle_time)
    
    # 목적함수: 지체 최소화
    def obj_rule(model):
        # 분모가 0이 되는 것을 방지하기 위해 g[d]는 위에서 bounds로 10 이상 설정됨
        return sum(model.q[d] / (model.s[d] * model.g[d] / cycle_time) for d in model.directions)
    
    model.obj = aml.Objective(rule=obj_rule, sense=aml.minimize)
    
    # [핵심 수정 부분]
    # SciPy 솔버 호출 시 'method'를 명시하는 것이 안전함
    # 기존: solver = aml.SolverFactory('scipy')
# 수정:
    solver = aml.SolverFactory('ipopt')
    results = solver.solve(model)

    
    # 결과 반환 (딕셔너리 형태로 변환하여 traci에서 사용하기 편하게 함)
    print("최적화 결과:", results)
    
    return {d: aml.value(model.g[d]) for d in model.directions}

# [B] SUMO 실행 및 실시간 루프
traci.start(["sumo-gui", "-c", "intersection.sumocfg"])

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    curr_time = traci.simulation.getTime()

    # 120초(한 주기)마다 최적화 수행
    if curr_time % 120 == 0:
        # 1. 데이터 추출 (각 방향 대기 차량 수)
        current_q = {
            'N2C': traci.lane.getLastStepHaltingNumber("N2C_0"),
            'E2C': traci.lane.getLastStepHaltingNumber("E2C_0")
        }
        
        # 2. Ipopt로 최적 해 계산
        optimal_greens = solve_signal_optimization(current_q)
        
        # 3. 계산된 값을 신호등에 적용 (이게 제어의 핵심!)
        # 북쪽 녹색 신호(Phase 0) 시간을 optimal_greens['N2C']로 설정
        traci.trafficlight.setPhaseDuration("center", optimal_greens['N2C'])
        print(f"Time {curr_time}: 최적화 완료! 북쪽 녹색 시간 {optimal_greens['N2C']:.2f}초")

traci.close()