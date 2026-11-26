import { z } from "zod";
import type { PredictionInput } from "../../api/prediction";

// 입력하지 않은 필드는 실제 입력과 구분하기 위해 빈 문자열로 둔다.
export const predictionFormSchema = z.object({
  age: z.string().min(1, "나이를 입력해 줘.").refine(
    (v) => /^\d+$/.test(v) && Number(v) >= 30 && Number(v) <= 80,
    "지원 연령은 30~80세야.",
  ),
  gender: z.string()
  .min(1, "성별을 선택해 줘.")
  .refine(
    (v) => ["1", "2"].includes(v),
    "성별 입력값을 확인해 줘."
  ),

  everSmoked: z.string()
  .min(1, "흡연 경험을 선택해 줘.")
  .refine(
    (v) => ["1", "2"].includes(v),
    "흡연 경험 입력값을 확인해 줘."
  ),
  smokingFrequency: z.string(),
}).superRefine((data, ctx) => {
  if (data.everSmoked === "1" && !["1", "2", "3"].includes(data.smokingFrequency)) {
    ctx.addIssue({ code: "custom", path: ["smokingFrequency"], message: "현재 흡연 상태를 선택해 줘." });
  }
});

export type PredictionFormValues = z.infer<typeof predictionFormSchema>;

export const emptyPredictionForm: PredictionFormValues = {
  age: "",
  gender: "",
  everSmoked: "",
  smokingFrequency: "",
};

export function toPredictionInput(data: PredictionFormValues): PredictionInput {
  if (data.gender !== "1" && data.gender !== "2") throw new Error("성별 입력값이 올바르지 않아.");
  if (data.everSmoked !== "1" && data.everSmoked !== "2") throw new Error("흡연 경험 입력값이 올바르지 않아.");
  if (data.everSmoked === "1" && !["1", "2", "3"].includes(data.smokingFrequency)) {
    throw new Error("현재 흡연 상태를 선택해 줘.");
  }
  return {
    age: Number(data.age),
    gender: Number(data.gender) as 1 | 2,
    ever_smoked: Number(data.everSmoked) as 1 | 2,
    smoking_frequency: data.everSmoked === "1"
      ? Number(data.smokingFrequency) as 1 | 2 | 3
      : null,
  };
}
