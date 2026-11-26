export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-header__inner">
        <a
          className="brand"
          href="#top"
          aria-label="GangNaengI AI 홈"
        >
          <span
            className="brand__mark"
            aria-hidden="true"
          >
            <i className="fa-solid fa-tooth"></i>
          </span>

          <span>
            GangNaengI <strong>AI</strong>
          </span>
        </a>

        <nav
          className="site-nav"
          aria-label="주요 메뉴"
        >
          <a href="#analysis">예측 분석</a>
        </nav>
      </div>
    </header>
  );
}
