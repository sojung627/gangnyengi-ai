
import { useState } from "react";
import type { FormEvent } from "react";
import axios from "axios";
import { predictPeriodontal } from "./api/prediction";

import "./App.css";


// 사용자 입력 타입
type Gender = 1 | 2;
type SmokingExperience = 1 | 2;
type SmokingFrequency = 1 | 2 | 3 | null;

interface PredictionInput {
  age: number;
  gender: Gender;
  ever_smoked: SmokingExperience;
  smoking_frequency: SmokingFrequency;
}

// 모델 예측 결과 타입
interface ModelPrediction {
  probability: number;
  prediction: 0 | 1;
  threshold: number;
}

// API 전체 응답 타입
interface PredictionResponse {
  logistic_regression: ModelPrediction;
  xgbost: ModelPrediction;
  python_mlp: ModelPrediction;
  disclaimer: ModelPrediction;
}

// 주소
// 나중에 추가

// 개발 모델 결과 카드
function PredictionCard({
  title,
  result,
}: {
  title: string;
  result: ModelPrediction;
}) {
  const percentage = (
    result.probability * 100
  ).toFixed(2);
  
  return (
    <article className="result-card">
      <h3>{title}</h3>
      
      <p className="probability">
        {percentage}%
      </p>
      
      <p className="prediction-label">
        {
          result.prediction === 1
          ? "치주 이상 소견 기준군"
          : "기준 비해당군"
        }
      </p>
        
      <p className="threshold">
        분류 임계값: {result.threshold}
      </p>
    </article>
  );
}

// 메인 컴포넌트
function app() {
  
  // 사용자 입력 상태 - 하드코딩 [수정 필요]
  const [form, setForm] = useState<PredictionInput>({
    age: 45,
    gender: 2,
    ever_smoked: 2,
    smoking_frequency: null,
  })
}

// 예측 결과
const [result, setResult] = 
useState<PredictionResponse | Null>(null);

// API 요청 상태
const [loading, setLoading] = useState(false);

// 오류 메시지
const [error, setError] = useState("");

 // 6. 예측 요청
async function handlePredict(
  event: FormEvent<HTMLFormElement>
) {
  event.preventDefault();

  setLoading(true);
  setError("");
  setResult(null);

  try {
    const response = await fetch(
      `${API_URL}/predict`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      }
    );

    if (!response.ok) {
      const body = await response.json().catch(
        () => null
      );

      throw new Error(
        typeof body?.detail === "string"
          ? body.detail
          : `예측 요청 실패: ${response.status}`
      );
    }

    const data: PredictionResponse =
      await response.json();

    setResult(data);

  } catch (err) {
    setError(
      err instanceof Error
        ? err.message
        : "예측 중 오류가 발생했습니다."
    );

  } finally {
    setLoading(false);
  }
}

return (
  <main className="container">
    <header className="header">
      <div className="logo">🦷</div>
      <h1>GangNaengI AI</h1>
      <p>
        ML / DL 기반 치주 이상 소견 분류 시스템
      </p>
    </header>


    <section className="panel">
      <h2>분석 정보 입력</h2>
      <p className="description">
        연구용 데이터로 학습한 세 가지 모델의
        분류 결과를 비교합니다.
      </p>
      <form onSubmit={handlePredict}>
        {/* 연령 */}
        <div className="field">
          <label htmlFor="age">연령</label>
          <input id="age" type="number" min={30} max={80} required value={form.age} 
            onChange={(event) => {
              setForm({
                ...form,
                age: Number(event.target.value),
              });
            }}
          />
        </div>


        {/* 성별 */}
        <div className="field">
          <label htmlFor="gender">성별</label>

          <select
            id="gender"
            value={form.gender}
            onChange={(event) => {
              setForm({
                ...form,
                gender: Number(
                  event.target.value
                ) as Gender,
              });
            }}
          >
            <option value={1}>남성</option>
            <option value={2}>여성</option>
          </select>
        </div>


        {/* 흡연 경험 */}
        <div className="field">
          <label htmlFor="ever_smoked">
            평생 담배 100개비 이상 흡연 경험
          </label>

          <select
            id="ever_smoked"
            value={form.ever_smoked}
            onChange={(event) => {
              const value = Number(
                event.target.value
              ) as SmokingExperience;

              setForm({
                ...form,
                ever_smoked: value,
                smoking_frequency:
                  value === 1 ? 3 : null,
              });
            }}
          >
            <option value={2}>없음</option>
            <option value={1}>있음</option>
          </select>
        </div>


        {/* 현재 흡연 빈도 */}
        {form.ever_smoked === 1 && (
          <div className="field">
            <label htmlFor="smoking_frequency">
              현재 흡연 빈도
            </label>

            <select
              id="smoking_frequency"
              value={form.smoking_frequency ?? 3}
              onChange={(event) => {
                setForm({
                  ...form,
                  smoking_frequency: Number(
                    event.target.value
                  ) as 1 | 2 | 3,
                });
              }}
            >
              <option value={1}>매일</option>
              <option value={2}>가끔</option>
              <option value={3}>
                현재 피우지 않음
              </option>
            </select>
          </div>
        )}


        {/* 예측 버튼 */}
        <button
          type="submit"
          className="predict-button"
          disabled={loading}
        >
          {loading
            ? "분석 중..."
            : "AI 예측 실행"}
        </button>
      </form>


      {/* 오류 메시지 */}
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
    </section>


    {/* 결과 화면 */}
    {result && (
      <section className="panel">

        <h2>모델별 예측 결과</h2>

        <div className="results">
          <PredictionCard
            title="Logistic Regression"
            result={result.logistic_regression}
          />

          <PredictionCard
            title="XGBoost"
            result={result.xgboost}
          />

          <PredictionCard
            title="PyTorch MLP"
            result={result.pytorch_mlp}
          />
        </div>

        <p className="disclaimer">
          {result.disclaimer}
        </p>
      </section>
    )}


    <footer>
      GangNaengI AI · Research Portfolio
    </footer>

  </main>
)