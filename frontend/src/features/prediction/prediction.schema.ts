import { z } from "zod"; // zod = 입력한데이터가 지정한 조건에 맞는지 검증
import type { PredictionInput } from "../../api/prediction"; // prediction.ts 불러와라

// 입력폼 유효성 검증
export const predictionFormSchema = z.object({ // export = 외부에서 사용할 수 있게 하라
                                               // const  = 상수
                                               // predictionFormSchema = 예측 입력폼 유효성 검증용 스키마
                                               // z = zod
                                               // object() = 객체 속성과 각 속성 유효한 검증 규칙을 정의
  // 나이 조건 - 30~80세                                             
  age: z.string().min(1, "나이를 입력해 주세요.").refine( // z = zod
                                                        // .string() = 문자열로 검증
                                                        // .min()    = 문자열 최소 길이 지정
                                                        // .refine() = 직접 정의된 조건으로 추가 유효성 검증
    (v) => /^\d+$/.test(v) && Number(v) >= 30 && Number(v) <= 80, // (v) = 사용자가 입력한 나이 문자열을 전달
                                                                  // /^\d+$/ = 숫자만 있는 문자열 검사
                                                                  // .test(v) = v가 정규표현식에 맞는지 검사
                                                                  // && = and
                                                                  // Number(v) = 문자열 v를 숫자형으로 변환
                                                                  // 해석: Number(v)가 30~80인가
    "검사 가능 연령은 30~80세입니다.",
  ),
  // 성별 - 남 / 여
  gender: z.string() // z = zod
                     // .string() = 문자열 검증 
  .min(1, "성별을 선택해 주세요.") // .min(1, 경고문) = 최소 한글자 이상 입력하라
  .refine( // .refine() = 사용자정의 조건 추가 유효성 검증
    (v) => ["1", "2"].includes(v), // (v) = 성별 입력값
                                   // ["1", "2"]   = 성별값 허용은 1, 2 뿐
                                   // .includes(v) = 배열에 v가 일치하는지 확인 
    "성별을 다시 선택해 주세요."
  ),
  // 흡연 경험 - 유 / 무
  everSmoked: z.string() // z = zod
                         // .string() = 문자열 검증 
  .min(1, "흡연 경험을 선택해 주세요.") // .min(1, 경고문) = 최소 한글자 이상 입력하라
  .refine( // .refine() = 사용자정의 조건 추가 유효성 검증
    (v) => ["1", "2"].includes(v), // (v) = 성별 입력값
                                   // ["1", "2"] = 성별값 허용은 1, 2 뿐
                                   // .includes(v) = 배열에 v가 일치하는지 확인 
    "흡연 경험을 다시 선택해 주세요."
  ),
  // 흡연 빈도 - 유 / 무
  smokingFrequency: z.string(), // z = zod
                                // .string() = 문자열 검증 
}).superRefine((data, ctx) => { // .superRefine() = 사용자 정의 유효성 검증 및 오류 등록
                                // data = 입력데이터
                                // ctx  = 유효성검증오류 등록하는 context 객체
  if (!["1", "2", "3"].includes(data.smokingFrequency)) { // ![] = []가 아니라면
                                                          // .includes() = 배열에 특정값이 존재하는가
    console.warn("현재 흡연 상태가 선택되지 않았거나 유효하지 않습니다."); // .warn() = 콘솔에 경고메시지 출력
    // 유효성 검증 오류 등록
    ctx.addIssue({ // ctx = 유효성검증오류 등록하는 context 객체
                   // .addIssue() = superRefine 에서만 사용하며 오류메시지를 등록
      code: "custom", // code   = 코드에러라면
                      // custom = 개발자가 등록한 에러로 하라
      path: ["smokingFrequency"], // path = 오류가 발생한 데이터 속성의 경로
                                  // smokingFrequency = 흡연 빈도에 대한 오류
      message: "현재 흡연 상태를 선택해 주세요." // message = 오류메시지
    });
  }
});
// 스키마 기반 자료형 생성
export type PredictionFormValues = z.infer<typeof predictionFormSchema>; // export = 외부에서도 쓰게 하라
                                                                         // type   = tsx
                                                                         // PredictionFormValues = 예측 입력폼 자료형
                                                                         // z = zod
                                                                         // .infer = zod에 tsx 추가
                                                                         // <> = 제네릭
                                                                         // typeof = 변수의 tsx 타입 가져오라
                                                                         // predictionFormSchema = 유효성검증스키마

