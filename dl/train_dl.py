# 1. 라이브러리 및 경로 설정 -------------------------------------------------------------------------------------

from pathlib import Path  # pathlib = 파일 폴더 관리
                          # Path = 경로 생성 및 파일 폴더 생성
from copy import deepcopy # copy = 객체 복사 기능
                          # deepcopy = 객체 내부 데이터까지 복사
                          #            복사본을 수정해도 원본은 무관
import json 

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt # matplotlib = 데이터 시각화 라이브러리
                                # pyplot = 그래프 생성 및 수정

import torch # torch = Pytorch 라이브러리
from torch import nn # nn = Pytorch 신경망 모듈
from torch.utils.data import TensorDataset, DataLoader # .utils = Pytorch 보조 기능 제공
                                                       # .data  = 데이터 관리 및 처리
                                                       # TesorDataset = 입력데이터와 정답데이터의 텐서를 
                                                       #                하나의 데이터셋으로 통합
                                                       # DataLoader = 데이터셋을 일정한 크기(Batch)로 나누어 모델에 전달

from sklearn.metrics import ( # .metrics = 모델의 예측 성능 평가용
  accuracy_score,  # 정확도: 전체데이터 중 예측 잘한 비율
  precision_score, # 정밀도: 예측 중 실제로 치주질환 있을 비율
  recall_score,    # 재현율: 치주질환자 중 모델에 예측 성공한 비율
  f1_score,        # F1 스코어: 정밀도와 재현율의 조화평균
  average_precision_score # AP: PR곡선의 평균 정밀도 스코어   
)

from model import PerioMLP # 내가 설계한 치주 MLP(신경망)

# 프로젝트 경로
ROOT = Path(__file__).resolve().parent.parent # Path(__file__) = 현 파일을 파이썬 경로로
                                              # .resolve() = 절대경로로 지정
                                              # ROOT = C:\projects\projectAI\GangNaengI_AI

PROCESSED = ROOT / "data" / "processed" # PROCESSED = C:\projects\projectAI\GangNaengI_AI\data\processed
MODELS = ROOT / "models"   # MODELS  = C:\projects\projectAI\GangNaengI_AI\models
RESULTS = ROOT / "results" # RESULTS = C:\projects\projectAI\GangNaengI_AI\results

MODELS.mkdir(parents=True, exist_ok=True)  # .mkdir = 폴더 생성
RESULTS.mkdir(parents=True, exist_ok=True) # parent=True   = 부모 폴더도 생성
                                           # exist_ok=True = 이미 폴더 있다면 생성하지도 말고 오류도 내지마

# 재현 가능한 실험을 위한 시드
torch.manual_seed(42) # manual_seed() = Pytorch 난수 생성 시드
                      # 42 = 난수 생성 시 기본값
np.random.seed(42) # random() = 난수 생성
                   # .seed()  = 난수 생성 시 기준값 설정

# CPU or GPU
device = torch.device( # .device() = 모델 학습 시 사용할 연산 장치 정보 저장
  "cuda" if torch.cuda.is_available() else "cpu" # cuda    = 엔비디아 GPU로 연산 수행
)                                                # .cuda() = cuda 관련 기능 제공하라
                                                 # is_availabel() = cuda 사용가능 여부 확인
                                                 # cpu = cuda 사용 못하면 cpu 써라 

print("사용 장치: ", device)

# 2. 데이터 부르기 + Tensor 변환 --------------------------------------------------------------------------------

# 데이터 불러오기
# 학습데이터 위치: C:\projects\projectAI\GangNaengI_AI\data\processed\train_data.npz
# 검증데이터 위치: C:\projects\projectAI\GangNaengI_AI\data\processed\val_data.npz
train = np.load(PROCESSED / "train_data.npz") 
val = np.load(PROCESSED / "val_data.npz")

X_train = train["X"] # = 학습데이터의 입력데이터
y_train = train["y"] # = 학습데이터의 정답라벨

X_val = val["X"] # = 검증데이터의 입력데이터
y_val = val["y"] # = 검증데이터의 정답라벨

# Pytorch --> Tensor로 변환
X_train_tensor = torch.tensor( # Tensor 뜻: 데이터를 저장한 뒤 수학적연산하는 다차원 배열
  X_train, dtype=torch.float32 # .tensor() = 리스트나 np 같은 것들을 Tensor로 변환
)

y_train_tensor = torch.tensor(
  y_train, dtype=torch.float32
).reshape(-1, 1) # .reshape() = 데이터의 개수 + 값은 유지한채 배열로 변경
                 # -1 = 전체 데이터 개수에 맞춰 행으로 만들어라
                 # 1  = 열의 개수는 1개

X_val_tensor = torch.tensor(
  X_val, dtype=torch.float32
)

y_val_tensor = torch.tensor(
  y_val, dtype=torch.float32
).reshape(-1, 1)

# 데이터 검증
assert torch.isfinite(X_train_tensor).all() # assert = 조건이 True면 실행 False면 AssertError
                                            # .isfinite() = 각 원소가 유한한 숫자인지 검사
                                            #               NaN이거나 무한수면 False 반환
                                            # .all() = 모든 원소가 True면 True 반환하라
assert torch.isfinite(X_val_tensor).all()
assert X_train_tensor.shape[0] == y_train_tensor.shape[0] # .shape    = 차원 크기 반환
assert y_val_tensor.shape[0] == y_val_tensor.shape[0]     # .shape[0] = 행의 개수 
                                                          # .shape[1] = 열의 개수

# 데이터셋 생성
train_dataset = TensorDataset( # TensorDataset() = 여러 tensor를 하나의 데이터셋으로 만듦
  X_train_tensor,
  y_train_tensor
)

# 데이터로더 생성
train_loader = DataLoader( # 데이터셋을 일정한 크기고 쪼개어 모델에 전달
  train_dataset, # = 학습용 데이터셋
  batch_size=32, # 학습 1회당 연산에 사용할 데이터 몇개로 할 지
  shuffle=True   # 데이터 순서 무작위로 하라
)

print("Train: ", X_train_tensor.shape)
print("Validation: ", X_val_tensor.shape)


# 3. 모델 + 손실함수 + 옵티마이저 설정 ---------------------------------------------------------------------------

# 4. 모델 학습 루프 구현 ----------------------------------------------------------------------------------------

# 5. 학습 곡선 그리기 -------------------------------------------------------------------------------------------

# 6. 최적 모델 평가 및 저장 -------------------------------------------------------------------------------------