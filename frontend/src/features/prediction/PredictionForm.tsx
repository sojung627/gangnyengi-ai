import { zodResolver } from "@hookform/resolvers/zod"; // zodResolver = Zod 유효성검증스키마를 React Hook Form과 연결
                                                       // @hookform/resolvers/zod = zodResolver의 라이브러리 모듈
import { useForm } from "react-hook-form"; // useForm = 입력폼 데이터 + 유효성 검증 상태 관리하는 React Hook
// 입력폼 관련 데이터 및 자료형 가져오기
import {
  emptyPredictionForm,  // emptyPredictionForm  = 입력폼 초기값을 저장한 객체
  predictionFormSchema, // predictionFormSchema = 입력폼 유효성 검증 스키마
  type PredictionFormValues, // type = tsx의 자료형을 가져와라
                             // PredictionFormValues = 입력폼데이터의 자료형
} from "./prediction.schema"; // prediction.schema.ts 불러와라

// 컴포넌트 Props 인터페이스 정의 
interface PredictionFormProps { // interface = 인터페이스
                                // PredictionFormProps = 컴포넌트가 전달받을 Props의 자료형
  isLoading: boolean; // isLoading = 현재예측작업의 진행 여부
  onPredict: (values: PredictionFormValues) => Promise<void>; // onPredict = 치주질환 예측 실행함수를 전달 받아라
                                                              // values = 입력폼 데이터 전달받는 변수
                                                              // PredictionFormValues = 입력폼 데이터 자료형
                                                              // Promise = 비동기 작업 완료 or 실패 
                                                              // <void>  = 비동기 성공해도 반환값 없음
  onReset: () => void; // onReset = 초기화 함수를 전달받는 속성
}                      // () = 전달받을 매개변수 x
                       // void  = 비동기 성공해도 반환값 없음

