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
def evaluate_model(model, X, y, model_name): # model = ML 모델 
                                             # X = 입력데이터 
                                             # y = 정답라벨
                                             # model_name = 모델명
  # 이진법 - 0 또는 1
  y_pred = model.predict(X) # .predict() = 입력데이터로 예측 결과 반환

  # 클래스 1일 확률 예측
  y_prob = model.predict_proba(X)[:, 1] # .predict_proba() = 각 클래스에 속할 확률 반환
                                        # [:, 1] 
                                        # : = 모든 행 선택 
                                        # 1 = 두번째 컬럼의 클래스가 1일 확률 

  # 모델 평가 점수 저장
  scores = {
    "model": model_name,
    "accuracy": accuracy_score(y, y_pred), # 정확도
    "precision": precision_score( # 정밀도
      y, y_pred, zero_division=0  # 계산 불가능한 정밀도는 0으로 처리하라
    ),
    "recall": recall_score(      # 재현율
      y, y_pred, zero_division=0 # 계산 불가능한 재현율은 0으로 처리하라 
    ),
    "f1": f1_score(              # f1 스코어
      y, y_pred, zero_division=0 # 계산 불가능한 f1 스코어는 0으로 처리하라 
    ),
    "average_precision": average_precision_score( # 평균 정밀도(AP)
      y, y_prob                                   # 뜻: 정밀도를 재현율 증가에 따라 가중 평균화 함
    )
  }

  print(f"\n[{model_name}]")
  print(
    classification_report(       # classification_report() = 분류 모델 평가 결과를 표로 반환하는 함수
      y, y_pred, zero_division=0 # 평가지표 계산 안되면 0으로 처리하라
    )
  )

  return scores

# 4. Logistic Regression 학습 ---------------------------------------------------------------------------------

# 로지스틱 회귀 학습
lr_model = LogisticRegression( # LogisticRegression() = 로지스틱 회귀 모델 생성
  max_iter=1000,  # 학습 최대 반복 횟수
  random_state=42 # 난수 사용 시 난수 시드는 42로 사용
                  # 난수: 무작위로 생성되는 숫자
)

# 모델 학습
lr_model.fit(X_train, y_train) # .fit() = ()안의 것들로 모델 학습
                               # 해석: 학습데이터와 정답라벨로 모델 학습

# 검증데이터 평가   
lr_result = evaluate_model( # lr_result = 로지스틱 회귀 모델 평가 결과
                            # evaluate_model() = 모델 성능 평가 함수
  lr_model, # 로지스틱 회귀 모델
  X_val,    # 검증데이터의 입력데이터
  y_val,    # 정답라벨의 입력데이터
  "Logistic Regression" # 평가 결과에 표시될 모델명
)

# 모델 저장
joblib.dump( # joblib  = ML모델을 파일로 저장하거나 불러옴
             # .dump() = 파이썬 모델을 직렬화하여 파일로 저장
             # 직렬화: 객체를 파일에 저장할 수 있는 형태로 변환
  lr_model,  # 학습 완료된 로지스틱 회귀 모델
  MODELS / "logistic_regression.joblib" # 모델 저장 경로 = 
)                                       # C:\projects\projectAI\GangNaengI_AI\models\logistic_regression.joblib

print(("Logistic Regression 학습 완료"))

# 5. XGBoost 모델 학습 ----------------------------------------------------------------------------------------

# XGBoost 모델 학습 + 튜닝
configs = [
  {"max_depth": 2, "learning_rate": 0.05}, # max_depth     = 결정트리 최대 깊이
  {"max_depth": 3, "learning_rate": 0.05}, # learning_rate = 학습률 지정
  {"max_depth": 3, "learning_rate": 0.02}  # 하이퍼 파리미터 중 하나다(사용자가 설정하는 것)
]

xgb_results = [] # xgb_results = XGBoost 모델 결과 저장하는 리스트
best_xgb = None  # best_xgb = 가장 좋은 XGBoost 모델만 저장
                 # None = 지정되지 않음
best_f1 = -1 # best_f1 = f1 스코어 중 제일 좋은 것
             # -1 = 초기 비교 기준값

for config in configs: # 아까 그 config들 저장
  model = XGBClassifier( # XGBClassifier() = XGBoost 분류 모델 생성
    n_estimators=200, # n_estimators = 부스팅 중 생성될 결정트리 개수
    max_depth=config["max_depth"],         # max_depth = 결정트리 최대 깊이
    learning_rate=config["learning_rate"], # learning_rate = 학습률
    objective="binary:logistic", # objective = 모델 최적화할 학습 목적
                                 # binary:logistic = 이진법 로지스틱 손실 사용하라
    eval_metric="logloss", # eval_metric = 모델성능 평가할 지표
                           # logloss     = 로그 손실
    random_state=42, # random_state = 난수 시드
    n_jobs=-1,       # n_jobs = 모델학습에 사용할 CPU 병렬 작업 수 설정 
    tree_method="hist" # tree_method = 결정트리 생성할 알고리즘 지정
  )                    # hist = 히스토그램 기반 트리 생성 알고리즘 지정

  # Train으로 학습
  model.fit(X_train, y_train) # .fit()  = 데이터 이용해 모델 학습 시키는 메서드
                              # X_train = 학습데이터의 입력데이터
                              # y_train = 학습데이터의 정답라벨

  # 모델명 정하기
  model_name = (
    f"XGBoost_depth{config['max_depth']}" # XGBoost_depth = 모델명
    f"_lr{config['learning_rate']}" # _lr = 학습률 표시
  )                                 # ex) 모델명: XGBoost_depth2_lr0.05

  # Val로 성능 평가
  scores = evaluate_model(
    model, # 학습 완료된 XGBoost 모델
    X_val, # 검증데이터의 입력데이터
    y_val, # 검증데이터의 정답라벨
    model_name # 모델명
  )

  xgb_results.append(scores) # xgb_results = 모델 결과 저장
                             # .append()   = 리스트에 추가

  # 가장 높은 Val F1 모델 선택
  if scores["f1"] > best_f1: # 현재 f1 > 최고의 f1
    best_f1 = scores["f1"] # 현재 f1이 더 높으면 현재로 수정
    best_xgb = model       # XGBoost 1등 모델도 현재로 변경

# 최적 XGBoost 모델 저장
joblib.dump( # joblib = ML모델을 파일로 저장하거나 불러옴
  best_xgb,  # best_xgb = XGBoost 1등 모델
  MODELS / "xgboost.joblib" # 최고 모델 저장 경로 = 
)                           # C:\projects\projectAI\GangNaengI_AI\models\xgboost.joblib

print("XGBoost 학습 및 튜닝 완료")

# 6. 모델 성능 비교 및 저장 ------------------------------------------------------------------------------------

all_results = [lr_result] + xgb_results

results_df = pd.DataFrame(all_results)

# F1 높은 순으로 정렬
results_df = results_df.sort_values(
  by="f1",
  ascending=False
)

print("\n=== Validation 성능 비교 ===")
print(results_df.to_string(index=False))

# 성능이 가장 높은 모델 기록
best_model_name = results_df.iloc[0]["model"]

summary = {
  "Selection_metric": "validation_f1",
  "best_model": best_model_name,
  "best_f1": float(results_df.iloc[0]["f1"]),
  "evalution_split": "validation"
}

with open(
  RESULTS / "ml_summary.json",
  "w",
  encoding="utf-8"
) as f:
  json.dump(summary, f, indent=2, ensure_ascii=False)

print("\n최고 Validation F1 모델: ", best_model_name)
print("day03 - ML모델 학습 완료")  