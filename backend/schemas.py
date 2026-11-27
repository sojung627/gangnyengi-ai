from typing import Literal # typing  = 자료형 힌트 기능 제공
                           # Literal = 허용되는 값을 특정 값으로 변환

from pydantic import ( # pydantic = 데이터구조 정의 or 유효성검증
  BaseModel, # BaseModel = 데이터모델 정의 및 검증
  Field, # Field = 필드 기본값과 검증 설정
  model_validator # model_validator = 모델 전체 필드의 유효성검증 설정
)

# 사용자가 직접 입력 - 나이, 성별, 흡연경험 유무, 현재흡연 빈도
class PredictionInput(BaseModel): # PredictionInput = 예측 입력데이터 구조 정의
                                  # BaseModel = 데이터 정의 및 검증
  # 나이 - 30~80세
  age: int = Field( # Field = 필드 기본값 및 검증 설정
    ge=30, # Geater Than or Equl | 크거나 같다(이상)
           # 해석: ge 최대 30까지 입력 허용
    le=80  # Less Than or Equl   | 작거나 같다(이하)
  )        # 해석: le 최대 80까지 입력 허용
  # 성별 - 남성[1] | 여성[2]
  gender: Literal[1, 2] # Literal = 입력 가능한 값 설정
                        # [1, 2]  = 허용되는 값
  # 흡연경험 유무 - 유[1] | 무[2]                      
  ever_smoked: Literal[1, 2] # Literal = 입력 가능한 값 설정
                             # [1, 2]  = 허용되는 값
  # 현재흡연 빈도 - 매일[1] | 가끔[2] | 안함[3]
  smoking_frequency: Literal[1, 2, 3] | None = None # Literal    = 입력 가능한 값 설정
                                                    # [1, 2, 3]  = 허용되는 값 
                                                    # | = 여러타입 중 하나 사용
                                                    # None=None  = None값도 허용 + 기본값도 None값
  # 데이터 변수
  # RIDAGEYR = 연령                | int
  # RIAGENDR = 성별                | 남성[1]  여성[2]
  # SMQ020   = 평생 흡연 100개 이상 | YES[1]   NO[2]
  # SMQ040   = 현재 흡연빈도        | 매일[1]  가끔[2]  안함[3]

  # 흡연경험 및 현재흡연빈도 검증
  @model_validator(mode="after") # @ = 데코레이터 - 추가기능 적용
                                 # @model_validator() = 모델 단위 유효성 검증 설정
                                 # mode  = 검증실행 시점 설정
                                 # after = 개별 검증 끝난 뒤 실행하라
                                 #         --> 모델 단위 유효성 검증을
  # 흡연 관련 데이터 검증                               
  def check_smoking(self): # self = 현재 생성된 클래스 인스턴스 자신
    # 흡연경험이 있다면
    if self.ever_smoked == 1:
      # 흡연 빈도를 입력하지 않았다면
      if self.smoking_frequency is None:
        # 흡연경험이 있고 흡연빈도 입력 안했다면 강제 에러
        raise ValueError( # raise = 강제 발생
                          # ValueError = 이상한 값에 대한 에러
          "흡연경험이 있다면 흡연빈도를 선택하세요."
        )
    
    # 흡연경험이 없다면
    if self.ever_smoked == 2:
      # 흡연 빈도를 입력하지 않았다면
      if self.smoking_frequency is None:
        # 흡연경험이 없고 흡연빈도 입력 안했다면 강제 에러
        raise ValueError( # raise = 강제 발생
                          # ValueError = 이상한 값에 대한 에러
          "흡연경험이 없다면 흡연빈도를 입력하지 마세요."
        )  
    return self # PredictionInput 반환
                # 사용자가 직접 입력 --> 나이, 성별, 흡연경험 유무, 현재흡연 빈도

# 모델 1개당 예측 결과
class ModelPrediction(BaseModel): # ModelPrediction = 모델 1개당 예측 결과
                                  # BaseModel = 데이터 정의 및 검증
  # 모델예측 확률
  probability: float = Field( # Feild() = 필드검증 조건 설정
    ge=0, # ge = 이상
    le=1  # le = 이하
  )       # 해석: 모델예측 확률을 소수점으로 받아라
          #       소수점도 0~1 사이로만 받아라
  # 모델 최종 예측 결과
  prediction: Literal[0, 1] # Literal = 입력 가능한 값 설정
                            # [0, 1]  = 0 or 1
  # 모델 분류 임계값
  threshold: float = Field( # Field() = 필드검증 조건 설정
    ge=0, # ge = 이상
    le=1  # le = 이하
  )       # 해석: 모델 분류 임계값을 소수점으로 받아라
          #       단 0~1 사이의 소수점만 받아라

# 모델 3개 전부 예측 결과
class PredictionResponse(BaseModel): # PredictionResponse = 모델 3개 전부 예측 결과
                                     # BaseModel = 데이터 정의 및 검증
  # 로지스틱 회귀 모델
  logistic_regression: ModelPrediction # logisic_regression = 로지스틱 회귀 모델
                                       # ModelPrediction = 모델 1개당 예측 결과
  # XGBoost 모델
  xgboost: ModelPrediction # xgboost = XGBoost 모델(앙상블 모델)
                           # ModelPrediction = 모델 1개당 예측 결과
  # MLP 모델
  pytorch_mlp: ModelPrediction # pytorch_mlp = MLP 모델
                               # ModelPrediction = 모델 1개당 예측 결과
  # 면책 및 주의사항 안내
  disclaimer: str # disclaimer = 면책 + 주의사항
                  # str = String