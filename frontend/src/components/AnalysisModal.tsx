import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";
import { PredictionForm } from "../features/prediction/PredictionForm";
import { PredictionResults } from "../features/prediction/PredictionResults";
import type { PredictionResponse } from "../api/prediction";
import type { PredictionFormValues } from "../features/prediction/prediction.schema";
import "./AnalysisModal.css";

interface AnalysisModalProps {
  onClose: () => void;
  onPredict: (values: PredictionFormValues) => Promise<void>;
  onReset: () => void;
  onTryAgain: () => void;
  isLoading: boolean;
  result: PredictionResponse | null;
  error: string;
}

export function AnalysisModal({ onClose, onPredict, onReset, onTryAgain, isLoading, result, error }: AnalysisModalProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    previousFocusRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    closeRef.current?.focus();

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        event.preventDefault();
        onClose();
        return;
      }
      if (event.key !== "Tab" || !dialogRef.current) return;
      const focusable = Array.from(dialogRef.current.querySelectorAll<HTMLElement>(
        'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])'
      ));
      if (!focusable.length) { event.preventDefault(); return; }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault(); last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault(); first.focus();
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = previousOverflow;
      previousFocusRef.current?.focus();
    };
  }, [onClose]);

  return createPortal(
    <div className="analysis-backdrop" onMouseDown={(event) => {
      if (event.target === event.currentTarget) onClose();
    }}>
      <div ref={dialogRef} className="analysis-modal" role="dialog" aria-modal="true" aria-labelledby="analysis-modal-title" aria-describedby="analysis-modal-description">
        <button ref={closeRef} type="button" className="analysis-modal__close" onClick={onClose} aria-label="분석 창 닫기">
          <span aria-hidden="true">×</span>
        </button>
        <header className="analysis-modal__heading">
          <h2 id="analysis-modal-title">치주질환 위험도 분석</h2>
          <p id="analysis-modal-description">AI 분석을 위해 아래 정보를 입력해 주세요.</p>
        </header>
        {result ? (
          <div className="analysis-modal__results">
            <PredictionResults result={result} />
            <button type="button" className="analysis-modal__again" onClick={onTryAgain}>다시 분석하기</button>
          </div>
        ) : (
          <>
            <PredictionForm isLoading={isLoading} onPredict={onPredict} onReset={onReset} />
            {error && <p className="analysis-modal__error" role="alert">{error}</p>}
          </>
        )}
      </div>
    </div>,
    document.body
  );
}
