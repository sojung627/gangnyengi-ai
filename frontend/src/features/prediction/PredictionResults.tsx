import { AlertTriangle, CheckCircle2 } from "lucide-react"; // AlertTriangle = 주의사항 아이콘 불러오기
                                                            // CheckCircle2  = 체크 아이콘 불러오기
                                                            // lucide-react  = react에서 아이콘 사용을 허가하라
import type { ModelPrediction, PredictionResponse } from "../../api/prediction"; // type = 외부모듈에서 자료형 가져와라
                                                                                 // prediction.ts를 불러와라
// 개별 AI 모델의 예측 결과 카드
function ModelCard({
  title, // title = 제목
  model, // model = 모델
}: {
  title: string; // 제목은 str
  model: ModelPrediction; // 모델은 ModelPrediction
}) {
  // 예측확률을 백분율로 변환
  const percentage = (model.probability * 100).toFixed(1); // const = 상수
                                                           // model = 개별 모델 예측 결과
                                                           // probability = 모델 예측 확률
                                                           // * 100 = 예측 확률을 백분율로 변환
                                                           // () = 내부 연산을 먼저 수행하라
                                                           // .toFixed() = 지정한 소수점 자릿수에서 반올림 후 문자열로 반환
                                                           // (1) = 소수점 첫 번째 자리까지 표시하라
  // 양성 예측 여부 확인
  const positive = model.prediction === 1; // const = 상수
                                           // model = 개별 모델 예측 결과
                                           // prediction = 모델의 최종 예측 분류값
                                           // 1 = 앙성
  return (
    <article className="model-card">
      <div className="model-card__head">
        <h3>{title}</h3>
        <span
          className={`status ${positive ? "status--positive" : "status--negative"}`}
        >
          {positive ? (
            <AlertTriangle size={13} aria-hidden="true" />
          ) : (
            <CheckCircle2 size={13} aria-hidden="true" />
          )}
          {positive ? "기준군" : "비해당군"}
        </span>
      </div>
      <p className="model-card__value">
        {percentage}
        <span>%</span>
      </p>
      <div
        className="meter"
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={Math.round(model.probability * 100)}
        aria-label={`${title} 양성 클래스 점수`}
      >
        <span
          className="meter__fill"
          style={{
            width: `${Math.min(100, Math.max(0, model.probability * 100))}%`,
          }}
        />
      </div>
      <div className="model-card__foot">
        <span>분류 임계값</span>
        <strong>{(model.threshold * 100).toFixed(0)}%</strong>
      </div>
    </article>
  );
}

export function PredictionResults({ result }: { result: PredictionResponse }) {
  return (
    <section
      className="panel result-panel"
      id="results"
      aria-labelledby="results-heading"
      aria-live="polite"
    >
      <div className="panel__heading">
        <div>
          <p className="eyebrow">RESULTS</p>
          <h2 id="results-heading">모델별 예측 결과</h2>
        </div>
      </div>
      <p className="panel__description">
        개인의 건강정보는 저장되지 않습니다.
      </p>
      <div className="model-grid">
        <ModelCard
          title= "LR"
          model={result.logistic_regression}
        />
        <ModelCard title="XGBoost" model={result.xgboost} />
        <ModelCard title="MLP" model={result.pytorch_mlp} />
      </div>
      <div className="notice" role="note">
        <AlertTriangle size={18} aria-hidden="true" />
        <p>{result.disclaimer} 의료적 진단 치료 의사결정에 사용하지 마세요.</p>
      </div>
    </section>
  );
}
