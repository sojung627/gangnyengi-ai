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
                    # TN[진음성] = 예측성공 | 실제라벨=0 예측라벨=0 | 음성을 음성으로 예측
                    # TP[진양성] = 예측성공 | 실제라벨=1 예측라벨=1 | 양성을 양성으로 예측
                    # FN[위음성] = 예측실패 | 실제라벨=1 예측라벨=0 | 음성을 양성으로 예측
                    # FP[위양성] = 예측실패 | 실제라벨=0 에측라벨=1 | 양성을 음성으로 예측
                    
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

# 디바이스 결정
device = torch.device("cpu") # CPU 써라

mlp_model = PerioMLP(
  input_dim=X_test.shape[1] # input_dim = 신경망의 특성개수 전달
                            # .shape    = 배열 차원의 크기를 튜플로 변환 
                            #             ex) 출력: (100, 50)
                            #                 해석: 100행 50열
                            # .shape[1] = 인덱스가 1인 값들 가져와라
).to(device) # .to() = 모델 or Tensor를 CPU로 이동

# 학습모델 상태 불러오기
state_dict = torch.load( # load() = 저장한 파일을 저장한 객체로 불러라
  MODELS / "mlp_model.pth", # 학습모델 위치 = C:\projects\projectAI\GangNaengI_AI\models\mlp_model.pth
  map_location=device, # map_location = 저장된 Tensor를 해당 연산장치로 보내라
  weights_only=True    # weights_only = 파일 불러올 때 기본객체만 불러라
)                      # True = 기본자료형만 / False = 기본자료형 말고도

mlp_model.load_state_dict(state_dict) # .load_state_dict() = 모델 상태를 신경망에 적용

# 신경망 평가모드
mlp_model.eval() # 평가모드 = Dropout 비활성화 | 모델 평가 및 예측 | 기울기 계산(설정에 따라 가능)

print("MLP 모델 로딩 완료")

# 5. 모델 3개 예측 확률 구하기 -----------------------------------------------------------------------------------

# 모델 3개 
# 1. Logistic Regression
# 2. XGBoost
# 3. Pytorch

# Logistic Regression 예측 확률
lr_prob = lr_model.predict_proba(X_test)[:, 1] # .predict_proba() = 에측 확률 반환
                                               # [:, 1] = 모든 행의 인덱스 1번 열 추출

# XGBoost 예측 확률
xgb_prob = xgb_model.predict_proba(X_test)[:, 1]

# Pytorch MCP 예측 확률
with torch.no_grad(): # with = 특정 실행환경 설정 + 정리
                      # no_grad() = 자동 미분 후 기록 비활성화
                      #             사용 이유: 손실값을 줄여 가중치를 수정 시 필요
  X_tensor = torch.tensor( # tensor() = 전달받은 데이터를 Tensor로 생성
    X_test,
    dtype=torch.float32,
    device=device
  )
  # 활성화 함수 적용 전 모델 출력값
  logits = mlp_model(X_tensor) # 모델 순전파 연산하라
                               # 순전파: 입력층 -> 은닉층 -> 출력층
                               # 로짓: 출력층에 반환된 값
                               #       출력 활성화 함수를 적용하기 전 점수
                               #       출력 활성화 함수: Sigmoid, Softmax

  # 로짓을 예측 확률로 변환
  mlp_prob = torch.sigmoid( # .sigmoid() = 입력값을 0~1 사이 값으로 변환
    logits
  ).cpu().numpy().ravel() # .cpu()   = Tensor를 CPU로 이동
                          # .numpy() = Tensor를 NP로 변환
                          # .ravel() = 다차원 NP를 1차원 NP로

# 모델별 예측 확률 및 임계값 저장
models = {
  # 로지스틱 회귀 모델
  "Logistic Regreesion": {
    "prob": lr_prob, # prob = 확률
    "threshold": 0.5 # threshold = 임계값 or 분류 기준값
  },                 # 양성분류 기준 = 50%
  # XGBoost 모델(앙상블)
  "XGBoost": {
    "prob": xgb_prob, # prob = 확률
    "threshold": 0.5  # threshold = 임계값 or 분류 기준값
  },                  # 양성분류 기준 = 50%
  # DL 모델 신경망(PyTorch)
  "PyTorch MLP": {
    "prob": mlp_prob, # prob = 확률
    "threshold": 0.3  # threshold = 임계값 or 분류 기준값
  }                   # 양성분류 기준 = 30%
}  

