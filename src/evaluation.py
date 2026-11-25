# 1. 라이브러리 및 경로 설정 -------------------------------------------------------------------------------------

from pathlib import Path # pathlib = 파일 및 폴더 경로 관리
                         # Path = 파일 및 폴더 경로 생성 및 조회
import sys # sys = 파이썬 실행환경 관리
           #       파이썬 인터프리터 환경 관리
           #       설치 필요없음 --> 기본 제공
import json   # JSON
import joblib # joblib = ML모델이나 전처리 객체를 파일로 저장 및 불러오기

import numpy as np  # NumPy  = 배열 및 수치 연산
import pandas as pd # Pandas = 표를 가공 및 분석
import matplotlib.pyplot as plt # matplotlib = 데이터 시각화 라이브러리
                                # pyplot = 그래프
import shap  # shap = 모델 예측 결과에 대한 각 입력특성의 기여도 분석
             #        요약: 어떤 입력특성이 예측값을 얼마나 높이고 낮췄는가
import torch # torch = Pytorch
             #         역할: Tensor 연산 및 DL모델 설계 + 학습 + 평가 기능 제공
             #               --> Tensor: 숫자 데이터 저장 후 수학적 연산하는 다차원 배열 
             #                           쓰임새: 사칙연산 | 행렬곱셈 | 가중치 or 편향 계산 |
             #                                   활성화 함수 | 손실값 계산 | 미분 or 기울기 계산 |

from sklearn.metrics import ( # sklearn    = Scikit-learn
                              #              뜻: ML모델 개발 및 데이터 전처리 평가
                              # .metrics() = 모델 예측 성능 측정 및 평가
  accuracy_score,  # 정확도 - 전체데이터 중 모델이 올바르게 예측한 비율
  precision_score, # 정밀도 - 모델이 예측한 것 중 정답라벨인 비율
  recall_score,    # 재현율 - 정답라벨 중 모델이 올바르게 찾아낸 비율
  f1_score,        # F1 스코어 - 정밀도와 재현율을 조화평균 계산
  average_precision_score, # 평균 정밀도 - 여러 임계값 중 재현율 증가량을 가중치로 사용하여 정밀도 가중평균 계산
  roc_auc_score,    # ROC = 수산자 조작 특성
                    # AUC = 곡선 아래 면적
                    # roc_auc_score = ROC 곡선 아래 면적을 계산하여 모델이 양성 or 음성을 얼마나 잘구분하는지 평가
  confusion_matrix, # 혼동행렬 - TP TN FP FN의 데이터 개수 확인
                    # T = True(참)        P = Positive(양성)
                    # F = False(거짓)     F = negative(음성)
                    # TN[진음성] = 예측성공 | 실제라벨=0 예측라벨=0
                    # TP[진양성] = 예측성공 | 실제라벨=1 예측라벨=1
                    # FN[위음성] = 예측실패 | 실제라벨=1 예측라벨=0
                    # FP[위양성] = 예측실패 | 실제라벨=0 에측라벨=1   
                    
  ConfusionMatrixDisplay, # 혼동행렬 시각화
                          # 한마디로 눈에 보이게 하라고 == 출력하라
  roc_curve, # ROC 곡선 체크
             # roc_curve = 여러 임계값의 FPR과 TPR 계산
             # FPR[위양성률] = 실제 음성인 환자를 양성으로 판단한 경우
             #                식: FPR = FP + TN / FP
             # TPR[진양성률] = 실제 양성인 환자를 양성으로 판단한 경우
             #                식: TPR = TP + FN / TP
  precision_recall_curve # 정밀도 재현율 곡선
)                        # 여러 임계값의 정밀도와 재현율 곡선 계산

# 프로젝트 최상위 폴더
ROOT = Path(__file__).resolve().parent.parent # ROOT = C:\projects\projectAI\GangNaengI_AI
                                              # Path = 경로 변환
                                              # __file__  = 현재 파일 경로 
                                              #.resolve() = 절대경로로 지정
                                              # .parent = 부모폴더

PROCESSED = ROOT / "data" / "processed" # PROCESSED = C:\projects\projectAI\GangNaengI_AI\data\processed
MODELS = ROOT / "models"   # MODELS  = C:\projects\projectAI\GangNaengI_AI\models
RESULTS = ROOT / "results" # RESULTS = C:\projects\projectAI\GangNaengI_AI\results

RESULTS.mkdir(parents=True, exist_ok=True) # .mkdir() = 폴더 생성
                                           # parents  = 부모 폴더도 생성
                                           # exist_ok = 이미 생성했으면 그대로

# dl/model.py에서 PeroMLP 불러와라
sys.path.insert(0, str(ROOT / "dl")) # sys = 파이썬 실행 환경과 관련된 기능 제공
                                     # .path()   = 파이썬 모듈 탐색 경로
                                     # .insert() = 리스트의 특정 인덱스에 새 원소 삽입
                                     # str() = 문자열을 str로 변환

