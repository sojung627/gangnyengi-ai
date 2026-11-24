# 1. MLP 신경망 설계 ------------------------------------------------------------------------------------------ 

import torch         # Pytorch 라이브러리
from torch import nn # Pytorch 신경망의 모듈 nn

# 치주 신경망 
class PerioMLP(nn.Module): # nn.Module = Pytorch의 기본 클래스 
                           #             1. 신경망 가중치 편향을 관리 
                           #             2. 학습모드 평가모드 전환
                           #             3. 모델 저장
                           #             4. GPU CPU간 모델 이동
  def __init__(self, input_dim): # __init__ = 객체 생성시 자동 초기화
                                 # self = 방금 생성된 객체가 나다
    super().__init__() # super()    = 부모 클래스에 접근 
                       # 부모 클래스 = nn.Modual

    self.network = nn.Sequential( # self.network    = 현 객체에 network라는 속성을 생성하라
                                  # nn.Sequential() = 신경망 층을 설계한 순서대로 실행하라
      nn.Linear(input_dim, 32), # nn.Liner() = 완전 연결층
                                # 완전연결층  = 입력값 x 가중치 + 편향 
                                # input_dim  = 입력데이터 특성 개수
                                # 32 = 출력뉴런 개수 
                                # 뜻: input_dim을 32개로 반환
      nn.ReLU(), # 렐루함수: 비선형 패턴 학습할 수 있게 해주는 활성화 함수

      nn.Linear(32, 16), # 아까 받은 출력뉴런 32개를 16개로 바꿈
      nn.ReLU(), # 그 16개를 렐루함수에 적용

      nn.Dropout(p=0.2), # nn.Dropout() = 일부 뉴런을 무작위로 0으로 바꿈(과적합 예방)
                         # p=0.2 = 각 뉴런당 0으로 대체될 확률이 20%
      
      nn.Linear(16, 1) # 16개를 1개로 바꿈
    )                  # 출력층 결과: 1개

  def forward(self, x): # x = 신경망에 전달할 입력데이터
    return self.network(x) # 리턴한 결과: x를 모든 계층에 순서대로 통과시킨 뒤 최종 예측점수에 반환