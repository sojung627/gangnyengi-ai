# 1. 라이브러리 및 경로 설정 -------------------------------------------------------------------------------------

from pathlib import Path 
from copy import deepcopy
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

from sklearn.metrics import (
  accuracy_score,
  precision_score,
  recall_score,
  f1_score,
  average_precision_score
)

from model import PerioMLP

# 프로젝트 경로
ROOT = Path(__file__).resolve().parent.parent

PROCESSED = ROOT / "data" / "processed"
MODELS = ROOT / "models"
RESULTS = ROOT / "results"

MODELS.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

# 재현 가능한 실험을 위한 시드
torch.manual_seed(42)
np.random.seed(42)

# CPU or GPU
device = torch.device(
  "cuda" if torch.cuda.is_available() else "cpu"
)

print("사용 중지: ", device)

# 2. 데이터 부르기 + Tensor 변환 --------------------------------------------------------------------------------

# 3. 모델 + 손실함수 + 옵티마이저 설정 ---------------------------------------------------------------------------

# 4. 모델 학습 루프 구현 ----------------------------------------------------------------------------------------

# 5. 학습 곡선 그리기 -------------------------------------------------------------------------------------------

# 6. 최적 모델 평가 및 저장 -------------------------------------------------------------------------------------