# 신경망 불러오기
from model import PerioMLP 

# 재현성을 위한 시드
np.random.seed(42) # .random() = 난수 생성 시드
                   # .seed()   = NP 전역 난수 생성기의 시드 설정
torch.manual_seed(42) # manual_seed() = Pytorch 난수 생성 시드 설정
                      # 난수: 무작위로 생성되는 숫자
                      # 시드: 난수 생성 초기값 --> ex) 42
                      # DL에서 난수 필요한 이유:
                      #   1. 신경망의 초기 가중치를 무작위로 설정하기 위해
                      #   2. 학습데이터 순서 무작위로 섞기 위해
                      #   3. Dropout에서 무작위로 뉴런 0으로 만들기 위해
                      # DL에서 시드가 필요한 이유:
                      #   1. 무작위 연산 결과를 만들어서 재현성 높일 수 있으니까

# 2. 데이터 로딩 ------------------------------------------------------------------------------------------------

# 테스트 데이터 불러오기
# 테스트데이터 = C:\projects\projectAI\GangNaengI_AI\data\processed\test_data.npz
test = np.load(PROCESSED / "test_data.npz") 
X_test = test["X"] # 테스트데이터의 입력데이터
y_test = test["y"] # 테스트데이터의 정답라벨

# SHAP 배경 데이터: 모델 예측 결과에 따라 각 입력특성이 얼마나 기여했는가
# SHAP 배경 데이터 = C:\projects\projectAI\GangNaengI_AI\data\processed\train_data.npz
train = np.load(PROCESSED / "train_data.npz")
X_train = train["X"] # 학습데이터의 입력데이터

print("Test X: ", X_test.shape) # X_test = 테스트데이터의 입력데이터
print("Test y: ", y_test.shape) # y_test = 테스트데이터의 정답라벨
                                # .shape = 배열의 각 차원별 크기를 튜플로 반환
                                #          ex) 출력: (100, 50)
                                #              해석: 100행 50열

assert X_test.shape == (543, 10) # assert = 조건이 맞으면 True니까 다음 코드를 실행하라
                                 #          아니면 AssertError
                                 # 해석: 테스트 데이터가 543행 10열이 맞느냐
assert len(np.unique(y_test)) == 2 # len() = 길이
                                   # .unique() = 중복된 값 제거
assert np.isfinite(X_test).all() # .isfinite() = 배열의 원소가 유한하면 True 
                                 #               하나라도 아니면 False 
                                 #               ex) NaN, 무한수
                                 # .all() = 배열의 모든 원소가 True라면 True
                                 #          하나라도 False면 False

# 3. ML모델 불러오기 --------------------------------------------------------------------------------------------

# 로지스틱 회귀 모델 불러오기
# ML 위치 = C:\projects\projectAI\GangNaengI_AI\models\logistic_regression.joblib
lr_model = joblib.load( # joblib  = 객체를 파일에 저장하거나 불러오기
                        #           쓰임새: ML모델이나 NP 배열 및 전처리 객체 저장용
                        # .load() = 파일에 저장된 객체들 불러오기
  MODELS / "logistic_regression.joblib"
)

# XGBoost 모델 불러오기
# ML 위치 = C:\projects\projectAI\GangNaengI_AI\models\xgboost.joblib
xgb_model = joblib.load(
  MODELS / "xgboost.joblib"
)

print("ML 모델 로딩 완료")

# 4. DL모델 불러오기 --------------------------------------------------------------------------------------------

# 디바이스 부르기
device = torch.device("cpu")

mlp_model = PerioMLP(
  input_dim=X_test.shape[1]
).to(device)

state_dict = torch.load(
  MODELS / "mlp_model.pth",
  map_location=device,
  weights_only=True
)

mlp_model.load_state_dict(state_dict)

# 평가모드
mlp_model.eval()

print("MLP 모델 로딩 완료")

# 5. 3개 모델 예측 확률 구하기 -----------------------------------------------------------------------------------

# 6. ML DL 성능 평가 --------------------------------------------------------------------------------------------

# 7. ML DL 성능 비교 그래프 --------------------------------------------------------------------------------------

# 8. Confusion Matrix 생성 --------------------------------------------------------------------------------------

# 9. ROC Curve --------------------------------------------------------------------------------------------------

# 10. PR Curve --------------------------------------------------------------------------------------------------

# 11. SHAP 분석 -------------------------------------------------------------------------------------------------

# 12. 전처리 입력 변수 이름 복원 ----------------------------------------------------------------------------------

# 13. XGBoost SHAP 중요도 계산 -----------------------------------------------------------------------------------

# 14. 오분류 사례 분석 -------------------------------------------------------------------------------------------

# 15. 결과 요약 --------------------------------------------------------------------------------------------------