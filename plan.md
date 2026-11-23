# GangNaengI AI 7day Dev Plan

---

개발기간: 2026.11.21 - 2026.11.27
목표: 치주질환 ML DL 위험 분류 시스템

---

### 기술 스택

| 분야          | 기술                              |
| ------------- | --------------------------------- |
| Language      | Python 3.12                       |
| Data          | NumPy   Pandas   Scikit-learn |
| ML            | Logistic Regression   XGBoost   |
| DL            | PyTorch   MLP                   |
| Visualization | Matplotlib   SHAP               |
| Backend       | FastAPI                           |
| Frontend      | React(Vite)   TypeScript        |
| Deployment    | Docker   Git   GitHub         |

data는 [wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/OHXPER_H.htm?utm_source=chatgpt.com](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/OHXPER_H.htm?utm_source=chatgpt.com) 참고

---

### 폴더 구조

```
GangNaengI_AI/
	ㄴ data/													 데이터셋
    	ㄴ raw/										    NHANES 원본 데이터
        ㄴ processed/									  전처리 된 데이터
  
    ㄴ notebooks										  EDA 및 실행 분석
    	ㄴ 01_eda.ipynb										   데이터 탐색
        ㄴ 02_evaluation.ipynb 								모델 성능 비교
  
    ㄴ ml/												     머신러닝 개발
    	ㄴ train_ml.py					Logistic Regression, XGBoost 학습
  
    ㄴ dl/													   딥러닝 개발
    	ㄴ model.py									 PyTorch MLP 모델 정의
        ㄴ train_dl.py							   		       딥러닝 학습
  
    ㄴ src/										   공통 데이터 처리 및 평가
    	ㄴ preprocessing.py						 라벨 생성 및 데이터 전처리
        ㄴ evaluation.py									성능 평가 함수
  
    ㄴ models/										   학습 완료 모델 파일
  
    ㄴ backend/												 FastAPI 서버
    	ㄴ main.py										    API 엔드포인트
        ㄴ schmas.py								     입출력 데이터 검증
  
    ㄴ frontend/ 									   React + TypeScript
    	ㄴ src/												React 컴포넌트
  
    ㄴ results/									   성능 지표 및 시각화 결과
    ㄴ tests										   전처리 및 API 테스트
    ㄴ requirements.txt									     Python 의존성
    ㄴ .gitignore										     Git 제외 항목
    ㄴ Dockerfile										   백엔드 실행 환경
    ㄴ plan.md										       	  프로젝트 기획
    ㄴ README.md								  프로젝트 설명 및 실험 결과
```

### 개발 순서

| 날짜  | 작업 폴더                     |
| ----- | ----------------------------- |
| 11/21 | data/   notebooks/          |
| 11/22 | src/preprocessing.py          |
| 11/23 | ml/                           |
| 11/24 | dl/                           |
| 11/25 | src/evalution.py   results/ |
| 11/26 | backend/   frontend/        |
| 11/27 | tests/   README.md          |

### 꼭 지킬 설계 원칙

1. ML과 DL은 분리: 모델 학습 코드를 ml/, dl/에서 각각 관리.
2. 전처리는 공유: 동일한 학습·검증·테스트 데이터 분할을 사용해 공정하게 성능 비교.
3. 추론과 학습은 분리: FastAPI에서는 저장된 모델만 불러와 예측.
4. Git 관리: 대용량 원본 데이터, 모델 가중치, 가상환경, 개인정보가 포함된 파일은 무분별하게 커밋하지 않기.

---

### 일주일치 목표

**11/21 - 데이터 수집 및 EDA**
✅ NHANES 치주검사 데이터 확보
✅ 인구통계·흡연 관련 데이터 결합
✅ 결측치 및 클래스 분포 분석

**11/22 - 전처리 및 학습 데이터 구축**
✅치주질환 라벨 정의 및 생성
✅데이터 누수 방지, 학습·검증·테스트 분리
✅인코딩·스케일링 파이프라인 구현

**11/23 - ML 모델 개발**
ㅁ Logistic Regression 베이스라인
ㅁ XGBoost 모델 학습 및 튜닝
ㅁ F1·Recall·PR-AUC 비교

**11/24 - DL 모델 개발**
ㅁ PyTorch MLP 신경망 설계
ㅁ 학습·검증 루프 및 Early Stopping
ㅁ 학습 곡선과 모델 저장

**11/25 - 모델 평가 및 분석**
ㅁ 공통 테스트셋으로 ML/DL 비교
ㅁ Confusion Matrix 및 ROC/PR Curve
ㅁ SHAP 분석 및 오류 사례 정리

**11/26 - API 및 웹 구현**
ㅁ FastAPI 예측 엔드포인트 구현
ㅁ React 입력 폼 및 결과 화면
ㅁ 학습된 모델 연결

**11/27 - 포트폴리오 완성**
ㅁ Docker 실행 환경 및 테스트
ㅁ README·아키텍처·성능표 작성
ㅁ GitHub 업로드 및 데모 확인

---
