import { useCallback, useEffect, useRef, useState } from "react";
import { getPredictionError, predictPeriodontal, type PredictionResponse } from "../api/prediction";
import { PredictionForm } from "../features/prediction/PredictionForm";
import { PredictionResults } from "../features/prediction/PredictionResults";
import { toPredictionInput, type PredictionFormValues } from "../features/prediction/prediction.schema";

export function PredictionPage() {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => () => abortRef.current?.abort(), []);

  const handleReset = useCallback(() => {
    abortRef.current?.abort();
    setLoading(false);
    setResult(null);
    setError("");
  }, []);

  const handlePredict = useCallback(async (values: PredictionFormValues) => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const data = await predictPeriodontal(toPredictionInput(values), controller.signal);
      if (!controller.signal.aborted) setResult(data);
    } catch (err: unknown) {
      if (!controller.signal.aborted) setError(getPredictionError(err));
    } finally {
      if (abortRef.current === controller) {
        abortRef.current = null;
        setLoading(false);
      }
    }
  }, []);

  return (
    <main id="top">
      <section className="hero" aria-labelledby="hero-heading">
        <div className="hero__inner">
          <h1 id="hero-heading">치주질환 위험도 분석</h1>
          <span className="hero__rule" aria-hidden="true" />
          <p className="hero__intro">내 구강 데이터를 기반으로<br />치주질환의 위험도를 AI가 예측합니다.</p>
          <a className="hero__cta" href="#analysis">
            위험도 분석 시작 <span aria-hidden="true">→</span>
          </a>
        </div>
      </section>

      <div className="content-width content-layout" id="analysis">
        <PredictionForm isLoading={loading} onPredict={handlePredict} onReset={handleReset} />
        {error && <div className="error-banner" role="alert">{error}</div>}
        {result && <PredictionResults result={result} />}
      </div>
    </main>
  );
}
