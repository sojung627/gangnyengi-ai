import axios from "axios"; // axios = 프론트에서 백엔드로 HTTP 요청 보내거나 응답 받음
import { z } from "zod";   // z = Zod의 스키마 정의 및 검증도구 불러와라
                           // zod = 데이터 구조 및 유효성 검증
import { apiClient, assertApiConfigured } from "./client"; // apiClient = axios 기본 설정
                                                           //             client.ts에서 생성한 const
                                                           // assertApiConfigured = API주소 유뮤 체크
                                                           //                       client.ts에서 생성한 function
                                                           // from "./client"; = client.ts

// 요청데이터 인테페이스 정의                                                           
export interface PredictionInput { // backend/schemas.py의 PredictionInput/PredictionResponse와 동일한 계약
                                   // export = 외부에서도 사용가능하게 하라
                                   // interface = 인터페이스
                                   //             인터페이스: 객체가 어떤 속성 + 값을 가졌는가 정의하라
  // 인터페이스 정의                                   
  age: number;   // 나이 = 숫자(정수 or 실수)
  gender: 1 | 2; // 성별 = 1 or 2
  ever_smoked: 1 | 2; // 흡연경험 = 1 or 2
  smoking_frequency: 1 | 2 | 3; // 흡연빈도 = 1 or 2 or 3
}

// 예측결과 조건 설정
const modelPredictionSchema = z.object({ // const = 상수
                                         // z = zod(데이터구조 및 유효성을 검증하라)
                                         // .object() = 객체구조정의 및 검증하라
  // 예측확률                                       
  probability: z.number().min(0).max(1), // z = 데이터구조 및 유효성 검증하라
                                         // .number() = 숫자타입인가
                                         // .min() = 최소값은 ()만 해라
                                         // .max() = 최대값은 ()만 해라
                                         // 해석:예측확률은 숫자여야만 하고 0~1만 가능
                                         
  // 최종예측결과
  prediction: z.union([z.literal(0), z.literal(1)]), // z = 데이터구조 및 유효성 검증하라
                                                     // .union()   = 여러 검증 조건 중 하나만 통과해도 허용 가능
                                                     // .literal() = 조건과 정확히 일치하는가
                                                     // 해석: 최종예측결과는 0 or 1만 가능
  // 예측임계값
  threshold: z.number().min(0).max(1), // z = 데이터구조 및 유효성 검증하라
});                                    // .number() = 숫자타입인가
                                       // .min() = 최소값은 ()만 해라 
                                       // .max() = 최대값은 ()만 해라
                                       // 해석: 예측임계값은 숫자여야만하고 0~1만 가능

// 전체예측응답 조건 설정                                      
const predictionResponseSchema = z.object({ // const = 상수
                                            // z = 데이터구조 및 유효성 검증
                                            // .object() = 객체구조정의 및 검증
  // 로지스틱회귀모델                                          
  logistic_regression: modelPredictionSchema, // modelPredictionSchema = 예측결과 조건 설정
                                              // 예측확률     = 0~1
                                              // 최종예측결과 = 0 or 1
                                              // 예측임계값   = 0~1
  // XGBoost모델(앙상블모델)
  xgboost: modelPredictionSchema,
  // MLP모델
  pytorch_mlp: modelPredictionSchema,
  // 면책 및 주의사항 안내
  disclaimer: z.string(), // z = 데이터구조 및 유효성 검증
});                       // .string() = 문자열타입이여야 한다

// 각 모델 결과를 zod에서 --> tsx로 변환
export type ModelPrediction = z.infer<typeof modelPredictionSchema>; // export = 외부에서도 사용할 수 있게하라
                                                                     // type   = tsx
                                                                     // ModelPrediction = 게별모델결과
                                                                     // z = 데이터구조 및 유효성 검증
                                                                     // .infer<> = zod를 tsx로 변환
                                                                     // typeof   = 타입의 특정값을 가져와라 
                                                                     // modelPredictionSchema = 예측결과조건 설정                                                                 
