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
assert X_val_tensor.shape[0] == X_val_tensor.shape[0]     # .shape[0] = 행의 개수 
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
for epoch in range(1, EPOCHS + 1): # Epoch = 학습데이터 전부 학습 1회
                                   # 100번 학습 시키기
  # Train
  model.train() # .train() = 모델학습 모드 전환
                #            Dropout = 활성화
                #            사용목적 = 모델 학습
                #            기울기 제거 = 별도 설정에 따라 다름
  train_loss_sum = 0.0 # = 현재 Epoch의 전체 학습 손실값으로 누적
                       # 0.0 = 새로운 Epoch가 시작될 때 마다 Epoch 손실값 누적되지 않게 0으로 초기화

  for X_batch, y_batch in train_loader: # X_batch = 현 배치의 학습용 입력데이터
    X_batch = X_batch.to(device)        # y_batch = 현 배치의 학습용 정답라벨
    y_batch = y_batch.to(device)        # .to()   = Tensor의 연산장치 이동

    # 이전 Graient 초기화 --> = 이전 기울기 제거
    optimizer.zero_grad() # .zero_grad() = 이전 역전파에서 계산된 기울기를 초기화
                          #                내부적 기울기를 0이나 None으로

    # 순전파
    # --> 입력데이터를 신경망을 처음부터 끝까지 순서대로 전달하면서 예측값을 계산
    # --> 방향: 입력층 -> 은닉층 -> 출력층
    logits = model(X_batch) 

    # 손실 계산
    loss = criterion(logits, y_batch) # criterion() = 앞에서 생성한 손실함수 객체
                                      # criterion() = BCEWithLogitsLoss

    # 역전파
    # --> 출력층에서 입력층 방향으로 각 가중치와 편향이 손실값에 영향을 얼마나 미치는지 미분을 통해 계산
    # --> 방향: 출력층 -> 은닉층 -> 입력층
    loss.backward()

    # 가중치 업데이트
    optimizer.step() # .step() = 역전파에서 계산된 기울기로 모델의 가중치랑 편향 업데이트

    # 학습 손실값 누적
    train_loss_sum += (
      loss.item() * X_batch.size(0) 
    )

  # 전체 학습 데이터의 평균 손실값 계산
  train_loss = (
    train_loss_sum / len(train_dataset)
  )  

  # Validation 
  model.eval() # .eval() = 모델을 평가모드로 전환
               #           Dropout = 비활성화
               #           사용목적 = 모델검증 및 예측
               #           기울기 계산 = 별도 설정 따름 

  with torch.no_grad(): # with = 특정 기능이나 설정을 지정한 코드에서만 처리하라
                        # torch.no_grad() = 자동미분 연산기록 비활성화
    Xv = X_val_tensor.to(device) # Xv = 검증용 입력데이터 저장
    yv = y_val_tensor.to(device) # yv = 검증용 정답라벨 저장
                                 # .to() = Tensor에 지정한 연산장치로 이동 --> GPU or CPU

    val_logists = model(Xv) # val_logists = 검증데이터 예측 점수 저장
    val_loss = criterion(   # val_loss = 검증 데이터 평균 손실값 저장
      val_logists, yv 
    ).item() # .item() = 계산된 손실값을 Tensor에서 --> 숫자로 변환

    val_prob = torch.sigmoid( # val_prob = 검증데이터 예측 확률 저장
      val_logists
    ).cpu().numpy().ravel() # .cpu() = Tensor를 CPU로 이동시킴
                            # .numpy() = Tensor를 --> NumPy로 변환
                            # .ravel() = 다차원 NumPy --> 1차원 NumPy로 변환

  val_pred = (val_prob >= 0.5).astype(int) # val_pred = 검증데이터 예측 라벨 저장
                                           # val_prob >= 0.5 = 치주질환 여부 판단하는 분류 기준값
                                           # .astype() = NumPy 배열 자료형(int)으로 변경
  
  val_f1 = f1_score( # val_f1 = 검증데이터 F1 스코어 저장
    y_val,    # 검증용 정답라벨
    val_pred, # 모델이 예측한 검증용 정답라벨
    zero_division=0 # = 평가 지표를 계산 안될 떄 0으로 처리하라
  )  

  # 학습 CSV 파일 저장
  history.append({ # .append() = 리스트에 추가
    "epoch": epoch, # epoch = 학습의 반복횟수 저장
    "train_loss": train_loss, # train_loss = 평균 학습 손실값 저장
    "val_loss": val_loss, # val_loss = 평균 검증 손실값 저장
    "val_f1": val_f1 # val_f1 = 검증 F1 스코어 저장
  })

  print(
    f"Epoch {epoch:03d} || " # epoch:03d = 정수 최소 3자리 출력
    f"Train Loss: {train_loss:.4f}" # train_loss:.4f = 학습 손실값을 소수점 4자리 출력
    f"Val Loss: {val_loss:.4f}" # val_loss:.4f = 검증 손실값을 소수점 4자리 출력
    f"Val F1: {val_f1:.4f}" # val_f1:.4f = 검증 F1 스코어 소수점 4자리
  )

  # Early Stopping
  if val_loss < best_val_loss - 1e-5: # val_loss = Epoch 검증 손실값
                                      # best_val_loss = 가장 낮은 검증 손실값
    best_val_loss = val_loss
    best_state = deepcopy(model.state_dict()) # best_state    = 검증 손실값이 가장 낮은 모델
                                              # deepcopy()    = 객체 내부까지 깊게 복사 (원본은 영향 x)
                                              # .state_dict() = 모델 가중치와 편향, 영구 버퍼 반환
    # 최적 Epoch 기록
    best_epoch = epoch
    wait = 0 # 대기횟수 초기화
  else:
    wait += 1 # 검증 손실 개선 안되면 대기 1회 증가
  
  # 검증 손실값 10회 이상 개선 안되었는가
  if wait >= PATIENT:
    print("Early Stopping 실행") # 학습 조기 종료
    break
  