# 모델별 예측 확률 개수 출력
for name, info in models.items(): # name     = 모델명
                                  # info     = 임계값 등등 정보
  print(                          # .items() = dict의 key랑 value 동시 출력하라
    name,
    "예측 확률 개수: ", len(info["prob"]) # len() = 길이
  )                                      # prob  = 확률

# 6. ML DL 성능 평가 --------------------------------------------------------------------------------------------

# 성능 평가
def evaluate_model(y_true, probabillities, threshold, name): # y_true = 실제 정답라벨
                                                             # probabillities = 모델 예측 확률
                                                             # threshold = 분류 임계값
                                                             # name = 평가할 모델명
  # 예측확률을 분류라벨로 변환                                                           
  predictions = ( # predictions = 예측라벨 저장
    probabillities >= threshold # 예측확률 배열 >= 분류 임계값
  ).astype(int) # .astype() = 타입 변환하라

  return {
    "model": name, # 모델명
    "threshold": threshold, # 분류 임계값
    "accuracy": accuracy_score(y_true, predictions), # accuracy = 정확도
                                                     # y_true   = 실제 정답라벨
                                                     # predictions = 모델 예측라벨
    "precisions": precision_score( # precisions = 정밀도
      y_true, predictions, zero_division=0 # y_true = 실제 정답라벨
                                           # predictions = 모델 예측라벨
                                           # zero_division = 계산 안되는 경우 0으로 나눠라
    ),
    "recall": recall_score( # 재현율
      y_true, predictions, zero_division=0 # y_true = 실제 정답라벨
                                           # predictions = 모델 예측라벨
                                           # zero_division = 계산 안되는 경우 0으로 나눠라
    ),                        
    "f1": f1_score( # F1 스코어
      y_true, predictions, zero_division=0 # y_true = 실제 정답라벨
                                           # predictions = 모델 예측라벨
                                           # zero_division = 계산 안되는 경우 0으로 나눠라
    ),
    "roc_auc": roc_auc_score( # roc_auc_score() = ROC 곡선 아래 면적 계산
                              # 추가한 이유: 양성사례가 음성사례보다 높은예측점수 받는 경우 평가하기 위해서
      y_true, probabillities  # y_true = 실제 정답라벨
                              # probabillities = 모델 에측확률
    ),
    "average_precision": average_precision_score( # average_precision = 평균 정밀도(AP)
                                                  # 평균 정밀도: 임계값들 중 재현율 증가량을 가중치로 사용하여 
                                                  #             정밀도 가중 평균 계산
      y_true, probabillities # y_true = 실제 정답라벨
    )                        # probabillities = 모델 에측확률
  }

# 모델별 성능 지표 계산
results = [] 

for name, info in models.items(): # name = 모델명
                                  # info = 모델 예측확률 + 임계값
                                  # .items() = dict의 key랑 value 반환
  # 모델 성능 평가 결과                                 
  scores = evaluate_model( 
    y_test, # 테스트데이터 실제 정답라벨
    info["prob"], # 현 모델 예측 확률
    info["threshold"], # 현 모델 분류 임계값
    name # 현 모델명
  )
  # 평가 결과 추가
  results.append(scores) # .append() = 리스트에 추가

# 모델 성능 평가 표 저장
results_df = pd.DataFrame(results)

# F1 높은 순서로(내림차순) 정렬
results_df = results_df.sort_values( # .sort_values() = 지정한 열 기준으로 데이터 정렬
  by="f1", # by = 정렬기준 설정
           # F1 스코어 기준으로 정렬
  ascending=False # ascending = 오름차순 or 내림차순 설정
)                 # True = 오름차순 | False = 내림차순

print("\n=== FINAL TEST RESULTS===")
print(results_df.to_string(index=False)) # .to_string() = DF 문자열로 반환
                                         # index = 인덱스 행 출력 여부 결정
                                         # True =  출력 | False = 출력 x

