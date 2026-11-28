import axios from "axios"; // axios = 프론트에서 백엔드로 HTTP 요청 보내고 응답 받음

// API 불러오기
const apiBaseUrl = import.meta.env.VITE_API_URL?.trim(); // const = 상수 - 수정 및 삭제 x
                                                         // .meta = 메타데이터 제공
                                                         // .env  = env 제공
                                                         // VITE_API_URL = env의 환경변수
                                                         // ? = 옵셔널 체이닝 연산자
                                                         //     값이 undefiend나 null이면 환경변수대신 undefiend
                                                         // .trim() = 문자열 앞뒤 공백 제거

// axios 기본 설정  
// .create() 덕에 매번 API주소 + 시간제한 적지 않아도 됨                                                       
export const apiClient = axios.create({ // export    = 다른 파일도 사용할 수 있게 하라
                                        // const     = 상수
                                        // axios     = axios 모듈 가져와라
                                        // .create() = axios 인스턴스 생성하라
  baseURL: apiBaseUrl, // baseURL = HTTP에 요청할 기본응답주소 설정
  timeout: 15000,      // timeout = 요청시간 제한: 15,000(15초)
  headers: { "Content-Type": "application/json" }, // headers = HTTP요청헤더 설정
});                                                // Content-Type = HTTP메시지 본문 데이터 형식
                                                   // application/json = 데이터형식은 JSON이라는 선언

// API 설정 체크                                                   
export function assertApiConfigured(): void { // export   = 다른 파일도 사용할 수 있게 하라
                                              // function = 함수
                                              // void = 반환값 없음
  // API 주소가 없다면                                              
  if (!apiBaseUrl) { // ! = not 연산자
                     // apiBaseUrl = API 기본주소
    // 개발자용 오류 로그
    console.error("VITE_API_URL이 설정되지 않았습니다."); // console  = 콘솔 출력하라
                                                        // .error() = 오류 메시지 출력하라
                                                        // console.error() = 오류메시지를 출력하지만 실행 중단은 안함
    // 웹에 보일 오류
    throw new Error("서비스 연결에 문제가 발생했습니다. 잠시 후 다시 시도해 주세요."); // throw = 예외 발생 시커라
                                                                                  // new   = 새로운 객체 생성하라
                                                                                  // Error = 에러를 생성하라
  }                                                                                  
}         // console.error()        
          // 메시지출력 - 가능       
          // 예외발생   - 불가능     
          // 실행중단   - 불가능     
          // try-catch - 불가능     
          
          // throw new Error()
          // 메시지출력 - 가능
          // 예외발생   - 가능 
          // 실행중단   - 가능
          // try-catch - 가능