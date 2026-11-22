from pathlib import Path # pathlib = 파일 및 폴더 라이브러리
import re # re = 정규표현식 라이브러리
import joblib # joblib = ML모델을 파일로 저장하거나 불러오는 라이브러리
import numpy as np  # numpy  = 배열 및 수치 계산용 라이브러리
import pandas as pd # pandas = 표 형태의 데이터 가공 라이브러리

from sklearn.model_selection import train_test_split # sklearn.model_selection = ML 모델 평가용 데이터 분할 및 검증 모듈
                                                     # train_test_split = 데이터 학습용 / 테스트용으로 나누는 함수
from sklearn.compose import ColumnTransformer # sklearn.compose   = 여러 데이터 변환 작업을 결합하는 모듈
                                              # ColumnTransformer = 데이터의 컬럼마다 서로 다른 전처리 적용하는 클래스
from sklearn.pipeline import Pipeline # sklearn.pipeline = 데이터 처리 단계를 순서대로 하는 모듈 
                                      # Pipeline = 전처리부터 모델 학습 까지 연결하는 클래스
from sklearn.preprocessing import ( # sklearn.preprocessing = ML용 데이터 전처리하는 모듈
  OneHotEncoder,                    # OneHotEncoder  = 범주형 데이터를 0과 1로 변환하는 클래스(이진법용) 
  StandardScaler                    # StandardScaler = 데이터 평균을 0으로 맞추고 표준편차를 1로 만드는 클래스(표준화용)
)

# 프로젝트 최상위 폴더
ROOT = Path(__file__).resolve().parent.parent # Path(__file__) = 현 파일을 Python 경로로
                                              # .resolve() = 절대경로로 변환
                                              # .parent    = 부모 폴더
                                              # 해석: GangNyaengI_AI 폴더를 ROOT에 저장함

PROCESSED = ROOT / "data" / "processed" # PROCESSED = C:\projects\projectAI\GangNaengI_AI\data\processed
MODELS = ROOT / "models"                # MODELS = C:\projects\projectAI\GangNaengI_AI\models

PROCESSED.mkdir(parents=True, exist_ok=True) # POCESSED 폴더를 생성할 때 부모 폴더 없음 부모 폴더도 생성하라
MODELS.mkdir(parents=True, exist_ok=True)    # 이미 있으면 생성하지 말고 오류도 내지 마라

# 머지한 데이터 읽기
df = pd.read_csv(PROCESSED / "nhanes_merged.csv") # 데이터 머지를 저장한 파일 = nhanes_merged.csv
                                                  # 그 파일 위치를 df에 저장하며 읽으라고 함
                                                  # df = C:\projects\projectAI\GangNaengI_AI\data\processed\nhanes_merged.csv

print("원본 데이터 크기: ", df.shape) # df.shape = df의 행과 열을 튜플로 반환
                                     # ex) "원본 데이터 크기: (5000, 30)"
                                     # --> 5000행 30열