# CSV 저장
results_df.to_csv( # .to_csv() = DF에서 CSV로 변환
  RESULTS / "final_model_comparison.csv", # 모델평가 CSV 위치 = 
                                          # C:\projects\projectAI\GangNaengI_AI\models\final_model_comparison.csv
  index=False # index = 인덱스 행 저장 여부 결정
)             # True = 저장 | False = 저장 x

# 7. ML DL 성능 비교 그래프 --------------------------------------------------------------------------------------

# 그래프 표기할 것들
metrics = [
  "precision", # 재현율
  "recall",    # 재현율
  "f1",        # F1 스코어
  "roc_auc",   # ROC 곡선 아래 면적 계산
  "average_precision" # 평균 정밀도
]

plot_df = results_df.set_index("model")[metrics] # .set_index() = 특정 열을 행 인덱스로 지정
                                                 # [metrics] = metrics 리스트에 포함된 열만 추출

ax = plot_df.T.plot( # .T = Transpose(전치)
                     #      행과 열을 서로 교환
                     # .plot() = DF 그래프 시각화
  kind="bar", # kind = 그래프 종류 설정
              # bar  = 믹대그래프 
  figsize=(11, 6), # figsize = 그래프 사이즈
                   # --> 그래프 가로 11인치 + 세로 6인치
  rot=0 # rot = Rotation
)       #       X축 눈금 라벨 회전 각도
        #       딱히 성능은 아니고 이름이 어떻게 나오느냐임(디자인적 영역)
        #       이름        름
        #                 이
        #       이런 정도?
        # rot=0 = 눈금 라벨 회전 x

ax.set_title("ML DL Model Comparison") # ax = Axes 객체 저장할 변수
                                       # Axes = Matplotlib의 그래프의 영역 관리
                                       #        한마디로 디자인적인 영역
                                       # set_title() = 그래프 제목
ax.set_ylabel("score") # set_ylabel() = y 라벨 설정
ax.set_ylim(0, 1) # set_ylim() = y축의 표시 범위 설정
                  #              lim = limit
ax.legend(title="Model") # .legand() = 그래프 범례 표시 및 설정
                         # title = 범례 제목 설정
                         # 범례: 그래프의 색상 및 기호가 무엇인지 알려줌
                         #       ex) 초록색 막대그래프 = 식물의 키
                         #           갈색 막대그래프   = 나무의 키
plt.tight_layout() # plt = 그래프
                   # tight_layout() = 여백 자동 조절
plt.savefig( # savefig() = 현 figure를 이미지로 저장
  RESULTS / "model_comparision.png", # 성능 비교 그래프 사진 =
                                     # C:\projects\projectAI\GangNaengI_AI\results\model_comparision.png
  dpi=150 # dpi = 이미지 해상도                              
)         # 1인치당 150개의 점으로 구성된 해상도

plt.show() # 그래프 출력       

# 8. Confusion Matrix 생성 --------------------------------------------------------------------------------------

# Confusion Matrix = 혼동행렬
# 혼동행렬 - TP TN FP FN의 데이터 개수 확인
#   T = True(참)        P = Positive(양성)
#   F = False(거짓)     F = negative(음성)
#   TN[진음성] = 예측성공 | 실제라벨=0 예측라벨=0 | 음성을 음성으로 예측
#   TP[진양성] = 예측성공 | 실제라벨=1 예측라벨=1 | 양성을 양성으로 예측
#   FN[위음성] = 예측실패 | 실제라벨=1 예측라벨=0 | 양성을 음성으로 예측
#   FP[위양성] = 예측실패 | 실제라벨=0 에측라벨=1 | 음성을 양성으로 예측 

