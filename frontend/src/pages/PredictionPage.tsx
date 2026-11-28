import { useCallback, useEffect, useRef, useState } from "react"; // useCallback = 함수의 참조 재사용하는 React Hook
                                                                  // useEffect = 컴포넌트 렌더링 후 특정 작업 실행하는 React Hook
                                                                  // useRef = 특정값을 유지 or HTML요소를 직접 참조하는 React Hook
                                                                  // useState = 컴포넌트의 상태값 저장 or 변경하는 React Hook
import {
  getPredictionError, // getPredictionError = 예측 작업에 중 생긴 오류를 메시지로 변환
  predictPeriodontal, // predictPeriodontal = 치주질환 예측 API 요청 
  type PredictionResponse,  // PredictionResponse = 전체 예측 응답 데이터의 자료형
} from "../api/prediction"; // prediction.ts 파일 불러오라
import { AnalysisModal } from "../components/AnalysisModal"; // AnalysisModal = 치주질환 분석 모달 컴포넌트
                                                             // AnalysisModal.tsx 불러와라
import {
  toPredictionInput, // toPredictionInput = 입력폼 데이터를 API 요청 데이터 형식으로 변환
  type PredictionFormValues, // PredictionFormValues = 입력폼 데이터의 자료형
} from "../features/prediction/prediction.schema"; // prediction.schema.ts 파일 불러오라

