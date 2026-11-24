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



# 3. 모델 + 손실함수 + 옵티마이저 설정 ---------------------------------------------------------------------------

# 4. 모델 학습 루프 구현 ----------------------------------------------------------------------------------------

# 5. 학습 곡선 그리기 -------------------------------------------------------------------------------------------

# 6. 최적 모델 평가 및 저장 -------------------------------------------------------------------------------------