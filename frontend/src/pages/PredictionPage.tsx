import { useCallback, useEffect, useRef, useState } from "react";
import { Activity, Database, ShieldCheck } from "lucide-react";
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
        <div className="content-width hero__inner">
          <span className="hero__eyebrow"><Activity size={15} aria-hidden="true" /> DATA-DRIVEN PERIODONTAL RESEARCH</span>
          <h1 id="hero-heading">데이터로 살펴보는<br /><span>치주 건강 분류</span></h1>
          <p className="hero__intro">NHANES 2013–2014 데이터를 바탕으로 학습한 머신러닝·딥러닝 모델의 예측 결과를 한곳에서 비교해 보세요.</p>
          <div className="hero__facts">
            <span><Database size={17} aria-hidden="true" /> NHANES 2013–2014</span>
            <span><ShieldCheck size={17} aria-hidden="true" /> 연구·교육 목적</span>
          </div>
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
