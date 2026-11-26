import axios from "axios";
import { z } from "zod";
import { apiClient, assertApiConfigured } from "./client";

// backend/schemas.py의 PredictionInput/PredictionResponse와 동일한 계약
export interface PredictionInput {
  age: number;
  gender: 1 | 2;
  ever_smoked: 1 | 2;
  smoking_frequency: 1 | 2 | 3 | null;
}

const modelPredictionSchema = z.object({
  probability: z.number().min(0).max(1),
  prediction: z.union([z.literal(0), z.literal(1)]),
  threshold: z.number().min(0).max(1),
});

const predictionResponseSchema = z.object({
  logistic_regression: modelPredictionSchema,
  xgboost: modelPredictionSchema,
  pytorch_mlp: modelPredictionSchema,
  disclaimer: z.string(),
});

export type ModelPrediction = z.infer<typeof modelPredictionSchema>;
export type PredictionResponse = z.infer<typeof predictionResponseSchema>;

export async function predictPeriodontal(
  data: PredictionInput,
  signal?: AbortSignal,
): Promise<PredictionResponse> {
  assertApiConfigured();
  const response = await apiClient.post<unknown>("/predict", data, { signal });
  return predictionResponseSchema.parse(response.data);
}

export function getPredictionError(error: unknown): string {
  if (axios.isCancel(error)) return "요청이 취소됐어.";
  if (error instanceof z.ZodError) return "API 응답 형식이 정의된 모델 계약과 달라. 백엔드 응답을 확인해 줘.";
  if (axios.isAxiosError(error)) {
    const detail: unknown = error.response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) {
      const messages = detail
        .filter((item): item is { msg: string } => Boolean(item) && typeof item.msg === "string")
        .map((item) => item.msg);
      if (messages.length) return messages.join(" / ");
    }
    if (error.code === "ECONNABORTED") return "서버 응답 시간이 초과됐어. 잠시 후 다시 시도해 줘.";
    if (!error.response) return "API 서버에 연결하지 못했어. 서버 실행 상태와 환경변수를 확인해 줘.";
    return `요청에 실패했어. (HTTP ${error.response.status})`;
  }
  return error instanceof Error ? error.message : "알 수 없는 오류가 발생했어.";
}
