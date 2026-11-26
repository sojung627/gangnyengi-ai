# 1. 라이브러리 및 경로 설정 ------------------------------------------------------------------------------------------

from pathlib import Path # pathlib = 파일 및 폴더 경로 관리
                         # Path = 파일 및 폴더 경로 생성
from contextlib import asynccontextmanager # contextlib = 컨텍스트 관리자 생성 및 관리
                                           # asynccontextmanager = 비동기 컨텍스트 관리자 생성
import sys # Python실행환경 + 시스템관련기능 제공

import joblib # joblib = 파이썬객체 or ML모델 저장하거나 불러옴 
import numpy as np  # numpy  = 배열 및 수치연산 관리
import pandas as pd # pandas = 표 데이터 분석 및 가공
import torch # torch = PyTorch 딥러닝 라이브러리

from fastapi import FastAPI # fastapi = Python 기반 API 서버
from fastapi.middleware.cors import CORSMiddleware # .middleware = 요청과 응답 사이에서 수행될 기능들 관리
                                                   # .cors = CORS 관련 기능 제공
                                                   # CORSMiddleware = CORS 정책 설정 및 관리
                                                   # CORS: Cross Origin Resource Sharing
                                                   #       Origin   - 출처
                                                   #       Resource - 자원
                                                   #       Sharing  - 공유

from schemas import ( # schemas = 입출력데이터 구조 정의
  PredictionInput,   # PredictionInput    = 사용자 입력데이터 검증 
  PredictionResponse # PredictionResponse = 전체모델 예측응답구조 정의
)

# 프로젝트 경로 설정
ROOT = Path(__file__).resolve().parent.parent # 프로젝트 기본 경로: C:\projects\projectAI\GangNaengI_AI
                                              # Path()     = 경로 생성
                                              # __file__   = 현재 파이썬 경로
                                              # .resolve() = 절대경로
                                              # .parent = 부모 폴더
MODELS = ROOT / "models" # 모델 경로: C:\projects\projectAI\GangNaengI_AI\models

# 기본 MLP 
sys.path.insert(0, str(ROOT / "dl")) # sys = 파이썬실행환경 관리
                                     # .path = 파이썬모듈 탐색경로 목록
                                     # .insert() = 지정한 인덱스에 데이터 삽입
                                     # 0     = 삽입할 인덱스
                                     # str() = 객체를 String으로 반환
                                     # ROOT / "dl" = 딥러닝 폴더명

from model import PerioMLP # model = 딥러닝모델 구조 정의
                           # PerioMLP = 치주질환 예측 인공신경망

# 학습된 모델의 전처리 객체 보관
artifacts = {} 

# 2. 학습된 모델 불러오기 ---------------------------------------------------------------------------------------------

# 서버시작 시 모델 로딩
@asynccontextmanager
async def lifespan(app: FastAPI):
  # 전처리 객체
  preprocessor = joblib.load(
    MODELS / "preprocessor.joblib"
  )

  # 로지스틱 회귀 모델
  lr_model = joblib.load(
    MODELS / "logistic_regression.joblib"
  )

  # XGBoost
  xgb_model = joblib.load(
    MODELS / "xgboost.joblib"
  )

  # 전처리 후 입력특성개수
  input_dim = len(
    preprocessor.get_feature_names_out()
  )

  # 파이토치 MLP
  mlp_model = PerioMLP(
    input_dim=input_dim
  )

  #
  state_dict = torch.load(
    MODELS / "mlp_model.pth",
    map_location="cpu",
    weights_only=True
  )

  #
  mlp_model.load_state_dict(state_dict)
  #
  mlp_model.eval()

  # 모델 저장
  artifacts.update({
    "preprocessor": preprocessor,
    "lr": lr_model,
    "xgb": xgb_model,
    "mlp": mlp_model
  })

  print("GangnaengI AI 모델 로딩 종료")

# 3. FastAPI와 CORS 설정 ---------------------------------------------------------------------------------------------

# 4. 서버 상태 확인 API ----------------------------------------------------------------------------------------------

# 5. 예측결과 변환 ---------------------------------------------------------------------------------------------------

# 6. 핵심 API -------------------------------------------------------------------------------------------------------
