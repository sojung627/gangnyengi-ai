export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-header__inner">
        <a className="brand" href="#top" aria-label="강냉이 AI 홈">
          <span className="brand__mark" aria-hidden="true">
            <i className="fa-solid fa-tooth" />
          </span>
          <span>강냉이 AI</span>
        </a>
      </div>
    </header>
  );
}
