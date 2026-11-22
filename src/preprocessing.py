# 1. 라이브러리 및 파일 경로 설정 ----------------------------------------------------------------------------------- 

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

# 2. 치주검사 완료 대상자 선택 ---------------------------------------------------------------------------------------

# 치주검사 완료된 참가자만 선택
df = df[df["OHPDSTS"] == 1].copy() # 검사 완료된 상태 == 1
                                   # 검사 완료된 대상자만 따로 복사해서 df에 담아라

print("검사 완료 대상자: ", len(df)) # 검사 완료된 대상자가 몇 명인가

# 3. CAL과 PD 컬럼의 특수 코드 처리 ---------------------------------------------------------------------------------

# 치주검사 - 인접면 측정 컬럼
# 인접면   - D S P A
# D(원심협면) / S(근심협면) / P(원심설면) / A(근심설면)

# 임상적 부착 소실
# 치은퇴축 + 치주낭 깊이 = 임상적 부착 소실
# GR + PD = CAL
cal_cols = [
  col for col in df.columns # df의 컬럼이 조건에 해당하면 col에 담겠다
  if re.fullmatch(r"OHX\d{2}\LA[DSPA]", col) # re.fullmatch() = 문자열 전체가 정규표현식과 일치하라
]                                            # OHX = OHX로 시작하라
                                             # \d  = 0~9 숫자 한자리
                                             # {2} = 앞의 숫자가 정확히 두번 반복하라
                                             # \LA  = 숫자 다음은 LA라는 문자열
                                             # [DSPA] = D S P A 중 하나 포함

# 치주낭 깊이 
pd_cols = [
  col for col in df.columns # df의 컬럼이 조건에 해당하면 col에 담겠다
  if re.fullmatch(r"OHX\d{2}\PC[DSPA]", col) # re.fullmatch() = 문자열 전체가 정규표현식과 일치해라
]                                            # OHX = OHX로 시작하라
                                             # \d  = 0~9 숫자 한자리
                                             # {2} = 앞의 숫자가 정확히 두번 반복하라
                                             # \PC  = 숫자 다음은 PC라는 문자열
                                             # [DSPA] = D S P A 중 하나 포함                                             

print("CAL 컬럼 개수: ", len(cal_cols)) # CAL 컬럼 개수
print("PD 컬럼 개수: ", len(pd_cols))   # PD  컬럼 개수

assert len(cal_cols) > 0 # assert = 조건이 참이면 검사 / 거짓이면 AssertonError
                         # CAL컬럼 1개 이상이면 검사하라
assert len(cal_cols) == len((pd_cols)) # cal컬럼과 pd컬럼의 개수가 같다면 검사하라

# 숫자형으로 변환
cal_data = df[cal_cols].apply(pd.to_numeric, errors="coerce") # .apply = 각 컬럼에 함수를 적용하는 메서드
pd_data = df[pd_cols].apply(pd.to_numeric, errors="coerce")   # pd.to_numric    = 숫자형 데이터로 변환
                                                              # errors="coerce" = 숫자 변환 불가 값은 결측치로 처리 

# xpt파일의 이상치(매우 작은 것들)는 0으로 처리
cal_data = cal_data.mask(cal_data.abs() < 1e-70, 0) # .mask() = 조건이 참인 값을 지정된 값으로 변경(매우작은 숫자를 0으로)
pd_data = pd_data.mask(pd_data.abs() < 1e-70, 0)    # .abs()  = CAL 데이터의 절댓값을 구하는 메서드
                                                    # 절댓값: 0에서 얼마나 떨어졌는가
                                                    # ex) -5의 절댓값은 5 / 10의 절댓값은 10

# 음수나 99 등 이상치 밖의 값 제외 시키기
cal_data = cal_data.where(cal_data.between(0, 20)) # .where()   = 조건에 맞는 값은 유지, 아닌 값은 결측치로 변경
pd_data = pd_data.where(pd_data.between(0, 20))    # .between() = A ~ B인가 --> 0~20 사이인가 

# 4. 치주질환 관련 라벨 생성 -----------------------------------------------------------------------------------------

# CAL컬럼과 치아 정보 연결
# cal_site{} = 치아번호 + 측정위치를 CAL컬럼에 연결하여 저장할 딕셔너리
cal_sites = { 
  col[3:5] + col[-1]: col # col[3:5] = 인덱스 3~4까지 문자 추출
  for col in cal_cols     # col[-1]  = 인덱스 마지막 문자 추출
}                         # ex) OHX11LAD --> 11D
                          # for문: col에 담은 것들 cal_cols에 담을거다

