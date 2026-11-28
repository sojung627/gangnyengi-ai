import { useEffect, useRef } from "react"; // useEffext = 컴포넌트를 화면에 표시한 뒤 작업실행 시 사용하는 react hook 
                                           // useRef = 특정값 저장하거나 HTML요소 직접 참조시키는 react hook
                                           // react  = react 라이브러리 
                                           // react hook   = react의 상태관리나 HTML요소 접근 허용시켜 react기능 사용하게 함
import { createPortal } from "react-dom";  // createPortal = HTML을 지정한 DOM위치에 렌더링
                                           // react-dom    = react와 브라우저 DOM을 연결
                                           // DOM = Document Object Model
                                           //       브라우저가 HTML을 JS로 접근하거나 JS로 수정할 수 있게 만들어줌
                                           // Portal = HTML을 이전 부모 HTML요소 내부가 아닌 다른위치에 표기
import { PredictionForm } from "../features/prediction/PredictionForm"; // = PredictionForm.tsx 가져와라
import { PredictionResults } from "../features/prediction/PredictionResults"; // PredictionResults.tsx 가져와라
import type { PredictionResponse } from "../api/prediction"; // prediction.ts 가져와라
import type { PredictionFormValues } from "../features/prediction/prediction.schema"; // prediction.schema.ts 가져와라
import "./AnalysisModal.css"; // AnalysisModal.css 가져와라

// 컴포넌트 Props 인터페이스 정의
interface AnalysisModalProps { // interface = 객체가 가질 속성과 자료형을 정의
                               // props = 부모컴포넌트에서 자식컴포넌트로 전달
  onClose: () => void; // onClose = 모달 닫기
                       // :  = 속성 자료형 지정
                       // () = 매개변수가 없음
                       // => = 화살표함수
                       // void = 반환값 x
  onPredict: (values: PredictionFormValues) => Promise<void>; // onPredict = 에측실행함수를 전달받음
                                                              // values    = 입력폼 데이터 전달받음
                                                              // : = 속성 자료형 지정
                                                              // PredictionFormValues = 입력폼 데이터의 자료형
                                                              // Promose = 비동기작업 성공 or 실패 결과
                                                              // <void>  = 비동기작업 성공 시 결과값 제공 x
  onReset: () => void; // onReset = 입력값을 초기화
                       // :    = 속성 자료형 지정
                       // ()   = 매개변수가 없음
                       // void = 반환값 x
  onTryAgain: () => void; // onTryAgain = 재분석 실행
                          // :    = 속성 자료형 지정
                          // ()   = 매개변수가 없음
                          // void = 반환값 x 
  isLoading: boolean; // isLoading = 현 작업이 진행중인가
                      // : = 속성 자료형 지정
                      // boolean = True or False
  result: PredictionResponse | null; // result = 예측 결과 전달
                                     // PredictionResponse = 전체 예측 응답 자료형
  error: string; // 에러는 str
}

