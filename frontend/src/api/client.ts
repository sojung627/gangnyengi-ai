import axios from "axios";

// 환경별 API 주소는 frontend/.env.development 또는 배포 환경변수에서 관리한다.
const apiBaseUrl = import.meta.env.VITE_API_URL?.trim();

export const apiClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 15000,
  headers: { "Content-Type": "application/json" },
});

export function assertApiConfigured(): void {
  if (!apiBaseUrl) {
    // 개발자용 오류 로그
    console.error("VITE_API_URL이 설정되지 않았습니다.");
    // 웹에 보일 오류
    throw new Error("서비스 연결에 문제가 발생했습니다. 잠시 후 다시 시도해 주세요.");
  }
}