# PD컬럼과 치아 정보 연결
# pd_sites{} = 컬럼명 중 치아번호만 추출
pd_sites = {
  col[3:5] + col[-1]: col # col[3-5] = 인덱스 3~4까지 문자 추출
  for col in pd_cols      # col[-1]  = 인덱스 마지막 문자 추출
}                         # for문: col에 담은 것들 pd_cols에 담을거다

# CAL 3mm 이상인 치아 확인
affected_teeth = pd.DataFrame(index=df.index) # index    = DF의 인덱스 지정하는 매개변수
                                              # df.index = 기존 DF 행의 인덱스
                                              # 즉 affected_teeth의 index는 df.index이다

for tooth in sorted({site[:2] for site in cal_sites}): # sorted() = 오름차순
                                                       # site[:2] = 두번째 문자열 까지(중복 x)
  site_cols = [
    cal_sites[site]       # key로 [site] 가져와야 함
    for site in cal_sites # ex) site="11D" --> 가져오는 것: OHX11LAD
    if site.startswith(tooth) # .startswith() = 문자열이 특정 문자로 시작하는지 검사하는 메서드
  ]                           # ex) stie="11D" 인데 tooth="11" 이라면 True

  affected_teeth[tooth] = (
    cal_data[site_cols] >= 3 # CAL이 3mm 이상이면 True
  ).any(axis=1) # .any() = 하나라도 만족하면 True
                # axis=1 = 행 기준으로 반환
                # axis=2 = 열 기준으로 반환

# 치아 2개 이상에서 CAL이 3mm 이상인 것 확인
cal_positive = affected_teeth.sum(axis=1) >= 2 # cal_positive   = CAL 조건 해당하는 대상자인지 확인
                                               # affected_teeth = CAL 조건 해당되는 것만 저장한 DF
                                               # .sum() = 합계(메서드)
                                               # 해석: CAL이 3mm 이상인 치아가 2개 이상이면 True
                                               # 참고: True=1 / False=0

# 인접면 PD 4mm 이상인 부위 있는지 확인
pd_positive = (pd_data >= 4).any(axis=1) # pd_positive = PD 조건 충족하는 것만 저장하는 변수
                                         # pd_data = 치주낭 깊이 데이터(숫자형)
                                         # .any()  = 하나라도 만족하면 True
                                         # axis=1  = 행 기준으로 검사

# 평가 가능한 측정값 있는 대상자만 유지하라
valid = (
  cal_data.notna().any(axis=1) # .notna() = 결측치가 아니면 True 반환하는 메서드
  & pd_data.notna().any(axis=1)# .any()   = 하나라도 만족하면 True
)                              # axis=1   = 행 기준으로 검사

df = df.loc[valid].copy() # .loc[]  = 행이나 열을 라벨이나 조건으로 선택하는 인덱서
                          # .copy() = 데이터 복사본 생성

df["target"] = ( # target 이라는 컬럼 지정하거나 생성
  cal_positive.loc[valid] # .loc[] = 행 or 열을 라벨이나 조건으로 선택
  & pd_positive.loc[valid]
).astype(int) # .astype() = 데이터 타입을 변경하는 메서드

print("라벨 생성 후 데이터 크기: ", df.shape) # df.shape = DF의 행과 열을 반환하는 속성
print(df["target"].value_counts())
print(df["target"].value_counts(normalize=True) * 100) # .value_counts() = 각 값이 몇번 나왔는가
                                                       # nomalize=True   = 등장 횟수 대비 비율로 변환
                                                       # nomalize=False  = 등장 횟수 
                                                       # * 100 = 백분율로 변환

# 5. 모델에 사용할 입력 변수 선택 ------------------------------------------------------------------------------------

# 사용할 입력 변수
FEATURES = [
  "RIDAGEYR",
  "RIAGENDR",
  "SMQ020",
  "SMQ040"
]

X = df[FEATURES].copy()
Y = df["target"].copy()

# 흡연 설문 응답 거부 or 모름 코드 처리
for col in ["SMQ020", "SMQ040"]:
  X[col] = X[col].replace({
    7: np.nan,
    9: np.nan
  })

# 범주형 변수는 숫자 크기 말고 범주형으로 취급하라
categorical_features = [
  "RIAGENDR",
  "SMQQ020",
  "SMQ040"
]  

numeric_features = ["RIDAGEYR"]

print("입력 데이터: ", X.shape)
print("정답데이터: ", Y.shape)
print(X.head())

# 6. 학습데이터 / 검증데이터 / 테스트데이터 분리 ----------------------------------------------------------------------
