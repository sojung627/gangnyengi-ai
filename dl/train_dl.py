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

# 입력 변수 개수
input_dim = X_train.shape[1]  # input_dim = 입력 특성 개수 저장
                              # X_train.shape[1] = X_train의 컬럼만 대입

# 모델 생성
model = PerioMLP(input_dim).to(device) # PerioMLP  = 치주질환 신경망
                                       # input_dim = 입력 특성 개수
                                       # .to()  = PR모델이나 Tensor를 연산장치로 이동
                                       # device = 연산장치(GPU / CPU)

# 이진분류 손실함수
criterion = nn.BCEWithLogitsLoss() # crierion = 손실함수
                                  # nn = Pytorch 신경망 관련 기능 제공 모듈
                                  # .BCEWithLogitsLoss() = 시그모이드함수랑 이진교차 엔트로피 손실함수 결합
                                  # 시그모이드 함수: 모델이 출력한 숫자를 0~1 사이 확률값으로 반환
                                  # 이진: 0이나 1이라는 두가지 클래스로 분류
                                  # 교차 엔트로피: 정답라벨의 분포 + 모델이 예측한 확률 분포 차이 평가 
                                  # 손실함수: 모델 에측과 정답이 얼마나 다른지 수치로 계산
                                  # 해석: 출력값(로짓)이 2.0 
                                  #       -> 
                                  #       시그모이드 0~1 사이 반환 --> 값 0.881
                                  #       -> 
                                  #       바이너리 크로스 엔트로피(예측확률) --> 정답라벨 1과 비교
                                  #       -> 
                                  #       손실값 --> 약 0.127

# 가중치 최적화 알고리즘
optimizer = torch.optim.Adam( # optimizer = 옵티마이저 저장용
                              # 옵티마이저: 가중치와 편향 조절 알고리즘
                              # .optim() = 가중치 최적화 알고리즘
                              # .Adam()  = 기울기 이동평균과 기울기 제곱 이동평균으로 매개변수 업데이트 크기 조절
  model.parameters(), # .parameters() = 모델 내부에 등록된 매개변수 중 순회 가능한 객체만 반환
  lr=0.001 # Learning rate(학습률)
)          # 가중치와 편향 업데이트 시 업데이트 크기 조절

# 학습 설정
EPOCHS = 100 # EPOCHS = 전체 학습데이터 한번씩 사용하라
             # 최대 100번 학습하라
PATIENT = 10 # PATIENT = 검증 성능이 개선되지 않을 때 PATIENT에 저장
             # 10 = 검증 성능 10번 이상 개선 안되면 학습 조기중단
             # --> 결과: 과적합 줄어듦

# 최고의 검증된 손실함수
best_val_loss = float("inf") # inf = 무한대

# 최고의 검증된 모델 가중치 + 편향 저장
best_state = None

# 가장 낮은 검증 손실값 기록
best_epoch = 0

# 검증 손실값이 연속으로 개선되지 않은 횟수 저장
wait = 0

# 학습기록 저장
history = []

print(model)

# 4. 모델 학습 루프 구현 ----------------------------------------------------------------------------------------

# 학습 시작
for epoch in range(2, EPOCHS + 1):
  # Train
  model.train()
  train_loss_sum = 0.0

  for X_batch, y_batch in train_loader:
    X_batch = X_batch.to(device)
    y_batch = y_batch.to(device)

    # 이전 Graient 초기화
    optimizer.zero_grad()

    # 순전파
    logits = model(X_batch)

    # 손실 계산
    loss = criterion(logits, y_batch)

    # 역전파
    loss.backward()

    # 가중치 업데이트
    optimizer.step()

    train_loss_sum += (
      loss.item() * X_batch.size(0)
    )
  
  train_loss = (
    train_loss_sum / len(train_dataset)
  )  

  # Validation 
  model.eval()

  with torch.no_grad():
    Xv = X_val_tensor.to(device)
    yv = y_val_tensor.to(device)

    val_logists = model(Xv)
    val_loss = criterion(
      val_logists, yv
    ).item()

    val_prob = torch.sigmoid(
      val_logists
    ).cpu().numpy().ravel()

  val_pred = (val_prob >= 0.5).astype(int)
  
  val_f1 = f1_score(
    y_val,
    val_pred,
    zero_division=0
  )  

  history.append({
    "epoch": epoch,
    "train_loss": train_loss,
    "val_loss": val_loss,
    "val_f1": val_f1
  })

  print(
    f"Epoch {epoch:03d} || "
    f"Train Loss: {train_loss:.4f}"
    f"Val Loss: {val_loss:.4f}"
    f"Val F1: {val_f1:.4f}"
  )

  # Early Stopping
  if val_loss < best_val_loss - 1e-5:
    best_val_loss = val_loss
    best_state = deepcopy(model.state_dict())
    best_epoch = epoch
    wait = 0
  else:
    wait += 1
  
  
  if wait >= PATIENT:
    print("Early Stopping 실행")
    break
  
# 가장 좋은 검증 손실 얻은 모델 복원
assert best_state is not None
model.load_state_dict(best_state)

print("Best Epoch: ", best_epoch)
print("Best Validation Loss: ", best_val_loss)      

# 5. 학습 곡선 그리기 -------------------------------------------------------------------------------------------

# 6. 최적 모델 평가 및 저장 -------------------------------------------------------------------------------------