// 치주질환 예측 페이지
export function PredictionPage() { // export = 외부 파일에서 사용할 수 있도록 허용
                                   // function = 함수
  // 모달 상태 관리                                 
  const [modalOpen, setModalOpen] = useState(false); // const = 상수
                                                     // modalOpen = 모달 열기
                                                     // setModalOpen = 모달 열림 여부 저장
                                                     // useState() = 컴포넌트 상태값 관리하는 React Hook
                                                     // (false) = 처음엔 모달 닫혀있음
  const [result, setResult] = useState<PredictionResponse | null>(null); // result = 치주질환 예측 결과를 저장
                                                                         // setResult = result값 변경
                                                                         // useState() = 컴포넌트 상태값 관리하는 React Hook
                                                                         // <PredictionResponse | null> = PredictionResponse 이거나 Null
                                                                         // PredictionResponse = 전체 예측 응답 데이터
                                                                         // (null) = 처음엔 결과값 x
  const [error, setError] = useState(""); // error = 오류 메시지를 저장
                                          // setError = error 상태값 변경
                                          // useState() = 컴포넌트 상태값 관리하는 React Hook
                                          // ("") = 처음엔 오류 메시지 없음
  const [loading, setLoading] = useState(false); // loading = 예측 진행 여부 저장
                                                 // setLoading = loading 상태값 변경
                                                 // useState() = 컴포넌트 상태값 관리하는 React Hook
                                                 // (false) = 처음엔 작업 진행 x 
  // API 요청 취소                                               
  const abortRef = useRef<AbortController | null>(null); // abortRef = API요청 취소되었다는 사실을 저장
                                                         // useRef = 렌더링 반복되어도 특정값 유지
                                                         // <AbortController | null> = AbortController 이거나 null
                                                         // AbortController = 비동기 작업 취소용 
                                                         // (null) = 처음엔 결과값 x
  // 컴포넌트 제거 시 기존 요청 취소
  useEffect(() => () => abortRef.current?.abort(), []); // useEffect() = 컴포넌트 렌더링 후 특정 작업 실행
                                                        // () =>       = useEffect()용 롤백함수
                                                        //               롤백함수: 
                                                        // () =>       = 클린업 함수
                                                        //               클린업 함수: 
                                                        // abortRef = API요청 취소되었다는 사실을 저장
                                                        // current  = Ref 객체에 저장된 값에 접근
                                                        // ? = 앞의 값이 Null 이거나 undefined가 아닌 경우 실행하라
                                                        // .abort() = 비동기 작업 취소시 신호 보냄
                                                        // [] = 빈 의존성 배얼
  // 예측 관련 상태 초기화
  const clearPrediction = useCallback(() => { // clearPrediction = 예측 관련 상태를 초기화
                                              // useCallback()   = 함수의 참조를 재사용하는 React Hook
    abortRef.current?.abort(); // abortRef = API요청 취소되었다는 사실을 저장
                               // current  = Ref 객체에 저장된 값에 접근
                               // ? = 앞의 값이 Null 이거나 undefined가 아닌 경우 실행하라
                               // .abort() = 비동기 작업 취소시 신호 보냄
    abortRef.current = null;   // 요청 취소 객체 초기화 
    setLoading(false); // 예측 작업의 진행 상태 초기화
    setResult(null);   // 기존 예측 결과 초기화
    setError("");      // 기존 오류 메시지 초기화
  }, []); // [] = 빈 의존성 배열 설정

  // 모달 닫기
  const closeModal = useCallback(() => { // useCallback() = 함수의 참조를 재사용하는 React Hook
    clearPrediction();   // clearPrediction()   = 기존 요청 취소 및 예측 관련 상태 초기화
    setModalOpen(false); // setModalOpen(false) = 모달 닫기로 변경
  }, [clearPrediction]); // [clearPrediction]   = useCallback의 의존성 배열

  // 모달 열기
  const openModal = useCallback(() => { // useCallback() = 함수의 참조를 재사용하는 React Hook
    clearPrediction();   // clearPrediction()   = 기존 요청 취소 및 예측 관련 상태 초기화
    setModalOpen(true);  // setModalOpen(true)  = 모달 열기로 변경
  }, [clearPrediction]); // [clearPrediction]   = useCallback의 의존성 배열

  // 치주질환 예측 실행
  const handlePredict = useCallback(async (values: PredictionFormValues) => { // handlePredict = 치주질환 예측 처리
                                                                              // useCallback() = 함수의 참조를 재사용하는 React Hook
                                                                              // async  = 비동기
                                                                              // values = 입력폼데이터 전달받기 
                                                                              // PredictionFormValues = 입력폼데이터 자료형
    abortRef.current?.abort(); // abortRef = API요청 취소되었다는 사실을 저장
                               // current  = Ref 객체에 저장된 값에 접근
                               // ? = 앞의 값이 Null 이거나 undefined가 아닌 경우 실행하라
                               // .abort() = 비동기 작업 취소시 신호 보냄
    const controller = new AbortController(); // new = 새로운 객체 생성
                                              // AbortController() = 비동기 작업 취소 제어
    abortRef.current = controller; // abortRef   = API요청 취소되었다는 사실을 저장
                                   // current    = Ref 객체에 저장된 값에 접근
                                   // controller = 현재 요청의 취소용
    // 분석 시작시 설정                               
    setLoading(true); // 진행중
    setError("");     // 에러메시지 없음
    setResult(null);  // 결과값 없음
    try {
      // 치주질환 예측 API 요청
      const data = await predictPeriodontal( // data  = API에서 반환한 예측 응답 데이터 저장
                                             // await = Promise 완료될 때 까지 비동기 함수 실행 대기
                                             // predictPeriodontal() = 치주질환 예측 API 요청 횟수
        // 입력데이터 변환                                     
        toPredictionInput(values), // toPredictionInput() = 입력폼데이터를 API 요청 형식으로 변환
                                   // values = 입력폼 데이터
        // API 요청 취소 전달                           
        controller.signal, // controller = AbortController의 객체
                           // AbortController = 비동기 작업 취소 제어
      );                   // signal = 취소 신호 전달(AbortSignal의 객체)
      // 요청 취소 여부 확인 및 예측 결과 저장
      if (!controller.signal.aborted) setResult(data); // !controller = controller가 아니라면
                                                       // signal  = 취소 신호 전달
                                                       // aborted = 취소 신호 발생 여부 저장
                                                       // setResult() = 예측 응답 데이터를 result 상태에 저장
      // 오류 시 
    } catch (err: unknown) { // err = 에러
                             // unknown = 모든 자료형을 전달받을 수 있는 tsx 객체
      // 오류 메시지 저장                       
      if (!controller.signal.aborted) setError(getPredictionError(err)); // !controller = controller가 아니라면
                                                                         // signal  = 취소 신호 전달
                                                                         // aborted = 취소 신호 발생 여부 저장
                                                                         // setError() = error 상태값 변경
                                                                         // getPredictionError() = 오류메시지로 변환
                                                                         // err = 발생한 오류
    // 예측 작업 종료 처리                                                                     
    } finally {
      // 현재 요청 객체 확인
      if (abortRef.current === controller) { // abortRef   = API 요청 취소용 객체를 저장
                                             // current    = 현재 저장된 AbortController 객체
                                             // controller = 현재 함수에서 생성한 AbortController 객체
        abortRef.current = null; // abortRef = API 요청 취소용 객체를 저장
                                 // current  = Ref에 저장된 값에 접근
                                 // null = 완료된 요청의 AbortController 객체 참조 제거
        setLoading(false); // setLoading() = loading 상태값을 변경
      }                    // (false) = 예측 작업 진행 x
    }
  }, []); // [] = 빈 의존성 배열 

  return (
    <main id="top">
      <section className="hero" aria-labelledby="hero-heading">
        <div className="hero__inner">
          <h1 id="hero-heading">치주질환 위험도</h1>
          <span className="hero__rule" aria-hidden="true" />
          <p className="hero__intro">
            입력한 정보를 바탕으로
            <br />
            치주질환의 위험도를 AI가 예측합니다.
          </p>
          <button type="button" className="hero__cta" onClick={openModal}>
            시작하기<span aria-hidden="true"></span>
          </button>
        </div>
      </section>
      {modalOpen && (
        <AnalysisModal
          onClose={closeModal}
          onPredict={handlePredict}
          onReset={clearPrediction}
          onTryAgain={clearPrediction}
          isLoading={loading}
          result={result}
          error={error}
        />
      )}
    </main>
  );
}