// 전체예측응답을 zod에서 --> tsx로 변환
export type PredictionResponse = z.infer<typeof predictionResponseSchema>; // exprot = 외부에서도 사용할 수 있게하라
                                                                           // type   = tsx
                                                                           // PredictionResponse = 전체예측응답
                                                                           // z = 데이터구조 및 유효성 검증
                                                                           // .infer<> = zod를 tsx로 변환
                                                                           // typeof   = 타입의 특정값을 가져와라
                                                                           // predictionResponseSchema = 전체예측응답 조건 설정

// 치주질환 예측                                                                           
export async function predictPeriodontal( // export   = 외부에서도 사용하라
                                          // async    = 비동기
                                          // function = 함수
  // 데이터 타입                                        
  data: PredictionInput, // data = 데이터 전달
                         // PredictionInput = 요청데이터 타입
                         //                   나이 - number(정수 or 실수)
                         //                   성별 - 1 or 2
                         //                   흡연경험 - 1 or 2
                         //                   흡연빈도 - 1 or 2 or 3 or Null
  // 요청 취소 시                        
  signal?: AbortSignal, // signal = 요청 취소됨을 전달
                        // ? = Null 허용
                        // AbortSignal = 비동기작업 취소 신호 그 자체
   // 작업 결과                     
): Promise<PredictionResponse> { // Promise - 비동기작업 결과 or 실패 전달
                                 // <PredictionResponse>  = 전체응답예측
  // API 주소 유무 확인                               
  assertApiConfigured(); // assertApiConfigured() = API 주소 유무 확인 
  // 백엔드 API 요청
  const response = await apiClient.post<unknown>("/predict", data, { signal }); // const = 상수
                                                                                // await = 비동기작업 완료까지 기다려라
                                                                                // apiClient = axios기본설정
                                                                                // .post = POST로 보내라
                                                                                // <unknown> = 응답 자료형 뭔지 모른다
                                                                                // /predict  = 엔드포인트
                                                                                // data = 백엔드에 보낼 요청데이터
                                                                                // { signal } = 요청취소 전달용
  // 백엔드 응답 검증                                                                              
  return predictionResponseSchema.parse(response.data); // return = 반환하라
}                                                       // predictionResponseSchema = 전체예측응답 조건 검증
                                                        // .parse() = 전달데이터가 조건을 충족하는가
                                                        // response = axios의 HTTP 응답
                                                        // .data = HTTP의 본문데이터

