#  SKN25-2nd-5Team
#  HR Attrition Prediction

직원 데이터를 기반으로 퇴사 여부를 예측하는 머신러닝 Sass 서비스!

---

## 팀소개
| 김홍익 | 이채림 | 이한솔 | 임하영 | 최유림 |
|:--:|:--:|:--:|:--:|:--:|
|  <img src="https://github.com/user-attachments/assets/c65b8359-978c-49e1-888a-32bb9269880e" width="150" height="150"/> |  <img src="https://github.com/user-attachments/assets/05119932-d032-40e0-b5ef-9216c43e7e47" width="150" height="150"/> |  <img src="https://github.com/user-attachments/assets/4bec8b83-d36e-456a-8e99-b0f25fe9c8bc" width="150" height="150"/> |  <img src="https://github.com/user-attachments/assets/3a535abf-69be-4aba-a9b5-12ccf656b82e" width="150" height="150"/> |  <img src="https://github.com/user-attachments/assets/5f1f4e0c-a32d-4c10-9dcc-932ce4aff56e" width="150" height="150"/> |
| `@skidroww` | `@chaechae18` | `@sol1021` | `@pureunsaerok` | `@yulim8813`|
| 공통 레이아웃 컴포넌트<br>dashboard 페이지<br>최적화 솔루션 페이지<br>전처리 및 모델링 | 퇴사 위험 예측 및 분석 페이지<br>직원 관리 및 수정 페이지<br> 맞춤형 시뮬레이션 페이지<br>DB 설계 | 핵심 인재 관리 페이지<br>DB 설계<br>ERD | 로그인 페이지<br>회원가입 페이지<br>발표준비 | 데이터 전처리<br>모델링<br>발표준비 |

##  프로젝트 개요

프로젝트: 데이터 기반 선제적 인재 유지 솔루션

프로젝트 성격: 머신러닝(ML) 기반의 퇴사 예측 알고리즘과 최적화 시뮬레이션을 결합한 기업용 HR SaaS 프로그램입니다. 단순히 퇴사 가능성을 점치는 것을 넘어, 인사 운영의 효율성을 극대화하기 위한 구체적인 액션 아이템(Action Item)을 제시합니다.

핵심 가치: 예측(Predict)25개 이상의 다각도 인사 데이터를 분석하여 개인별 퇴사 확률 도출

최적화(Optimize): 한정된 인사 예산 내에서 퇴사율을 낮추기 위한 최적의 처우 개선 시나리오 시뮬레이션

실행(Execute): 특정 직원을 구제하기 위한 최소 비용 산출 및 우선순위 리포트 제공

---

## 🧠 문제 정의

1. 배경 (Context)
* 현대 기업 환경에서 핵심 인재의 이탈은 단순히 채용 비용의 발생을 넘어, 조직의 지식 자산 손실과 남은 팀원들의 사기 저하라는 치명적인 결과를 초래합니다. 하지만 기존의 인사 관리는 "이미 사직서를 낸 뒤에야" 대응하는 사후 약방문식 처방에 그치고 있습니다.

2. 핵심 문제 (Core Problems)
* 예측의 부재 (Lack of Foresight): 어떤 직원이 어떤 요인(야근, 낮은 급여, 승진 누락 등)으로 인해 이탈 위험이 높아졌는지 데이터에 기반해 판단하기 어렵습니다.
* 자원의 희소성 (Resource Scarcity): 모든 직원의 연봉을 대폭 올리거나 모두를 승진시킬 수는 없습니다. 한정된 예산 안에서 '가장 가성비 높은 처방'이 누구에게 필요한지 모릅니다.
* 처방의 불확실성 (Uncertainty of Action): "연봉을 5% 올리는 것이 나을까, 아니면 직급을 올려주는 것이 퇴사 방지에 더 효과적일까?"에 대한 시뮬레이션 데이터가 없습니다.

