# 1. 라이브러리 및 경로 설정 ------------------------------------------------------------------------------------------

import os # os = 운영체제 관련 기능
from dotenv import load_dotenv # dotenv = .env 파일 환경변수 불러오기
                               # load_dotenv = .env 환경변수 실행환경에 로딩
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

# FastAPI 앱 생성
app = FastAPI( # FastAPI() = FastAPI 객체 저장
  title="GangnaengI AI", # title = API 제목
  description="Periodontal finding classification API", # description = API 설명
  version="1.0.0",  # version  = API 버전
  lifespan=lifespan # lifespan[왼쪽]   = 서버 생명주기 관리 함수 지정
)                   # lifespan[오른쪽] = 서버 시작 및 종료 

# .env 불러오기
load_dotenv(ROOT / ".env") # load_dotenv() = .env 환경변수 실행환경에 로딩

# 허용할 프론트엔드 주소
CORS_ORIGINS = [ # CORS_ORIGINS = .env 변수
                 #                --> 웹 도메인
  origin.strip() # origin   = 출처들
                 # .strip() = 공백 및 줄바꿈 제거
  for origin in os.getenv("CORS_ORIGINS", "").split(",") # origin = 출처들
                                                         # os = 운영체제 및 환경변수 관리
                                                         # .getenv() = 환경변수 값 가져오기
                                                         # .split(",") = , 제거 
  if origin.strip() # .strip() = 공백 및 줄바꿈 제거
]

# CORS 설정
# CORS - 웹이 다른 출처를 서버에 요청할 수 있는가를 제어하는 정책 중 하나
app.add_middleware( # app = FastAPI 애플리케이션
                    # .add_middleware() = 애플리케이션 미들웨어 추가
  CORSMiddleware, # CORSMiddleware = CORS 정책 설정 및 처리
  allow_origins=CORS_ORIGINS, # allow_origins = 허용할 출처
  allow_methods=["GET", "POST"], # allow_methods = 허용할 HTTP 메서드 지정
  allow_headers=["Content-Type"] # allow_headers = 허용할 요청 헤더 지정
)

# 4. 서버 상태 확인 API ----------------------------------------------------------------------------------------------

# 서버상태 확인
@app.get("/health") # @ = 데코레이터
                    # .get() = GET으로 요청
def health():
  return{
    # 서버작동 상태 == 정상
    "status": "ok", 
    # 모델로딩 여부
    "model_loaded": len(artifacts) == 4 # model_loaded = 모델로딩 여부
  }                                     # len() = 길이
                                        # artifacts = 모델 및 전처리 객체 
                                        # == 4 = 4개면 True | 아니면 False

# 5. 예측결과 변환 ---------------------------------------------------------------------------------------------------

# 모델에서 반환한 확률을 양성 음성 라벨로 변환

# 예측확률
THRESHOLD = 0.3

# 예측 결과 반환
# 0.3 이상이면 1 | 0.3 이하면 0
def format_prediction(probability):
  # 예측확률을 소수로 변환 
  probability = float(probability) # probability = 예측확률
                                   # 변환 전: 0.45
                                   # 변환 후: 0.4446475675685 

  # 예측결과 반환
  return { # return{} = dict로 반환
    "probability": float(probability), # 예측확률 소수점
    "prediction": int( # prediction = 모델 최종 예측라벨
      probability >= THRESHOLD # 예측확률 소수점 >= 예측확률
    ),
    "threshold": THRESHOLD # threshold = 분류 임계값
  }

# 6. 핵심 API -------------------------------------------------------------------------------------------------------

# 모델 예측 API
@app.post(
  "/predict",
  response_model=PredictionResponse
)

def predict(data: PredictionInput):
  # 사용자의 입력을 NHANES 컬럼명으로 변환
  input_df = pd.DataFrame([{
    "RIDAGEYR": data.age,    # RIDAGEYR = 나이(연도)
    "RIAGENDR": data.gender, # RIAGENDR = 성별
    "SMQ020": data.ever_smoked, # SMQ020 = 평생 흡연 100개 이상
    "SMQ040": ( # SMQ040 = 현재 흡연빈도
      data.smoking_frequency
      if data.smoking_frequency is not None
      else np.nan
    )
  }])
  # 데이터 변수
  # RIDAGEYR = 나이(연도)          | int
  # RIAGENDR = 성별                | 남성[1]  여성[2]
  # SMQ020   = 평생 흡연 100개 이상 | YES[1]   NO[2]
  # SMQ040   = 현재 흡연빈도        | 매일[1]  가끔[2]  안함[3]
  
  # 기존 전처리 객체 적용
  X = artifacts["preprocessor"].transform(
    input_df
  )

  # PyTorch와 ML모델 모두 사용할 수 있게 반환
  if hasattr(X, "toarray"):
    X = X.toarray()

  # 
  X = np.asarray(X, dtype=np.float32)

  #
  if not np.isfinite(X).all():
    raise ValueError(
      "전처리 결과에 유효하지 않은 값이 있습니다."
    )
    
  # 로지스틱 회귀 모델 예측
  lr_prob = artifacts["lr"].predixt_proba(
    X
  )[0, 1]

  # XGBoost 모델 예측
  xgb_prob = artifacts["xgb"].predixt_proba(
    X
  )[0, 1]

  # PyTorch 모델 예측
  with torch.no_grad():
    #
    X_tensor = torch.tensor(
      X,
      dtype=torch.float32
    )
    #
    logits = artifacts["mlp"](X_tensor)

    #
    mlp_prob = torch.sigmoid(
      logits
    ).item()

  # 모델별 예측 결과 반환
  return {
    "logistic_regression": format_prediction(
      lr_prob
    ),
    "xgboost": format_prediction(
      xgb_prob
    ),
    "pytorch_mlp": format_prediction(
      mlp_prob
    ),
    "disclaimer": (
      "연구 예측 결과 입니다."
    )
  }  