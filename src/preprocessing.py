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
from sklearn.impute import SimpleImputer # sklearn.impute = 결측치 처리 모듈
                                         # SimpleImputer  = 결측치를 평균값 or 중앙값 or 최빈값으로 대체(결측치 단순대치법)                                       
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
  if re.fullmatch(r"OHX\d{2}LA[DSPA]", col) # re.fullmatch() = 문자열 전체가 정규표현식과 일치하라
]                                            # OHX = OHX로 시작하라
                                             # \d  = 0~9 숫자 한자리
                                             # {2} = 앞의 숫자가 정확히 두번 반복하라
                                             # \LA  = 숫자 다음은 LA라는 문자열
                                             # [DSPA] = D S P A 중 하나 포함

# 치주낭 깊이 
pd_cols = [
  col for col in df.columns # df의 컬럼이 조건에 해당하면 col에 담겠다
  if re.fullmatch(r"OHX\d{2}PC[DSPA]", col) # re.fullmatch() = 문자열 전체가 정규표현식과 일치해라
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
                # axis=0 = 열 기준으로 반환

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
  "RIDAGEYR", # 참가자의 나이(연도)
  "RIAGENDR", # 참가자의 성별
  "SMQ020",   # 평생 담배 100개비 이상 피었는가
  "SMQ040"    # 현재 흡연 빈도 ex) 요즘은 자주 피는가
]

X = df[FEATURES].copy() # X = ML모델 입력데이터 저장 | DF 타입
y = df["target"].copy() # Y = ML모델 정답데이터 저장 | Series 타입
                        # .copy() = 복사본

# 흡연 설문 응답 거부 or 모름 코드 처리
for col in ["SMQ020", "SMQ040"]:
  X[col] = X[col].replace({ # .replace() = 지정한 값을 다른 값으로 변경하는 메서드
    7: np.nan, # 7을 결측치로 저장
    9: np.nan  # 9를 결측치로 저장
  })

# 범주형 변수는 숫자 크기 말고 범주형으로 취급하라
categorical_features = [
  "RIAGENDR", # 참가자의 나이(연도)
  "SMQ020",   # 평생 담배 100개비 이상 피었는가
  "SMQ040"    # 현재 흡연 빈도 ex) 요즘은 자주 피는가
]  

numeric_features = ["RIDAGEYR"] # numeric_features = 수치형 변수들 저장하는 변수

print("입력 데이터: ", X.shape) # .shape = 데이터 크기 나타내는 속성
print("정답데이터: ", y.shape)  # X는 행과 열이 나타남(튜플) 
                               # Y는 행만 나타남(Series)
print(X.head())                # head() = 5개만 출력

# 6. 학습데이터 / 검증데이터 / 테스트데이터 분리 ----------------------------------------------------------------------

# 학습데이터 70 / 임시데이터 30으로 분리
# X_train = 모델 학습에 사용할 입력 데이터 저장용 변수
# X_temp  = 검증데이터와 테스트데이터 저장용 임시 변수
# y_train = 학습데이터 정답 라벨 저장 변수
# y_temp  = 임시데이터 정답 라벨 저장 변수
X_train, X_temp, y_train, y_temp = train_test_split(
  X, y,
  test_size=0.30, # 임시데이터=30%
  random_state=42,# 무작위 분할 난수 시드 --> 42
  stratify=y      # 데이터 비율 유지하며 분리하는 매개변수 --> 모든 데이터 정답라벨=y
)

# 나머지 30을 반반으로(15 / 15)
# X_val  = 검증용 입력데이터 저장용 변수
# X_test = 테스트용 입력데이터 저장용 변수
# y_val  = 검증용 데이터 정답 라벨 저장용 변수
# y_test = 테스트용 데이터 정답 라벨 저장용 변수
X_val, X_test, y_val, y_test = train_test_split(
  X_temp, y_temp,
  test_size=0.50, # 두번째 데이터는 50%
  random_state=42,# 무작위 분할 난수 시드 --> 42
  stratify=y_temp # 데이터 비율 유지하며 분리하는 매개변수
)                 # 임시 데이터 포함된 치주라벨을 0과 1로 유지하며 검증용 / 테스트용으로 분리

print("Train: ", X_train.shape) # .shape = DF의 행과 열 개수 반환
print("Validation: ", X_val.shape)
print("Test: ", X_test.shape)

# 참가자 서로 겹치는지 확인
assert set(X_train.index).isdisjoint(X_val.index) # assert = 조건 검사 후 False면 AssertionError
assert set(X_train.index).isdisjoint(X_test.index)# .index = DF 행 인덱스
assert set(X_val.index).isdisjoint(X_test.index)  # .isdisjoint() = 두 집합에 공통 요소가 없는지 확인하는 메서드

# 7. [전처리] - 결측치 처리 인코딩 및 스케일링 ----------------------------------------------------------------------

