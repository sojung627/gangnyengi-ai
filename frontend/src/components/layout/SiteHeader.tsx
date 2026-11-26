import { Activity, Github, HeartPulse } from "lucide-react";

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-header__inner">
        <a className="brand" href="#top" aria-label="GangNaengI AI 홈">
          <span className="brand__mark" aria-hidden="true"><HeartPulse size={23} strokeWidth={2.2} /></span>
          <span>GangNaengI <strong>AI</strong></span>
        </a>
        <nav className="site-nav" aria-label="주요 메뉴">
          <a href="#analysis"><Activity size={16} aria-hidden="true" /> 예측 분석</a>
          <a href="https://github.com/sojung627/gangnyengi-ai" target="_blank" rel="noopener noreferrer">
            <Github size={17} aria-hidden="true" /> GitHub
          </a>
        </nav>
      </div>
    </header>
  );
}
