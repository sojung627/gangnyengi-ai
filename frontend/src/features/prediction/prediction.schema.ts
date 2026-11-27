import { z } from "zod";
import type { PredictionInput } from "../../api/prediction";

// 입력하지 않은 필드는 실제 입력과 구분하기 위해 빈 문자열로 둔다.
export const predictionFormSchema = z.object({
  age: z.string().min(1, "나이를 입력해 주세요.").refine(
    (v) => /^\d+$/.test(v) && Number(v) >= 30 && Number(v) <= 80,
    "검사 가능 연령은 30~80세입니다.",
  ),

  gender: z.string()
  .min(1, "성별을 선택해 주세요.")
  .refine(
    (v) => ["1", "2"].includes(v),
    "성별을 다시 선택해 주세요."
  ),

  everSmoked: z.string()
  .min(1, "흡연 경험을 선택해 주세요.")
  .refine(
    (v) => ["1", "2"].includes(v),
    "흡연 경험을 다시 선택해 주세요."
  ),

  smokingFrequency: z.string(),
}).superRefine((data, ctx) => {
  if (data.everSmoked === "1" && !["1", "2", "3"].includes(data.smokingFrequency)) {
    console.warn("현재 흡연 상태가 선택되지 않았거나 유효하지 않습니다.");

    ctx.addIssue({
      code: "custom",
      path: ["smokingFrequency"],
      message: "현재 흡연 상태를 선택해 주세요."
    });
  }
});

export type PredictionFormValues = z.infer<typeof predictionFormSchema>;

// 폼 초기 입력값
export const emptyPredictionForm: PredictionFormValues = {
  age: "",
  gender: "",
  everSmoked: "",
  smokingFrequency: "",
};

// 폼 입력 데이터를 API 요청 형식으로 변환
export function toPredictionInput(data: PredictionFormValues): PredictionInput {

  // 유효성 검증 오류 메시지 저장 배열
  const errors: string[] = [];

  // 성별 유효성 검증
  if (data.gender !== "1" && data.gender !== "2") {
    console.error("성별 데이터 변환 실패: 허용되지 않는 입력값입니다.");
    errors.push("성별 입력값이 올바르지 않습니다.");
  }

  // 흡연 경험 유효성 검증
  if (data.everSmoked !== "1" && data.everSmoked !== "2") {
    console.error("흡연 경험 데이터 변환 실패: 허용되지 않는 입력값입니다.");
    errors.push("흡연 경험 입력값이 올바르지 않습니다.");
  }

  // 현재 흡연 상태 유효성 검증
  if (data.everSmoked === "1" && !["1", "2", "3"].includes(data.smokingFrequency)) {
    console.error("현재 흡연 상태 데이터 변환 실패: 입력값이 누락되었거나 유효하지 않습니다.");
    errors.push("현재 흡연 상태를 선택해 주세요.");
  }

  // 모든 유효성 검증이 끝난 후 오류 일괄 처리
  if (errors.length > 0) {
    throw new Error(errors.join("\n"));
  }

  // API 요청 데이터 반환
  return {
    age: Number(data.age),
    gender: Number(data.gender) as 1 | 2,
    ever_smoked: Number(data.everSmoked) as 1 | 2,
    smoking_frequency: data.everSmoked === "1"
      ? Number(data.smokingFrequency) as 1 | 2 | 3
      : null,
  };
}