// 오류 처리                                                        
export function getPredictionError(error: unknown): string { // export   = 외부에서도 사용할 수 있게 하라
                                                             // function = 함수
                                                             // getPredictionError = 오류메시지 가져올 함수명
                                                             // error    = 오류데이터
                                                             // unknown  = 자료형 모름
                                                             // : string = 반환값은 str이여야 함
  // API 취소 여부 확인                                                           
  if (axios.isCancel(error)) { // axios = 프론트에서 백엔드로 HTTP 요청보내고 응답받아옴
                               // .isCancel(error) = axios 취소로 인한 오류인지 확인
    console.info("API 요청이 취소되었습니다."); // console = 콘솔에 출력하라
                                              // .info() = 정보성 메시지 출력하라
                                              // console.info() = 콘솔에 정보 출력하라
    return "검사가 취소 되었습니다."; // return = 반환 후 종료하라
  }

  // zod오류 여부 확인
  if (error instanceof z.ZodError) { // error = 오류
                                     // instanceof = 객체가 특정클래스의 인스턴스인지 확인
                                     // z = zod(데이터구조 및 유효성 검증)
                                     // ZodError = zod 오류
    console.error("API 응답 스키마 불일치:", error.issues); // console = 콘솔에 출력하라
                                                           // .error() = 오류
                                                           // .issue   = zod검증 실패 정보 저장 
    return "검사 결과를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요."; // return = 반환 후 종료하라
  }

  // axios오류 여부 확인
  if (axios.isAxiosError(error)) { // axios = 프론트에서 백엔드로 HTTP 요청보내고 응답 받아와라
                                   // .isAxiosError() = axios에 의한 오류인가
    const detail: unknown = error.response?.data?.detail; // const  = 상수 
                                                          // detail = 상세정보
                                                          // : unknown = 자료형 모름
                                                          // .response = 서버가 준 HTTP 응답
                                                          // .data   = HTTP 응답 본문
                                                          // .detail = 백엔드에서 전달한 상세오류 정보
                                                          // ? = Null 허용
                                                          
    // 문자열 오류 확인
    if (typeof detail === "string") { // typeof = 값의 자료형을 확인하라
                                      //          python의 dtype과 비슷한듯
                                      // detail = 오류 상세정보
                                      // ===    = 값과 자료형이 모두 일치하는가
      console.error("백엔드 오류가 발생했습니다:", detail); // console = 콘솔에 출력하라
      return "검사 진행 중 문제가 발생했습니다. 잠시 후 다시 시도해 주세요."; // return = 반환 후 종료하라
    }

    // 배열 오류 확인
    if (Array.isArray(detail)) { // Array = 배열
                                 // .isArray() = 배열이 맞는가
                                 // detail = 오류 상세정보
      const messages = detail // const = 상수
        .filter( // .filter() = 조건을 충족하는 것들만 추출하여 새로운 배열을 만들어라
          (item): item is { msg: string } => // item = 배열의 개별 요소
                                             // is = 조건이 참이면 item을 지정된 자료형으로 취급하라
                                             // {msg: string} = 조건
                                             // =>   = 화살표 함수
                                             //        ex) 일반함수
                                             //            function add(a: number, b: number) {
                                             //               return a + b;
                                             //            }
                                             //            화살표 함수
                                             //            const add(a: number, b: number) => {
                                             //               retunr a + b;
                                             //            };
                                             //        일반함수 축약버전
            Boolean(item) && typeof item.msg === "string", // Boolean = 값을 True / False로 만듦
                                                           // item = 배열 개별요소
                                                           // &&   = AND (모두 다 True여야한다)
                                                           // typeof   = 값의 자료형을 문자열로 변환하라
                                                           // item.msg = 배열 개별요수 중 msg
                                                           // ===      = 값과 자료형이 모두 일치하는가 (==보다 강력함)
        )
        .map((item) => item.msg); // .map()   = 새로운 배열 반환하라
                                  // item     = 배열 개별요소
                                  // =>       = 화살표 함수
                                  // item.msg = 배열 개별요소중 msg만

      // 오류메시지 개수 확인                            
      if (messages.length) { // .length = 길이
        console.error("백엔드 데이터 검증 오류:", messages); // console = 콘솔에 출력하라
                                                           // .error() = 에러 출력하라
        return "입력하신 정보를 다시 확인해 주세요."; // return = 반환 후 종료하라
      }
    }

    // 응답시간 초과 확인
    if (error.code === "ECONNABORTED") { // error = axios 에러 객체
                                         // .code = 오류 코드 저장
                                         // ===   = ==보다 까다로운 확인(모든 조건이 같아야 함)
                                         // ECONNABORTED = axios전용 오류코드
                                         //                요청시간 초과시 나타나는 오류코드
      console.error("API 서버 응답 시간이 초과되었습니다.");
      return "검사 결과를 불러오는 데 시간이 오래 걸리고 있습니다. 잠시 후 다시 시도해 주세요.";
    }

    // 서버응답이 존재하지 않는가
    if (!error.response) { // ! = not
                           // error    = axios 에러 객체
                           // response = HTTP 응답
                           // 실행되는 경우: 서버를 실행하지 않거나 네트워크 오류, CORS 문제로 응답을 받지 못하였을 때
      console.error(
        "API 서버 연결 실패. 서버 실행 상태와 환경변수를 확인해 주세요.",
      );
      return "서비스에 연결할 수 없습니다. 인터넷 연결을 확인하거나 잠시 후 다시 시도해 주세요.";
    }

    console.error("HTTP 요청 실패:", error.response.status); // error = axios 에러 객체
                                                            // response = HTTP 응답
                                                            // status   = HTTP 상태코드
    return `검사 진행 중 문제가 발생했습니다. 잠시 후 다시 시도해 주세요. (HTTP ${error.response.status})`;
    // ``  = 템플릿 리터럴 작성
    //       템플릿 리터럴: 문자열 안에 변수나 연산결과 직접 삽입
    // ${} = 표현식 및 결과 삽입
  }

  console.error("예상하지 못한 오류가 발생했습니다:", error);
  return "일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.";
}
