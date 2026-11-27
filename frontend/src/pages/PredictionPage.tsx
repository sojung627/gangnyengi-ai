import { useCallback, useEffect, useRef, useState } from "react";
import { getPredictionError, predictPeriodontal, type PredictionResponse } from "../api/prediction";
import { AnalysisModal } from "../components/AnalysisModal";
import { toPredictionInput, type PredictionFormValues } from "../features/prediction/prediction.schema";

export function PredictionPage() {
  const [modalOpen, setModalOpen] = useState(false);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => () => abortRef.current?.abort(), []);

  const clearPrediction = useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
    setLoading(false);
    setResult(null);
    setError("");
  }, []);

  const closeModal = useCallback(() => {
    clearPrediction();
    setModalOpen(false);
  }, [clearPrediction]);

  const openModal = useCallback(() => {
    clearPrediction();
    setModalOpen(true);
  }, [clearPrediction]);

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
          <button type="button" className="hero__cta" onClick={openModal}>
            위험도 분석 시작 <span aria-hidden="true">→</span>
          </button>
        </div>
      </section>
      {modalOpen && (
        <AnalysisModal
          onClose={closeModal}
          onPredict={handlePredict}
          onReset={clearPrediction}
          onTryAgain={clearPrediction}
          isLoading={loading}
          result={result}
          error={error}
        />
      )}
    </main>
  );
}
