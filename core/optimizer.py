import pandas as pd
from core.predictor import AttritionPredictor

class HROptimizer:
    def __init__(self):
        self.predictor = AttritionPredictor()

    def optimize(self, df, budget, max_promotion, max_no_overtime):
        # 1. 원본 데이터 퇴사 확률 계산
        df_opt = df.copy()
        base_prob = []
        for i in range(len(df_opt)):
            prob = self.predictor.predict_single(df_opt.iloc[i:i+1])
            base_prob.append(prob if prob is not None else 0.0)
        
        df_opt['현재_위험도'] = base_prob

        high_risk_df = df_opt[df_opt['현재_위험도'] > 0.9].copy()

        action_candidates = []

        # 2. what-if 시나리오 
        for _, row in high_risk_df.iterrows():
            base_p = row['현재_위험도']
            emp_name = row.get('이름', 'Unknown')

            # 야근 면제(초과근무 Yes인 사람만)
            if row.get('초과근무여부') == 'Yes':
                sim_row = row.copy() 
                sim_row['초과근무여부'] = 'No'
                new_p = self.predictor.predict_single(sim_row.to_frame().T)
                drop_p = base_p - new_p
                if drop_p > 0:
                    action_candidates.append({
                        '이름': emp_name, '현재_위험도': base_p, '조치후_위험도': new_p,
                        '액션': '야근 면제', '비용_예산': 0, '비용_승진': 0, '비용_야근면제' : 1, '효과': drop_p, 'ROI': drop_p
                    })

            # 승진 시나리오
            if '직급' in row and row['직급'] < 5:
                sim_row = row.copy()
                sim_row['직급'] += 1
                if '마지막승진후경과년수' in sim_row:
                    sim_row['마지막승진후경과년수'] = 0

                new_p = self.predictor.predict_single(sim_row.to_frame().T)
                drop_p = base_p - new_p
                if drop_p > 0:
                    action_candidates.append({
                        '이름': emp_name, '현재_위험도': base_p, '조치후_위험도': new_p,
                        '액션': '직급 승진', '비용_예산': 0, '비용_승진': 1, '효과': drop_p, 'ROI': drop_p
                    })

            # 급여 인상 시나리오
            if '월급' in row:
                sim_row = row.copy()
                sim_row['월급'] = sim_row['월급'] * 1.10
                if '급여인상률' in sim_row:
                    sim_row['급여인상률'] = min(sim_row['급여인상률'] + 10, 25) # 최대 25%로 제한

                new_p = self.predictor.predict_single(sim_row.to_frame().T)
                drop_p = base_p - new_p

                # 비용 계산 (월급 단위를 임의로 조정. 데이터셋 단위에 맞춰 수정 필요)
                # 예: 월급 * 10% * 12개월
                cost = (row['월급'] * 0.10) * 12 
                if drop_p > 0 and cost > 0:
                    action_candidates.append({
                        '이름': emp_name, '현재_위험도': base_p, '조치후_위험도': new_p,
                        '액션': '연봉 10% 인상', '비용_예산': cost, '비용_승진': 0, '효과': drop_p, 'ROI': drop_p / cost
                    })
                    
        # 3. ROI 기준으로 내림차순 정렬
        candidates_df = pd.DataFrame(action_candidates)
        if candidates_df.empty:
            return pd.DataFrame(), 0.0, 0.0
        
        candidates_df = candidates_df.sort_values(by=['ROI','효과'], ascending=[False, False])

        # 4. 최적 할당(greedy)
        selected_actions = []
        optimized_names = set() # 한 명당 하나의 액션만 허용

        current_budget = budget
        current_promotion = max_promotion
        current_no_overtime = max_no_overtime

        total_prob_drop = 0.0

        for _, act in candidates_df.iterrows():
            name = act['이름']
            if name in optimized_names:
                continue # 이미 혜택이 선택된 직원은 건너뜀

            action_type = act['액션']
            can_apply = False
            cost_text = ""

            #액션 종류별로 TO체크 및 차감
            if action_type == '야근 면제':
                if current_no_overtime > 0:
                    current_no_overtime -= 1
                    can_apply = True
                    cost_text = "야근 면제 TO 1명"
            
            elif action_type == '직급 승진':
                if current_promotion > 0:
                    current_promotion -= 1
                    can_apply = True
                    cost_text = "승진 TO 1명"
            
            elif action_type == '연봉 10% 인상':
                 cost = act['비용_예산']
                 if current_budget >= cost:
                     current_budget -= cost
                     can_apply = True
                     cost_text = f"{cost:,.0f} 만원"

            if can_apply:
                total_prob_drop += act['효과']

                selected_actions.append({
                    "이름": name,
                    "현재 위험도": f"{act['현재_위험도']*100:.1f}%",
                    "추천 액션": act['액션'],
                    "투입 비용(예상)": cost_text,
                    "조치 후 예상 위험도": f"⬇️{act['조치후_위험도']*100:.1f}%"
                })
                optimized_names.add(name)

            
                
        result_df = pd.DataFrame(selected_actions)
        return  result_df, total_prob_drop, (len(df_opt)) # 추천 목록, 총 하락한 확률합, 전체 인원수


    