3. 기대효과
* **비용 측면**: 채용 및 온보딩 비용 절감, 인사 예산 ROI 최적화
* **운영 측면**: 퇴사율 구제를 위한 최적의 처방 시나리오 확보
* **조직 측면**: 핵심 인재 이탈 방지를 통한 지식 자산 보호 및 팀 사기 유지
---

## 🛠 사용 기술

### 🖥 Frontend
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
* **Streamlit**: 파이썬 기반 웹 UI 프레임워크 (인터랙티브 대시보드 구현)
* **Plotly**: 데이터 시각화 라이브러리 (퇴사율 변화 및 인사 지표 차트 구현)

### ⚙️ Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
* **Python**: 시스템 메인 로직 및 처우 개선 최적화 알고리즘 엔진
* **Pandas**: 인사 데이터(25개 지표) 전처리 및 데이터 분석
* **NumPy**: 대규모 인원 대상 퇴사 확률 시뮬레이션 및 수치 연산

### 🗄 Database
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLALCHEMY-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
* **MySQL**: 직원 정보, 면담 기록, 처우 개선 이력 관리
* **SQLAlchemy**: Python-DB 간 안정적인 ORM 및 커넥션 관리

### 🧠 Deep Learning / ML
![Scikit Learn](https://img.shields.io/badge/SCIKIT%20LEARN-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white&)
* **Scikit-learn, XGBoost**: 퇴사 예측 분류(Classification) 모델 학습 및 추론
* **Pickle / Joblib**: 학습 모델(`model.pkl`) 및 피처 규격(`feature_names.pkl`) 직렬화
* **Optimization Logic**: 급여 인상 및 승진 시나리오별 퇴사율 변화 산출 알고리즘

---
## 🚀 핵심 기능 (Key Features)
<p align="center">
<img src="https://github.com/user-attachments/assets/86c0d6df-7c3d-4bf8-bf66-d43ec49a2d2d">
</p>
<p align="center">
<img src="https://github.com/user-attachments/assets/d914e69b-2868-4b67-af1d-fd46f001d374">
</p>
<p align="center">
<img src="https://github.com/user-attachments/assets/5182ada5-163f-424b-865d-9725ed7921e9">
</p>

* **실시간 퇴사 위험도 예측**: 사내 인사 데이터를 업로드하여 직원별 퇴사 확률을 즉각적으로 도출합니다.
<p align="center">
<img src="https://github.com/user-attachments/assets/3b71dfea-7640-4d93-9142-865ebec3f61d">
</p>

* **사원 관리**: 각 직원을 추가 입력하고 수정합니다.
<p align="center">
<img src ="https://github.com/user-attachments/assets/605e32e4-066c-4831-96cd-dfebf8f57035">
</p>

* **급여 인상 시뮬레이션**: 특정 인원의 퇴사율을 줄일 수 있는 최적의 시뮬레이션과 급여인상, 승진했을 때 퇴사 확률이 어떻게 변화하는지 실시간 피드백을 제공합니다.
<p align="center">
<img src ="https://github.com/user-attachments/assets/32de6f20-d43a-479c-bb37-439c42ce6a34">
</p>

* **개인별 맞춤형 솔루션**: 각 직원을 안전권으로 이동시키기 위한 최적의 추가 비용을 제안합니다.
<p align="center">
<img src ="https://github.com/user-attachments/assets/91f4e5f7-c087-4395-874b-15c69a13cdfe">
</p>

* **핵심인재 관리시스템**: 각 직원들의 성과등급에 따라 면담 우선순위와 면담내용을 저장합니다.
<p align="center">
<img src ="https://github.com/user-attachments/assets/69737036-e34b-4252-a8ae-99c01be0542a">
</p>

## 📂 프로젝트 구조
```
HR_Analytics_SaaS/
│
├── [main.py](http://main.py/)                # 앱 실행 진입점 (python [main.py](http://main.py/))
├── [app.py](http://app.py/)                 # 앱 설정 및 라우팅 (Controller 역할)
├── requirements.txt       # 의존성 패키지 (xgboost, shap, streamlit 등)
│
├── models/                # [저장소] 학습된 모델 파일 저장
│   ├── best_model.pkl     # 학습된 분류 모델 (XGBoost/RandomForest)
│   ├── scaler.pkl         # 데이터 전처리용 스케일러
│   └── explainer.pkl      # SHAP Explainer 객체 (선택)
│
├── core/                  # [핵심 로직] UI와 독립적인 순수 파이썬 로직 (The Brain)
│   ├── init.py
│   ├── [loader.py](http://loader.py/)          # 모델 로드 및 캐싱 (@st.cache_resource)
│   ├── [predictor.py](http://predictor.py/)       # 퇴사 확률 예측 함수
│   ├── [explainer.py](http://explainer.py/)       # SHAP 값 계산 및 시각화 데이터 생성
│   └── [optimizer.py](http://optimizer.py/)       # 예산 대비 퇴사율 최적화 알고리즘
│
├── ui/                    # [화면] 사용자에게 보여지는 페이지들 (View)
│   ├── init.py
│   ├── [sidebar.py](http://sidebar.py/)         # 사이드바 메뉴
│   ├── [dashboard.py](http://dashboard.py/)       # 대시보드 (전체 현황)
│   ├── [prediction.py](http://prediction.py/)      # 개별/일괄 예측 및 데이터 업로드
│   ├── [simulation.py](http://simulation.py/)      # What-if 시뮬레이션 (연봉 인상 등)
│   └── [optimization.py](http://optimization.py/)    # 최적화 솔루션 페이지
│   └── [hr_retention.py](http://optimization.py/)    # 핵심인재 관리(면담내용 작성)
│
└── utils/                 # [도구] DB 연결, 데이터 가공 등
├── [db.py](http://db.py/)              # DB 연결 (필요 시)
└── data_loader.py     # CSV 파일 처리, 전처리 함수
```
---
## ERD
<div align="left"> <img width="1307" height="1397" alt="Image" src="https://github.com/user-attachments/assets/69598209-a798-4401-a6d8-ef4e85c61b91" width="10%" height="10%" /> </div>

## 데이터 출처
본 프로젝트는 다음과 같은 데이터를 활용하여 구성되었습니다.

**HR Analytics Dataset**
<div align="left"><img src="https://github.com/user-attachments/assets/dbe14c51-6495-459c-9a45-a01c65f630dc" width="50%" height="50%"/></div><br>
Kaggle에서 제공하는 <a href="https://www.kaggle.com/datasets/anshika2301/hr-analytics-dataset/data" target="_blank">[인사팀 분석 데이터셋]</a>를 활용하였습니다.

---

## 한줄 회고

> <img src="https://github.com/user-attachments/assets/c65b8359-978c-49e1-888a-32bb9269880e"  width="20" style="vertical-align:middle;" />&nbsp;**김홍익** : 직접 머신러닝 모델을 만들고 그 모델을 가지고 서비스를 만들어 보는 과정에서 많은 공부와 경험이 되었습니다. 부족한 점도 많이 알게되어 앞으로 공부하는데 많은 도움이 될 것 같습니다.
>
><img src="https://github.com/user-attachments/assets/05119932-d032-40e0-b5ef-9216c43e7e47" width="20" style="vertical-align:middle;" />&nbsp;**이채림** : ...
>
> <img src="https://github.com/user-attachments/assets/4bec8b83-d36e-456a-8e99-b0f25fe9c8bc"  width="20" style="vertical-align:middle;" />&nbsp;**이한솔** : ...
>
> <img src="https://github.com/user-attachments/assets/3a535abf-69be-4aba-a9b5-12ccf656b82e" width="20" style="vertical-align:middle;" />&nbsp;**임하영** : ...
>
> <img src="https://github.com/user-attachments/assets/5f1f4e0c-a32d-4c10-9dcc-932ce4aff56e" width="20" style="vertical-align:middle;" />&nbsp;**최유림** : ...

















