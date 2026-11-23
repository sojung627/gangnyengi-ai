# 1. 라이브러리 및 파일 경로 설정 ------------------------------------------------------------------------------

from pathlib import Path # pathlib = 파일 및 폴더 라이브러리
import json   # json   = 라이브러리
import joblib # joblib = ML모델을 파일로 저장하거나 불러오는 라이브러리
import numpy as np  # numpy  = 배열 및 수치 계산용 라이브러리
import pandas as pd # pandas = 표 형태의 데이터 가공 라이브러리

from sklearn.linear_model import LogisticRegression # scklearn = scikit-learn 라이브러리
                                                    # .linear_model      = 선형모델 기능 제공하는 모듈
                                                    # LogisticRegression = 로지스틱 회귀모델 생성하는 클래스
from sklearn.metrics import ( # .metrics = ML모델 성능을 평가하는 모듈
  accuracy_score,  # 전체 예측 정확도(정확도 스코어)
  precision_score, # 양성 예측 중 실제 양성 비율(정밀도 스코어)
  recall_score, # 실제 양성 중 찾아낸 비율(재현율 스코어)
  f1_score,     # precision과 recall의 조화평균                   # precision = 정밀도
  average_precision_score, # PR곡선의 평균 정밀도 스코어           # recall    = 재현율
  classification_report    # 정밀도, 재현율, f1 스코어 표로 정리   # f1 스코어  = 정밀도와 재현율을 고려한 스코어
)

from xgboost import XGBClassifier # xgboost       = 경사 부스팅 기반 ML 알고리즘 라이브러리
                                  # XGBClassifier = XGBoost 분류 모델 생성하는 클래스
                                  # --> XGBoost는 앙상블 중 하나이다

# 프로젝트 루트
ROOT = Path(__file__).resolve().parent.parent # Path(__file__) = 현 파일을 파이썬 경로로
                                              # .resolve() = 절대 경로로 변환
                                              # .parent    = 부모 폴더
                                              # ROOT = C:\projects\projectAI\GangNaengI_AI

PROCESSED = ROOT / "data" / "processed" # PROCESSED = C:\projects\projectAI\GangNaengI_AI\data\processed
MODELS = ROOT / "models"   # MODELS  = C:\projects\projectAI\GangNaengI_AI\models
RESULTS = ROOT / "results" # RESULTS = C:\projects\projectAI\GangNaengI_AI\results

MODELS.mkdir(parents=True, exist_ok=True)  # .mkdir        = 파일 생성
RESULTS.mkdir(parents=True, exist_ok=True) # parents=True  = 부모 폴더도 함께 생성하라
                                           # exist_ok=True = 이미 존재해서 폴더 생성 안하는 경우 에러 없이 처리하라

# 2. 학습데이터 불러오기 --------------------------------------------------------------------------------------

# 데이터 불러오기
# 학습데이터 위치 = C:\projects\projectAI\GangNaengI_AI\data\processed\train_data.npz
# 검증데이터 위치 = C:\projects\projectAI\GangNaengI_AI\data\processed\val_data.npz
train = np.load(PROCESSED / "train_data.npz") # train = 학습데이터
val = np.load(PROCESSED / "val_data.npz")     # val   = 검증데이터

# 학습 데이터
X_train = train["X"] # X = 입력데이터
y_train = train["y"] # y = 정답라벨

# 검증 데이터
X_val = val["X"] # X = 입력데이터
y_val = val["y"] # y = 정답라벨

# 데이터 크기 확인
print("X_train: ", X_train.shape) # 학습데이터의 입력데이터 행과 열(튜플)
print("y_train: ", y_train.shape) # 학습데이터의 정답라벨 행과 열(튜플)

print("X-val: ", X_val.shape) # 검증데이터의 입력데이터 행과 열(튜플)
print("y_val: ", y_val.shape) # 검증데이터의 정답라벨 행과 열(튜플)

# 클래스 분포 확인
print("Train 클래스: ", np.unique(y_train, return_counts=True))    # np.unique() = np의 중복값 제거
print("Validation 클래스: ", np.unique(y_val, return_counts=True)) # return_counts=True = 고유값이 각 몇번 등장했는가
                                                                  
assert X_train.shape[1] == X_val.shape[1] # assert    = 조건이 True인지 검사 --> False면 AssertError
                                          # .shape[1] = 열만 반환
assert set(np.unique(y_train)) == {0, 1}  # np.unique() = np의 중복값 제거
assert set(np.unique(y_val)) == {0, 1}    # {0, 1} = 정답라벨에서 허용한 값만 --> {0, 1}

# 3. 모델 성능 평가 ----------------------------------------------------------------------------------

# 모델 평가
def evaluate_model(model, X, y, model_name):
  # 이진법 - 0 또는 1
  y_pred = model.predict(X)

  # 클래스 1일 확률 예측
  y_prob = model.predict_proba(X)[:, 1]

  scores = {
    "model": model_name,
    "accuracy": accuracy_score(y, y_pred),
    "precision": precision_score(
      y, y_pred, zero_division=0
    ),
    "recall": recall_score(
      y, y_pred, zero_division=0
    ),
    "f1": f1_score(
      y, y_pred, zero_division=0
    ),
    "average_precision": average_precision_score(
      y, y_prob
    )
  }

  print(f"\n[{model_name}]")
  print(
    classification_report(
      y, y_pred, zero_division=0
    )
  )

  return scores

# 4. Logistic Regression 학습 ---------------------------------------------------------------------------------

# 5. XGBoost 모델 학습 ----------------------------------------------------------------------------------------

# 6. 모델 성능 비교 및 저장 ------------------------------------------------------------------------------------