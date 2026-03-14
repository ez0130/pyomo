import sys
sys.executable
import traci
import pyomo.environ as aml

# 1. 시뮬레이션 시작 (GUI 모드로 실행)
# 가상환경이 활성화된 상태여야 함
sumo_cmd = ["sumo-gui", "-c", "intersection.sumocfg"]
traci.start(sumo_cmd)

step = 0
try:
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()  # 1초 전진
        
        # 2. 특정 주기(예: 30초)마다 최적화 수행
        if step % 30 == 0:
            # 데이터 수집: 각 방향의 대기 차량 수 (Halting Number)
            # 'N2C_0'은 북쪽에서 중앙으로 들어오는 0번 차로 아이디야
            q_n = traci.lane.getLastStepHaltingNumber("N2C_0")
            q_s = traci.lane.getLastStepHaltingNumber("S2C_0")
            
            print(f"Time {step}: 북쪽 대기 {q_n}대, 남쪽 대기 {q_s}대")
            
            # 여기에 어제 만든 Pyomo 최적화 로직 호출
            # 예: g_opt = solve_optimization(q_n, q_s)
            
            # 3. 신호등 시간 변경 (필요시)
            # traci.trafficlight.setPhaseDuration("center", 30)
            
        step += 1
except Exception as e:
    print(f"에러 발생: {e}")
finally:
    traci.close()