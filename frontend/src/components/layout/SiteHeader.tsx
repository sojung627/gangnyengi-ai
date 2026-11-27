export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-header__inner">
        <a className="brand" href="#top" aria-label="강냉이 AI 홈">
          <span className="brand__mark" aria-hidden="true">
            <img src="/gangnaengi-favicon.png" alt="강냉이 이미지" />
          </span>
          <span>강냉이 AI</span>
        </a>
      </div>
    </header>
  );
}
