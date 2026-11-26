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
    throw new Error("VITE_API_URL이 설정되지 않았어. frontend/.env.development를 확인해 줘.");
  }
}
