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
@asynccontextmanager # @ = 데코레이터(추가 기능)
                     # asynccontextmanager = 비동기 컨텍스트 관리
async def lifespan(app: FastAPI): # async def  = 비동기 함수
                                  # lifespan() = 서버와 시작 종료 관리
                                  # app = FastAPI 애플리케이션 전달
                                  # FastAPI = Python API 서버
  # 전처리 객체
  preprocessor = joblib.load( # joblib  = 파이썬객체 or ML모델 저장하거나 불러옴 
                              # .load() = 객체 불러옴
    MODELS / "preprocessor.joblib" # 전처리파일 겅로 = C:\projects\projectAI\GangNaengI_AI\models\preprocessor.joblib
  )

  # 로지스틱 회귀 모델
  lr_model = joblib.load( # joblib  = 파이썬객체 or ML모델 저장하거나 불러옴
                          # .load() = 객체 불러옴
    MODELS / "logistic_regression.joblib" # 로지스틱회귀모델 = 
  )                                       # C:\projects\projectAI\GangNaengI_AI\models\logistic_regression.joblib

  # XGBoost
  xgb_model = joblib.load( # joblib  = 파이썬객체 or ML모델 저장하거나 불러옴
                           # .load() = 객체 불러옴
    MODELS / "xgboost.joblib" # XGBoost모델 경로 =
  )                           # C:\projects\projectAI\GangNaengI_AI\models\xgboost.joblib

  # 전처리 후 입력특성개수
  input_dim = len( # input_dim = 모델 입력특성개수 저장
                   # len() = 길이
    preprocessor.get_feature_names_out() # preprocessor = 학습할 때 사용한 전처리
  )                                      # .get_feature_names_out() = 전처리 이후 출력 특성명 반환

  # 파이토치 MLP
  mlp_model = PerioMLP( # mlp_model = MLP 모델
                        # PeroMLP   = 치주질환 예측용 인공신경망
    input_dim=input_dim # input_dim = 모델 입력특성개수 저장
  )

  # 학습된 가중치 로딩
  state_dict = torch.load( # state_dict = 학습된 가중치
                           # .torch  = PyTorch
                           # .load() = 객체 불러옴
    MODELS / "mlp_model.pth", # 학습된 가중치 경로 = C:\projects\projectAI\GangNaengI_AI\models\mlp_model.pth
    map_location="cpu", # map_location = 데이터 불러올 장치
    weights_only=True   # weights_only = 제한된 역직렬화 방식 사용 여부
  )                     # 직렬화: 프로그램 사용하는 객체를 저장하거나 전송할 수 있는 형태로 반환
                        # 역직렬화: 저장된 데이터를 다시 프로그램에 사용할 수 객체로 복원

  # 가중치 적용
  mlp_model.load_state_dict(state_dict) # mlp_model = MLP 모델
                                        # .load_state_dict() = 모델에 저장된 상태 적용
                                        # state_dict = 가중치 적용
  
  # MLP 모델 평가모드로 전환
  mlp_model.eval() # mlp_model = MLP 모델
                   # .eval() = 평가모드
                   # 모드 종류:
                   # train() = 학습모드
                   #           Dropout 활성화
                   #           현재를 통계에 사용
                   # eval()  = 평가모드
                   #           Dropout 비활성화
                   #           저장된 통계에 사용         

  # 모델 저장
  artifacts.update({ # artifacts = 모델 및 전처리 객체 보관
                     # .update() = 새로운 key와 value 추가
    "preprocessor": preprocessor, # preprocessor = 전처리 객체
    "lr": lr_model,   # lr  = 로지스틱회귀 모델
    "xgb": xgb_model, # xgb = XGBoost 모델
    "mlp": mlp_model  # mlp = MLP 모델
  })

  print("GangnaengI AI 모델 로딩 종료")

# 3. FastAPI와 CORS 설정 ---------------------------------------------------------------------------------------------

# 4. 서버 상태 확인 API ----------------------------------------------------------------------------------------------

# 5. 예측결과 변환 ---------------------------------------------------------------------------------------------------

# 6. 핵심 API -------------------------------------------------------------------------------------------------------