# 가장 좋은 검증 손실 얻은 모델 복원
assert best_state is not None     # assert = 조건에 맞으면 True로 다음 코드 실행
                                  #          아니면 AssertError 발생
model.load_state_dict(best_state) # 가장 좋은 검증 손실 모델

print("Best Epoch: ", best_epoch) # 가장 낮은 검증 손실값을 기록한 Epoch 번호
print("Best Validation Loss: ", best_val_loss) # 지금까지의 최저 검증 손실값  

# 5. 학습 곡선 그리기 -------------------------------------------------------------------------------------------

# 학습기록 DF로 변환
history_df = pd.DataFrame(history) # history = 각 Epoch 학습손실값 + 검증손실값 + F1스코어 저장된 리스트

# CSV 저장
history_df.to_csv( # .to_csv() = DF를 CSV로 저장
  RESULTS / "dl_training_history.csv", # CSV 경로 = C:\projects\projectAI\GangNaengI_AI\results\dl_training_history.csv
  index=False # index = 행 인덱스 저장 여부
)             # True = 저장 / False = 저장 x

# Loss 그래프
plt.figure(figsize=(9, 5)) # .figure() = 그래프 생성
                           # figsize   = 그래프 사이즈

plt.plot( # plot() = 선 그래프
  history_df["epoch"], # DF 중 epoch 컬럼 가져와서 "학습반복 횟수를 X축에 저장"
  history_df["train_loss"], # DF 증 train_loss 컬럼 가져와서 "학습손실값을 Y축에 저장"
  label="Train Loss" # label = 그래프 범례에 표시할 이름
)

plt.plot( # plot() = 선 그래프
    history_df["epoch"], # DF 중 epoch 컬럼 가져와서 "학습반복 횟수를 X축에 저장"
    history_df["val_loss"], # DF 증 val_loss 컬럼 가져와서 "검증손실값을 Y축에 저장"
    label="Validation Loss" # label = 그래프 범례에 표시할 이름
)

plt.axvline( # axvline() = 지정한 X축 위치에 수직선 그림
    best_epoch, # X축 = 가장 좋은 검증손실값 가진 Epoch
    color="gray", # 색상 = 그레이
    linestyle="--", # 선 = 파선
    label="Best Epoch" # label = 그래프명
)

