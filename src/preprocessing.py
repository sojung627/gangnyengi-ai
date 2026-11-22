from pathlib import Path
import re
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
  OneHotEncoder,
  StandardScaler
)

# 프로젝트 최상위 폴더
ROOT = Path(__file__).resolve().parent.parent

PROCESSED = ROOT / "data" / "processed"
MODELS = ROOT / "models"

PROCESSED.mkdir(parents=True, exist_ok=True)
MODELS.mkdir(parents=True, exist_ok=True)

# 머지한 데이터 읽기
df = pd.read_csv(PROCESSED / "nhanes_merged.csv")

print("원본 데이터 크기: ", df.shape)