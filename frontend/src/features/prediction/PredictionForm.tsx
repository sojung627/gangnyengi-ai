import { useEffect, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
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

export function PredictionForm({
  isLoading,
  onPredict,
  onReset,
}: PredictionFormProps) {
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
  // 시안에 포함된 참고 수치: 현재 저장된 모델의 예측 입력에는 포함되지 않는다.
  const everSmoked = watch("everSmoked");

  useEffect(() => {
    if (everSmoked !== "1") setValue("smokingFrequency", "");
  }, [everSmoked, setValue]);

  function clearForm() {
    reset(emptyPredictionForm);
    onReset();
  }

  return (
    <form
      className="analysis-form"
      onSubmit={handleSubmit(onPredict)}
      noValidate
    >
      <div className="analysis-form__grid">
        <div className="analysis-field">
          <label htmlFor="age">
            <i className="fa-regular fa-calendar-days" aria-hidden="true" />{" "}
            나이
          </label>
          <input
            id="age"
            type="number"
            min="30"
            max="80"
            step="1"
            placeholder="나이를 입력하세요"
            autoComplete="off"
            aria-invalid={Boolean(errors.age)}
            aria-describedby={errors.age ? "age-error" : undefined}
            {...register("age")}
          />
          {errors.age && (
            <p id="age-error" className="analysis-field__error" role="alert">
              {errors.age.message}
            </p>
          )}
        </div>
        <div className="analysis-field">
          <label htmlFor="gender">
            <i className="fa-solid fa-venus-mars" aria-hidden="true" /> 성별
          </label>
          <select
            id="gender"
            aria-invalid={Boolean(errors.gender)}
            aria-describedby={errors.gender ? "gender-error" : undefined}
            {...register("gender")}
          >
            <option value="">선택해 주세요</option>
            <option value="1">남성</option>
            <option value="2">여성</option>
          </select>
          {errors.gender && (
            <p id="gender-error" className="analysis-field__error" role="alert">
              {errors.gender.message}
            </p>
          )}
        </div>
        <div className="analysis-field analysis-field--wide">
          <label htmlFor="everSmoked">
            <i className="fa-solid fa-smoking" aria-hidden="true" /> 흡연 여부
          </label>
          <select
            id="everSmoked"
            aria-invalid={Boolean(errors.everSmoked)}
            aria-describedby={
              errors.everSmoked ? "everSmoked-error" : "smoking-help"
            }
            {...register("everSmoked")}
          >
            <option value="">선택해 주세요</option>
            <option value="2">평생 100개비 이상 흡연 경험 없음</option>
            <option value="1">평생 100개비 이상 흡연 경험 있음</option>
          </select>
          <p id="smoking-help" className="analysis-field__hint">
            NHANES 기준: 평생 100개비 이상 흡연 경험
          </p>
          {errors.everSmoked && (
            <p
              id="everSmoked-error"
              className="analysis-field__error"
              role="alert"
            >
              {errors.everSmoked.message}
            </p>
          )}
        </div>
          <div className="analysis-field analysis-field--wide">
            <label htmlFor="smokingFrequency">
              <i className="fa-solid fa-smoking" aria-hidden="true" /> 현재 흡연
              상태
            </label>
            <select
              id="smokingFrequency"
              aria-invalid={Boolean(errors.smokingFrequency)}
              aria-describedby={
                errors.smokingFrequency ? "smokingFrequency-error" : undefined
              }
              {...register("smokingFrequency")}
            >
              <option value="">선택해 주세요</option>
              <option value="1">매일 흡연</option>
              <option value="2">가끔 흡연</option>
              <option value="3">현재 흡연하지 않음</option>
            </select>
            {errors.smokingFrequency && (
              <p
                id="smokingFrequency-error"
                className="analysis-field__error"
                role="alert"
              >
                {errors.smokingFrequency.message}
              </p>
            )}
          </div>
        
      </div>
      <p className="analysis-form__disclosure">
        현재 모델은 나이 성별 흡연 정보로 예측합니다.
      </p>
      <button
        type="submit"
        className="analysis-form__submit"
        disabled={isLoading}
        aria-busy={isLoading}
      >
        <span>{isLoading ? "분석 중..." : "분석하기"}</span>
        <i className="fa-solid fa-arrow-right" aria-hidden="true" />
      </button>
      <button
        type="button"
        className="analysis-form__reset"
        onClick={clearForm}
        disabled={isLoading}
      >
        입력 초기화
      </button>
    </form>
  );
}