plt.xlabel("Epoch") # .xlabe()  = X축 이름 지정
plt.ylabel("Loss")  # .ylabel() = Y축 이름 지정
plt.title("MLP Training Curve") # .title() = 그래프 제목 지정
plt.legend() # .legend() = 라벨명 및 선색상이나 모양을 범례로 표기 
plt.tight_layout() # tight_layout() = 여백 자동조절

# 이미지 저장
plt.savefig( # savefig() = 이미지 저장
    RESULTS / "dl_learning_curve.png", # 이미지 경로 = C:\projects\projectAI\GangNaengI_AI\results\dl_learning_curve.png
    dpi=150 # dpi = 1인치당 점의 개수
)           # 해석: 1인치당 점이 150개

plt.show() # .show() = 그래프 출력

# 6. 최적 모델 평가 및 저장 -------------------------------------------------------------------------------------

# 평가모드
model.eval()

with torch.no_grad(): # with = 특정 범위로 제한
                      # no_grad() = 자동 미분 연산 기록 비활성화
    logits = model(X_val_tensor.to(device)) # 순전파 예측확률 계산

    probabilities = torch.sigmoid( # probabilities = 환자별 치주질환 예측 확률 저장
                                   # .sigmoid() = 모델 예측 점수 0~1 사이 확률값으로 변환
        logits
    ).cpu().numpy().ravel() # .cpu() = Tensor를 CPU로 이동
                            # .numpy() = Tensor를 --> NumPy로
                            # .ravel() = 다차원 NP를 --> 일차원 NP로

predictions = (probabilities >= 0.5).astype(int) # predictions   = 예측라벨 저장
                                                 # probabilities = 시그모이드 함수로 변환된 치주질환 예측 확률
                                                 # 0.5 = 치주질환으로 인정하는 임계값
                                                 # .astype() = 타입 설정

# 성능 계산
scores = {
    "model": "PyTorch MLP", # 모델명 = PyTorch MLP
    "accuracy": float(accuracy_score( # = 정확도를 소수로
        y_val, predictions # y_val = 검증용 정답라벨
    )),                    # predictions = 모델이 생성한 예측라벨
    "precision": float(precision_score( # = 정밀도를 소수로
        y_val, predictions, zero_division=0 # zero_division = 계산할 수 없는 경우 0을 사용해
    )),
    "recall": float(recall_score( # = 재현율을 소수로
        y_val, predictions, zero_division=0
    )),
    "f1": float(f1_score( # = F1 스코어를 소수로
        y_val, predictions, zero_division=0
    )),
    "average_precision": float( # = 평균 정밀도를 소수로
        average_precision_score(
            y_val, probabilities # probabilities = 모델이 계산한 예측 확률
        )
    ),
    "best_epoch": int(best_epoch), # best_epoch = 최적 Epoch 번호 저장
    "best_val_loss": float(best_val_loss), # best_val_loss = 최적 검증 손실값 저장
    "input_dim": int(input_dim) # input_dim = 신경망에 입력되는 특성 개수
}

# 다층 퍼셉트론 검증 결과
print("\n=== MLP Validation Results ===")
for name, value in scores.items():
    print(f"{name}: {value}")

# 모델 가중치 저장
torch.save( # .save() = Tensor, dict, 모델 상태 등을 파일로 저장
    model.state_dict(), # state_dict = 모델의 가중치 + 편향 + 영구 버퍼를 딕셔너리로 반환
    MODELS / "mlp_model.pth" # 모델 가중치 = C:\projects\projectAI\GangNaengI_AI\models\mlp_model.pth
)

# 성능 평가 결과 저장
with open( # with   = 특정 범위로 지정
           # open() = 파일 열거나 생성
    RESULTS / "dl_validation_results.json", # 성능 평가 결과 = C:\projects\projectAI\GangNaengI_AI\results\dl_validation_results.json
    "w", # w = 쓰기모드
    encoding="utf-8" # 인코딩은 utf-8로 하라
) as f: # 별칭이 f
    json.dump( # .dump() = 데이터를 내보내거라 기록하라
        scores, f, 
        ensure_ascii=False, # ensure_ascii = 아스키를 벗어나는 문자를 이스케이프 문자로 변활할 것 이냐
                            # True = 변환 / False = 변환 x
        indent=2 # indent = 들여쓰기
    )

print("day04 - 딥러닝 모델 학습 완료!")