// 폼 초기 입력값
export const emptyPredictionForm: PredictionFormValues = { // export = 외부에서도 쓰게 하라
                                                           // const  = 상수(변경 불가)
                                                           // emptyPredictionForm  = 입력데이터 초기상태를 저장
                                                           // PredictionFormValues = 스키마 기반 자료형
  age: "", // "" = 처음엔 빈값으로
  gender: "",
  everSmoked: "",
  smokingFrequency: "",
};

// 입력데이터를 API 요청 형식으로 변환
export function toPredictionInput(data: PredictionFormValues): PredictionInput { // export = 외부에도 쓰게하라
                                                                                 // function = 함수
                                                                                 // toPredictionInput = 입력데이터 요청형식 변환
                                                                                 // data = 입력데이터
                                                                                 // :    = 자료형 지정
                                                                                 // PredictionFormValues = 입력폼 데이터 자료형
                                                                                 // PredictionInput = 예측 API 요청 데이터 자료형

  // 유효성 검증 오류 메시지 배열
  const errors: string[] = [];

  // 성별 유효성 검증
  if (data.gender !== "1" && data.gender !== "2") { // 성별값이 1이나 2가 아니라면
    console.error("성별 데이터 변환 실패: 허용되지 않는 입력값입니다."); // console.error() = 콘솔에 에러를 출력하라
    errors.push("성별 입력값이 올바르지 않습니다."); // errors = 에러 메시지 저장한 리스트 
  }                                                // .push() = 리스트 끝에 추가

  // 흡연 경험 유효성 검증
  if (data.everSmoked !== "1" && data.everSmoked !== "2") { // 흡연 경험이 1이나 2가 아니라면
    console.error("흡연 경험 데이터 변환 실패: 허용되지 않는 입력값입니다."); // console.error() = 콘솔에 에러를 출력하라
    errors.push("흡연 경험 입력값이 올바르지 않습니다."); // errors = 에러 메시지 저장한 리스트 
  }                                                    // .push() = 리스트 끝에 추가

  // 현재 흡연 상태 유효성 검증
  if (!["1", "2", "3"].includes(data.smokingFrequency)) { // !["1", "2", "3"] = 1 2 3이 아니라면
                                                          // .includes() = 일치하는지 확인
    console.error("현재 흡연 상태 데이터 변환 실패: 입력값이 누락되었거나 유효하지 않습니다."); // console.error() = 콘솔에 에러를 출력하라
    errors.push("현재 흡연 상태를 선택해 주세요."); // errors = 에러 메시지 저장한 리스트 
  }                                               // .push() = 리스트 끝에 추가

  // 모든 유효성 검증이 끝난 후 오류 일괄 처리
  if (errors.length > 0) { // 에러가 1개 이상이라면
    throw new Error(errors.join("\n")); // throw   = 예외 발생
  }                                     // new     = 새로운 것 생성
                                        // Error   = 에러 발생
                                        // errors  = 에러담은 리스트
                                        // .join() = 리스트의 모든 요소를 하나의 문자열로 연결
                                        // "\n"    = 줄바꿈

  // API 요청 데이터 반환
  return {
    age: Number(data.age), // Number = 숫자형(int / float)
                           // data   = 입력데이터
    gender: Number(data.gender) as 1 | 2, // as = 타입 단원 키워드
    ever_smoked: Number(data.everSmoked) as 1 | 2,
    smoking_frequency: data.everSmoked === "2" ? null : (Number(data.smokingFrequency) as 1 | 2 | 3),
  };
}