import { AlertTriangle, BarChart3, CheckCircle2 } from "lucide-react";
import type { ModelPrediction, PredictionResponse } from "../../api/prediction";

function ModelCard({
  title,
  model,
}: {
  title: string;
  model: ModelPrediction;
}) {
  const percentage = (model.probability * 100).toFixed(1);
  const positive = model.prediction === 1;
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
        <BarChart3
          size={23}
          className="panel__heading-icon"
          aria-hidden="true"
        />
      </div>
      <p className="panel__description">
        확률은 AI가 추측한 것일 뿐 공식적인 진단이 아닙니다.
      </p>
      <div className="model-grid">
        <ModelCard
          title="Logistic Regression"
          model={result.logistic_regression}
        />
        <ModelCard title="XGBoost" model={result.xgboost} />
        <ModelCard title="PyTorch MLP" model={result.pytorch_mlp} />
      </div>
      <div className="notice" role="note">
        <AlertTriangle size={18} aria-hidden="true" />
        <p>{result.disclaimer} 의료적 진단 치료 의사결정에 사용하지 마세요.</p>
      </div>
    </section>
  );
}
