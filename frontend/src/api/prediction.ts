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
  if (axios.isCancel(error)) {
    console.info("API 요청이 취소되었습니다.");
    return "검사가 취소 되었습니다.";
  }

  if (error instanceof z.ZodError) {
    console.error("API 응답 스키마 불일치:", error.issues);
    return "검사 결과를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.";
  }

  if (axios.isAxiosError(error)) {
    const detail: unknown = error.response?.data?.detail;

    if (typeof detail === "string") {
      console.error("백엔드 오류가 발생했습니다:", detail);
      return "검사 진행 중 문제가 발생했습니다. 잠시 후 다시 시도해 주세요.";
    }

    if (Array.isArray(detail)) {
      const messages = detail
        .filter(
          (item): item is { msg: string } =>
            Boolean(item) && typeof item.msg === "string",
        )
        .map((item) => item.msg);

      if (messages.length) {
        console.error("백엔드 데이터 검증 오류:", messages);
        return "입력하신 정보를 다시 확인해 주세요.";
      }
    }

    if (error.code === "ECONNABORTED") {
      console.error("API 서버 응답 시간이 초과되었습니다.");
      return "검사 결과를 불러오는 데 시간이 오래 걸리고 있습니다. 잠시 후 다시 시도해 주세요.";
    }

    if (!error.response) {
      console.error(
        "API 서버 연결 실패. 서버 실행 상태와 환경변수를 확인해 주세요.",
      );
      return "서비스에 연결할 수 없습니다. 인터넷 연결을 확인하거나 잠시 후 다시 시도해 주세요.";
    }

    console.error("HTTP 요청 실패:", error.response.status);
    return `검사 진행 중 문제가 발생했습니다. 잠시 후 다시 시도해 주세요. (HTTP ${error.response.status})`;
  }

  console.error("예상하지 못한 오류가 발생했습니다:", error);
  return "일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.";
}