// PredictionForm 컴포넌트 선언                       
export function PredictionForm({ // export   = 외부에서 받아오라
                                 // function = 함수
  isLoading, // isLoading = 분석 작업의 진행 여부
  onPredict, // onPredict = 치주질환 예측 실행 함수
  onReset,   // onReset = 초기화 함수
}: PredictionFormProps) { // PredictionFormProps = 전달받는 Props의 자료형
  const { // const = 상수
    register,     // register = HTML 입력요소를 React Hook에 등록시킴
    handleSubmit, // handleSubmit = 입력폼 제출 및 유효성 검증 처리
    reset,    // reset = 입력폼 + 입력값 + 폼 상태를 초기화
    formState: { errors }, // formState  = 입력폼 상태 정보 저장
                           // { errors } = 입력폼 에러 정보 저장
  } = useForm<PredictionFormValues>({ // useForm = 입력폼 데이터 및 상태 관리하는 React Hook
                                      // <PredictionFormValues> = 입력폼에 관리할 데이터
    resolver: zodResolver(predictionFormSchema), // resolver = 입력폼에 적용할 외부유효성검증 기능 지정
                                                 // zodResolver = zod를 React Hook Form과 연결
                                                 // predictionFormSchema = 입력폼 유효성 검증 스키마
    defaultValues: emptyPredictionForm, // defaultValues = 입력폼 초기값 지정
                                        // emptyPredictionForm = 입력폼 초기값을 저장
    mode: "onSubmit", // mode = 입력폼의 최초 유효성검증 실행 시점을 지정
  });                 // onSubmit = 입력폼 제출 시 유효성검증 실행 
  
  // // 흡연 경험 입력값 변경시 감지  
  // const everSmoked = watch("everSmoked"); // const = 상수
  //                                         // everSmoked = 현재 흡연 경험 입력값 저장
  //                                         // watch() = 입력폼의 특정입력값을 구독 + 확인
  //                                         // "everSmoked" = 구독할 입력폼 필드명
  // // 흡연경험에 따른 입력값 자동 변경                                        
  // useEffect(() => { // useEffect() = 컴포넌트 렌더링 이후 특정 작업 실행하는 React Hook
  //                   // () = 매개변수가 x 
  //   // 100개비 이상 흡연 x == 흡연 x 
  //   if (everSmoked === "2") { 
  //     setValue("smokingFrequency", "3"); // setValue() = 입력폼의 특정 필드값을 변경
  //   } else {
  //     setValue("smokingFrequency", ""); // "" = 초기화
  //   }
  // }, [everSmoked, setValue]); // 의존성 배열

  // 입력폼 초기화
  function clearForm() { // function = 함수 
    reset(emptyPredictionForm); // reset = 입력값 초기화
                                // emptyPredictionForm = 입력폼 초기값 
    onReset(); // onReset() = 부모 컴포넌트에게 받은것들 초기화
  }

  return (
    <form
      className="analysis-form"
      onSubmit={handleSubmit(onPredict)}
      noValidate
    >
      <div className="analysis-form__grid">
        <div className="analysis-field">
          <label htmlFor="age">
            나이
          </label>
          <input
            id="age"
            type="number"
            min="30"
            max="80"
            step="1"
            placeholder="나이를 입력하세요"
            autoComplete="off"
            aria-invalid={Boolean(errors.age)}
            aria-describedby={errors.age ? "age-error" : undefined}
            {...register("age")}
          />
          {errors.age && (
            <p id="age-error" className="analysis-field__error" role="alert">
              {errors.age.message}
            </p>
          )}
        </div>
        <div className="analysis-field">
          <label htmlFor="gender">
            성별
          </label>
          <select
            id="gender"
            aria-invalid={Boolean(errors.gender)}
            aria-describedby={errors.gender ? "gender-error" : undefined}
            {...register("gender")}
          >
            <option value="">선택해 주세요</option>
            <option value="1">남성</option>
            <option value="2">여성</option>
          </select>
          {errors.gender && (
            <p id="gender-error" className="analysis-field__error" role="alert">
              {errors.gender.message}
            </p>
          )}
        </div>
        <div className="analysis-field analysis-field--wide">
          <label htmlFor="everSmoked">
            흡연 여부
          </label>
          <select
            id="everSmoked"
            aria-invalid={Boolean(errors.everSmoked)}
            aria-describedby={
              errors.everSmoked ? "everSmoked-error" : "smoking-help"
            }
            {...register("everSmoked")}
          >
            <option value="">선택해 주세요</option>
            <option value="2">평생 100개비 이상 흡연 경험 없음</option>
            <option value="1">평생 100개비 이상 흡연 경험 있음</option>
          </select>
          <p id="smoking-help" className="analysis-field__hint">
            NHANES 기준: 평생 100개비 이상 흡연 경험
          </p>
          {errors.everSmoked && (
            <p
              id="everSmoked-error"
              className="analysis-field__error"
              role="alert"
            >
              {errors.everSmoked.message}
            </p>
          )}
        </div>
        <div className="analysis-field analysis-field--wide">
          <label htmlFor="smokingFrequency">
            현재 흡연
            상태
          </label>
          <select
            id="smokingFrequency"
            aria-invalid={Boolean(errors.smokingFrequency)}
            aria-describedby={
              errors.smokingFrequency ? "smokingFrequency-error" : undefined
            }
            {...register("smokingFrequency")}
          >
            
              <>
                <option value="">선택해 주세요</option>
                <option value="1">매일 흡연</option>
                <option value="2">가끔 흡연</option>
              </>
            
            <option value="3">현재 흡연하지 않음</option>
          </select>
          {errors.smokingFrequency && (
            <p
              id="smokingFrequency-error"
              className="analysis-field__error"
              role="alert"
            >
              {errors.smokingFrequency.message}
            </p>
          )}
        </div>
      </div>
      <p className="analysis-form__disclosure">
        현재 모델은 나이 성별 흡연 정보로 예측합니다.
      </p>
      <button
        type="submit"
        className="analysis-form__submit"
        disabled={isLoading}
        aria-busy={isLoading}
      >
        <span>{isLoading ? "분석 중..." : "분석하기"}</span>
      </button>
      <button
        type="button"
        className="analysis-form__reset"
        onClick={clearForm}
        disabled={isLoading}
      >
        입력 초기화
      </button>
    </form>
  );
}