for name, info in models.items(): # name     = 모델명
                                  # info     = 모델 정보
                                  # .items() = dict의 Key와 Value 반환
  y_pred = ( # y_pred = 예측라벨
    info["prob"] >= info["threshold"] # prob = 모델 예측확률 배열
                                      # threshold = 모델 분류 임계값
  ).astype(int) # .astype() = 배열을 자료형으로 변환

  # 혼동행렬 생성 - 실제 라벨과 예측라벨 비교
  cm = confusion_matrix(
    y_test, # 테스트데이터의 정답라벨
    y_pred, # 모델의 예측라벨
    labels=[0, 1] # labels = 라벨 배치 순서
  )               # [0, 1] = 음성에서 양성 순으로 배치
                  # [1, 0] = 양성에서 음성 순으로 배치

  # 혼동행렬 시각화
  disp = ConfusionMatrixDisplay( # ConfusionMatrixDisplay = 혼동행렬 시각화
    confusion_matrix=cm, # confusion_matrix = 시각화할 혼동행렬 전달
    display_labels=["Negative", "Positive"] # display_labels = 그래프의 라벨명 지정
  )                                         # 라벨명: Negative = 음성 | Positive = 양성

  disp.plot( # .plot() = 그래프 그려라
    cmap="Blues", # cmap = Color Map
                  # Color Map = 데이터 수치에 따라 색상 정함
                  #             ex) 진한파랑, 중간파랑, 연한파랑 ... 
    values_format="d" # values_format = 혼동행렬 내부 숫자 출력 형식 지정
  )                   # d = 십진정수 형식

  plt.title(f"{name} - Confusion Matrix") # .title() = 그래프 제목
  plt.tight_layout() # tight_layout() = 그래프 여백 자동 조절

  # 이미지 파일명 지정
  filename = (
    name.lower() # .lower() = 소문자
                 # .upper() = 대문자
    .replace(" ", "_") # .replace() = 문자열 바꿔라
                       # 해석: 빈칸을 _로 바꿔라
    + "_confusion_matrix.png" # 해석: 맨 끝은 _confusion_matrix.png 이걸로 지정하라
  )                           # ex) logistic_regression_confusion_matrix.png
                              #     xgboost_confusion_matrix.png
                              #     pytorch_mlp_confusion_matrix.png

  plt.savefig( # .savefig() = 현 Figure를 이미지로 바꿔 저장
    RESULTS / filename, # 이미지 위치 = C:\projects\projectAI\GangNaengI_AI\results\파일이미지명
    dpi=150 # dpi = 해상도
  )         # 해석: 1인치당 점 150개의 해상도

  plt.show() # 그래프 출력

  # 혼동행렬 TN FP FN TP 추출
  tn, fp, fn, tp = cm.ravel() # .ravel() = 다차원 NP를 일차원 NP로 바꿔라

  print(f"\n{name}")
  print(f"TP: {tp}, TN: {tn}")
  print(f"FP: {fp}, FN: {fn}")

# 9. ROC Curve --------------------------------------------------------------------------------------------------

# ROC 곡선 = ROC Curve
#   roc_curve = 여러 임계값의 FPR과 TPR 계산
#   FPR[위양성률] = 실제 음성인 환자를 양성으로 판단한 경우
#                   식: FPR = FP + TN / FP
#   TPR[진양성률] = 실제 양성인 환자를 양성으로 판단한 경우
#                   식: TPR = TP + FN / TP

plt.figure(figsize=(9, 6))

for name, info in models.items():
  fpr, tpr, thresholds = roc_curve(
    y_test,
    info["porb"]
  )

  auc = roc_auc_score(
    y_test,
    info["prob"]
  )

  plt.plot(
    fpr,
    tpr,
    label=f"{name} (AUC={auc:.3f})"
  )

# 무작위 분류 기준선
plt.plot(
  [0, 1],
  [0, 1],
  "k--",
  label="Random Baseline"
)  

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - ML vs DL")
plt.legend()
plt.tight_layout()

plt.savefig(
  RESULTS / "roc_curve.png",
  dpi=150
)

plt.show()

# 10. PR Curve --------------------------------------------------------------------------------------------------

# 11. SHAP 분석 -------------------------------------------------------------------------------------------------

# 12. 전처리 입력 변수 이름 복원 ----------------------------------------------------------------------------------

# 13. XGBoost SHAP 중요도 계산 -----------------------------------------------------------------------------------

# 14. 오분류 사례 분석 -------------------------------------------------------------------------------------------

# 15. 결과 요약 --------------------------------------------------------------------------------------------------