# 숫자형 - 결측값을 중앙값으로 대체 후 표준화
# 해석: 숫자형 데이터 전처리 파이프라인
numeric_pipeline = Pipeline([ # Pipeline() = 데이터들 순서대로 처리하는 클래스 
  ("imputer", SimpleImputer(strategy="median")), # SimpleImputer()   = 결측값 대체(평균값 / 중앙값 / 최빈값)
                                                 # strategy="median" = 중앙값으로 대체하라
  ("scaler", StandardScaler()) # StandardScaler() = 평균이 0 표준편차 1로 하라(표준화) ex) Z-score
])

# 범주형 - 결측값을 별도 범주로 처리 후 원핫 인코딩
# 해석: 범주형 데이터 전처리 파이프라인 
categorical_pipeline = Pipeline([ # Pipeline() = 데이터들을 순서대로 처리하는 클래스
  (
    "imputer", 
    SimpleImputer( # 결측값 대체(평균값 / 중앙값 / 최빈값)
      strategy="constant", # 결측값을 지정된 고정값으로 수정하라
      fill_value=-1         # 결측값을 -1로 대체 하라
    )
  ),
  (
    "onehot",
    OneHotEncoder( # OneHotEncoder() = 0과 1인 컬럼으로 바꿔라(이진법)
      handle_unknown="ignore", # handle_unknown = 학습할 때 없던 새 범주가 들어오면 어떻게 처리할 지 정하는 매개변수
                               # ignore = 새 범주 와도 오류내지마
      sparse_output=False # sparse_output() = 원핫 인코딩 결과를 희소 행렬로 반환할 것인가
    )                     # False = 안한다(일반 NumPy 배열로 저장)
  )
])

# 숫자형 + 범주형 데이터 전처리 과정 둘다 저장
preprocessor = ColumnTransformer([ # ColumnTransformer() = 컬럼 종류에 따라 각 다르게 전처리 하라
  ("numeric", numeric_pipeline, numeric_features), # 숫자는 아까 정한대로 전처리 하라(중앙값 대체)
  ("categorical", categorical_pipeline, categorical_features) # 범주형은 아까 정한대로 해라(1로 대체)
]) 

# 학습데이터만 fit
X_train_processed = preprocessor.fit_transform(X_train) # X_train_processed = 전처리 완료된 학습데이터
                                                        # .fit_transform()  = 전처리 해야할 값 학습 후 변환하는 메서드

# 검증 or 테스트데이터는 transform만 실행
X_val_processed = preprocessor.transform(X_val)   # X_val_processed  = 전처리 완료된 검증데이터
X_test_processed = preprocessor.transform(X_test) # X_test_processed = 전처리 완료된 테스트데이터
                                                  # .transform() = 이미 학습한 데이터 변환 메서드

print("전처리 후 Train: ", X_train_processed.shape) # .shape = 행과 열을 튜플로 반환
print("전처리 후 Validation: ", X_val_processed.shape)
print("전처리 후 Test: ", X_test_processed.shape)

# 8. 전처리 결과 저장 ----------------------------------------------------------------------------------------------

# ML DL 공통 학습 데이터 저장
np.savez_compressed( # .savez_compressed() = NumPy 압축 파일 만드는 함수
  PROCESSED / "train_data.npz", # C:\projects\projectAI\GangNaengI_AI\data\processed\train_data.npz
  X=X_train_processed,
  y=y_train.to_numpy() # Pandas를 NumPy로 변환
)

np.savez_compressed( # .savez_compressed() = NumPy 압축 파일 만드는 함수
  PROCESSED / "val_data.npz", # C:\projects\projectAI\GangNaengI_AI\data\processed\val_data.npz
  X=X_val_processed,
  y=y_val.to_numpy() # Pandas를 NumPy로 변환
)

np.savez_compressed( # .savez_compressed() = NumPy 압축 파일 만드는 함수
  PROCESSED / "test_data.npz", # C:\projects\projectAI\GangNaengI_AI\data\processed\test_data.npz
  X=X_test_processed,
  y=y_test.to_numpy() # Pandas를 NumPy로 변환
)

# API에서도 동일한 전처리 사용하라(저장)
joblib.dump( # joblib  = 파이썬 객체를 파일로 저장 or 불러오기
             # .dump() = 파이썬 객체를 직렬화 
             # 직렬화: 객체를 파일로 저장할 수 있는 형태로 변환
  preprocessor,
  MODELS / "preprocessor.joblib" # C:\projects\projectAI\GangNaengI_AI\models\preprocessor.joblib
)

# 분석 및 추적용 라벨 데이터
df[["SEQN", "target"]].to_csv( # [[]]    = 두개의 컬럼만 선택
                               # .to_csv = DF를 CSV로 저장
  PROCESSED / "labels.csv", # C:\projects\projectAI\GangNaengI_AI\data\processed\labels.csv
  index=False # 행 인덱스는 csv 파일에 저장하지 마라
)

print("day02 - 데이터 전처리 및 학습데이터 구축")