// AnalysisModal 컴포넌트 선언
export function AnalysisModal({ // 객체구조분할: 객체에 저장된 속성을 각 변수별로 꺼내어 사용
                                // export = 외부에서 사용 허가하라
                                // function = 함수
  onClose,    // 모달닫기 함수
  onPredict,  // 치주질환 예측 함수
  onReset,    // 입력값 초기화 함수
  onTryAgain, // 재분석 함수
  isLoading,  // 분석 진행 여부
  result,     // 예측 결과
  error,      // 에러 
}: AnalysisModalProps) { // AnalysisModalProps = 전달받은 매게변수 자료형
  // HTML요소 참조변수 생성
  // 제네릭: 함수나 클래스를 사용할 때 어떠한 타입으로 지정하여 사용
  
  // 모달 영역 참조
  const dialogRef = useRef<HTMLDivElement>(null); // const = 상수
                                                  // dialogRef = div요소 참조용 변수
                                                  // useRef()  = 값 유지 or HTML요소 참조하라
                                                  // <HTMLDivElement> = HTML div 자료형으로 지정
                                                  // (null) = 초기엔 참조할 값이 없다는 뜻
  // 닫기 버튼 참조                                                
  const closeRef = useRef<HTMLButtonElement>(null); // const = 상수
                                                    // closeRef = 닫기버튼 참조용
                                                    // useFef() = 값 유지 or HTML요소 참조하라
                                                    // <HTMLButtonElement> = HTML button 자료형으로 지정
                                                    // (null) = 초기엔 참조할 값이 없다는 뜻
  // 이전 포커스 요소 참조
  const previousFocusRef = useRef<HTMLElement | null>(null); // const = 상수
                                                             // previousFocusRef = 전에 설정한 HTML요소 저장
                                                             // useRef = 값 유지 or HTML요소 참조하라
                                                             // HTMLElement = 일반적인 HTML 요소
                                                             // <HTMLElement | null> = 일반적인 HTML요소거나 Null
                                                             // (null) = 초기에는 null이다
                                                             
                                                             // 참조할 수 있는 요소
                                                             // HTMLDivElement    == div
                                                             // HTMLButtonElement == button
                                                             // HTMLElement == 일반적인 요소                                               
  
  // 모달 뜰 때 실행할 것들
  useEffect(() => { // useEffect() = 컴포넌트 렌더링 이후 특정 작업을 실행하는 react hook
                    // () = 현재 매개변수 없음
    previousFocusRef.current = // previousFocusRef = 이전 포커스 요소 저장하는 Ref 객체
                               // .current = Ref 객체 값에 접근
      document.activeElement instanceof HTMLElement // document = 현 파일
                                                    // activeElement = 포커스 설정된 요소들
                                                    // instanceof  = 객체가 특정클래스 인스턴스인가
                                                    // HTMLElement = 일반적인 HTML 요소
        ? document.activeElement // ? = 조건이 True면 사용하라
                                 // document = 문서
                                 // activeElement = 포커스 설정된 요소들
        : null; // : null = 조건이 거짓일 경우 null을 저장하라
    // 기존 스크롤 저장 및 스크롤 차단    
    const previousOverflow = document.body.style.overflow; // const = 상수
                                                           // previousOverflow = 기존 스크롤 설정 저장
                                                           // document = 현 파일
                                                           // body  = HTML의 body
                                                           // style = HTML의 CSS
                                                           // overflow = 요소영역 벗어난 콘텐츠 처리방식
    document.body.style.overflow = "hidden"; // hidden = overflow들 숨기기
    closeRef.current?.focus(); // closeRef = 모달닫기 버튼의 Ref 객체
                               // current  = Ref 객체에 저장된 HTML 요소
                               // ? = Null이나 undefined가 아니면 실행하라
                               // focus() = 해당 HTML요소에 포커스 설정하라
    
    // 키보드 이벤트 처리
    function onKeyDown(event: KeyboardEvent) { // function = 함수
                                               // event = 발생한 이벤트객체 전달
                                               // : = 매개변수 자료형 지정
                                               // KeyboardEvent = 키보드이벤트 객체 자료형
      // ESC키 - 누르면 모달 닫음                                        
      if (event.key === "Escape") { // event = 이벤트
                                    // key   = 키 
                                    // 해석: ESC키가 눌렸다면
        event.preventDefault(); // event = 이벤트
                                // .preventDefault() = 브라우저 기본동작 방지
        onClose(); // onClose() = 모달닫기 함수 실행
        return;    // return = 반환 + 종료
      }
      // TAB키 - 다음 input으로 이동
      if (event.key !== "Tab" || !dialogRef.current) return; // event.key !== "Tab" = 이벤트키가 TAB이 아니라면
                                                             // ! = not
                                                             // dialogRef = 모달 참조하는 Ref
                                                             // current   = Ref에 저장된 HTML요소
                                                             // return = 반환 + 종료
      // 포커스 설정할 수 있는 HTML 요소 검색                                                       
      const focusable = Array.from( // const = 상수
                                    // Array.from() = 유사배열객체 or 반복가능한객체를 배열로 반환
        // HTML 요소 검색                            
        dialogRef.current.querySelectorAll<HTMLElement>( // dialogRef = 모달 참조하는 Ref
                                                         // current   = Ref에 저장된 HTML요소
                                                         // querySelectorAll = 지정된 CSS랑 일치하는 모든 요소 검색
                                                         // <HTMLElement> = 검색한 요소를 HTMLElement로 지정
          'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])',
        ), // a[href] = href가 존재하는 a태그
      );   // button:not([disabled]) = 비활성화 안된 버튼
           // input:not([disabled])  = 비활성화 안된 입력요소
           // select:not([disabled]) = 비활성화 안된 선택요소
           // textarea:not([disabled]) = 비활성화 안된 textarea
           // [tabindex]:not([tabindex="-1"]) = tabindex속성이 있고 값이 -1이 아닌 요소
      // 포커스 가능한 요소 확인     
      if (!focusable.length) { // ! = not
                               // focusable = 포커스 가능한 것들의 배열
                               // length = 길이
        event.preventDefault(); // event = 이벤트
                                // .preventDefault() = TAB의 기본동작 방지
        return; // return = 반환 + 종료
      }
      // 첫번째 요소와 마지막 요소 저장
      const first = focusable[0]; // const = 상수
                                  // focusable = 포커스 가능한 것들의 배열
                                  // [0] = 첫번째 요소 
      const last = focusable[focusable.length - 1]; // [focusable.length - 1] = focusable배열의 마지막 요소
      // SHIFT + TAB키 - 이전 input으로 이동
      if (event.shiftKey && document.activeElement === first) { // event = 이벤트
                                                                // shiftKey = SHIFT키
                                                                // && = 모든 조건이 True
                                                                // document = 현 파일
                                                                // activeElement = 포커스 설정된 요소들
                                                                // first = 첫번째 요소
        event.preventDefault(); // event = 이벤트
                                // .preventDefault() = 브라우저 기본동작 방지
        last.focus(); // 마지막 포커스 실행
        // 일반 TAB 처리
      } else if (!event.shiftKey && document.activeElement === last) { // !event.shiftKey = SHIFT키 안눌렀다면
                                                                       // && = 모든 조건이 True
                                                                       // document.activeElement === last = 포커스의 마지막요소
        event.preventDefault(); // 브라우저 기본동작 방지
        first.focus(); // 첫번째 포커스 실행
      }
    }
    // 키보드 이벤트 등록
    document.addEventListener("keydown", onKeyDown); // document = 현 파일
                                                     // .addEventListener() = 특정 이벤트 발생 시 사용
                                                     // "keydown" = 키 누르면
                                                     // onKeyDown = 키 누르면 발생할 이벤트
    return () => { // 클린업함수: useEffect()에서 반환할 함수
                   // return = 반환 + 종료
                   // () = 빈 매개변수
      document.removeEventListener("keydown", onKeyDown); // .removeEventListener() = 이벤트 리스너 제거
                                                          // "keydown" = 제거할 이벤트 
                                                          // onKeyDown = 제거할 이번트 처리
      document.body.style.overflow = previousOverflow; // body     = html의 body요소
                                                       // style    = 인라인 CSS에 접근
                                                       // overflow = 영역 벗어난 것들 처리
                                                       // previousOverflow = 모달켜기 전 저장한 overflow 설정
      previousFocusRef.current?.focus(); // previousFocusRef = 이전 포커스 요소 저장한 Ref 객체
                                         // current = Ref객체에 저장된 HTML 요소들
                                         // ? = null이나 undefined 아니면 실행
                                         // focus() = 해당 HTML요소 포커스
    };
  }, [onClose]); // [onClose] = useEffect 의존성 배열
                 // onClose   = 모달닫는 함수 실행

  // 모달 렌더링 - 화면에 뜰 것들               
  return createPortal(
    <div
      className="analysis-backdrop"
      onMouseDown={(event) => { // onMouseDown = 마우스버튼 누르면 실행
                                // (event) => {} = 이벤트가 발생하면 {}를 실행하라
        if (event.target === event.currentTarget) onClose();
      }} // event.target = 이벤트가 발생한 요소
         // event.currentTarget = 이벤트처리할 함수 
    >    
      <div
        ref={dialogRef} 
        className="analysis-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="analysis-modal-title"
        aria-describedby="analysis-modal-description"
      >
        <button
          ref={closeRef}
          type="button"
          className="analysis-modal__close"
          onClick={onClose}
          aria-label="분석 창 닫기"
        >
          <span aria-hidden="true">×</span>
        </button>
        <header className="analysis-modal__heading">
          <h2 id="analysis-modal-title">치주질환 위험도</h2>
        </header>
        {result ? (
          <div className="analysis-modal__results">
            <PredictionResults result={result} />
            <button
              type="button"
              className="analysis-modal__again"
              onClick={onTryAgain}
            >
              다시 분석하기
            </button>
          </div>
        ) : (
          <>
            <PredictionForm
              isLoading={isLoading}
              onPredict={onPredict}
              onReset={onReset}
            />
            {error && (
              <p className="analysis-modal__error" role="alert">
                {error}
              </p>
            )}
          </>
        )}
      </div>
    </div>,
    document.body,
  );
}
