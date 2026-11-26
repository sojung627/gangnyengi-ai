import { apiClient } from "./client";

export interface PredictionInput {
  age: number;
  gender: 1 | 2;
  ever_smoked: 1 | 2;
  smoking_frequency: 1 | 2 | 3 | null;
}

export interface ModelPrediction {
  probability: number;
  prediction: 0 | 1;
  threshold: number;
}

export interface PredictionResponse {
  logistic_regression: ModelPrediction;
  xgboost: PredictionResponse;
  pytorch_mlp: PredictionResponse;
  disclaimer: string;
}

export async function predictPeriodontal(
  data: PredictionInput
): Promise<PredictionResponse> {
  const response = await apiClient.post<PredictionResponse>(
    "/predict",
    data
  );
  return response.data;
}

