import { useEffect } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowRight, RotateCcw } from "lucide-react";
import { useForm } from "react-hook-form";
import {
  emptyPredictionForm,
  predictionFormSchema,
  type PredictionFormValues,
} from "./prediction.schema";

interface PredictionFormProps {
  isLoading: boolean;
  onPredict: (values: PredictionFormValues) => Promise<void>;
  onReset: () => void;
}

export function PredictionForm({ isLoading, onPredict, onReset }: PredictionFormProps) {
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    reset,
    formState: { errors },
  } = useForm<PredictionFormValues>({
    resolver: zodResolver(predictionFormSchema),
    defaultValues: emptyPredictionForm,
    mode: "onSubmit",
  });

  const everSmoked = watch("everSmoked");
  useEffect(() => {
    if (everSmoked !== "1") setValue("smokingFrequency", "");
  }, [everSmoked, setValue]);

  return (
    <section className="panel form-panel" aria-labelledby="form-heading">
      <div className="panel__heading">
        <div>
          <p className="eyebrow">STEP 01 · INPUT</p>
          <h2 id="form-heading">분석 정보 입력</h2>
        </div>
        <span className="panel__tag">필수 항목 3개 + 조건부 1개</span>
      </div>
      <p className="panel__description">실제 조사 항목과 동일한 입력값을 사용해 세 가지 모델의 출력을 비교해요.</p>

      <form onSubmit={handleSubmit(onPredict)} noValidate>
        <div className="form-grid">
          <div className="field">
            <label htmlFor="age">연령 <span aria-hidden="true">*</span></label>
            <input
              id="age" type="number" min="30" max="80" step="1"
              placeholder="나이를 입력하세요 (30~80)" autoComplete="off"
              aria-invalid={Boolean(errors.age)} aria-describedby={errors.age ? "age-error" : "age-help"}
              {...register("age")}
            />
            {errors.age ? <p className="field__error" id="age-error" role="alert">{errors.age.message}</p>
              : <p className="field__help" id="age-help">NHANES 2013–2014 치주검사 대상 연령</p>}
          </div>

          <div className="field">
            <label htmlFor="gender">성별 <span aria-hidden="true">*</span></label>
            <select id="gender" aria-invalid={Boolean(errors.gender)} aria-describedby={errors.gender ? "gender-error" : undefined} {...register("gender")}>
              <option value="">선택하세요</option>
              <option value="1">남성</option>
              <option value="2">여성</option>
            </select>
            {errors.gender && <p className="field__error" id="gender-error" role="alert">{errors.gender.message}</p>}
          </div>

          <div className="field">
            <label htmlFor="everSmoked">평생 100개비 이상 흡연 경험 <span aria-hidden="true">*</span></label>
            <select id="everSmoked" aria-invalid={Boolean(errors.everSmoked)} aria-describedby={errors.everSmoked ? "everSmoked-error" : undefined} {...register("everSmoked")}>
              <option value="">선택하세요</option>
              <option value="1">있음</option>
              <option value="2">없음</option>
            </select>
            {errors.everSmoked && <p className="field__error" id="everSmoked-error" role="alert">{errors.everSmoked.message}</p>}
          </div>

          {everSmoked === "1" && (
            <div className="field">
              <label htmlFor="smokingFrequency">현재 흡연 상태 <span aria-hidden="true">*</span></label>
              <select id="smokingFrequency" aria-invalid={Boolean(errors.smokingFrequency)} aria-describedby={errors.smokingFrequency ? "smokingFrequency-error" : undefined} {...register("smokingFrequency")}>
                <option value="">선택하세요</option>
                <option value="1">매일 흡연</option>
                <option value="2">가끔 흡연</option>
                <option value="3">현재 흡연하지 않음</option>
              </select>
              {errors.smokingFrequency && <p className="field__error" id="smokingFrequency-error" role="alert">{errors.smokingFrequency.message}</p>}
            </div>
          )}
        </div>

        <div className="form-actions">
          <button type="button" className="button button--ghost" disabled={isLoading}
            onClick={() => { reset(emptyPredictionForm); onReset(); }}>
            <RotateCcw size={16} aria-hidden="true" /> 초기화
          </button>
          <button type="submit" className="button button--primary" disabled={isLoading} aria-busy={isLoading}>
            {isLoading ? "모델 분석 중…" : "AI 예측 실행"}
            {!isLoading && <ArrowRight size={17} aria-hidden="true" />}
          </button>
        </div>
      </form>
    </section>
  );
}
