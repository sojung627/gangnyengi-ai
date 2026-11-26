export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="site-footer__inner">
        <p>© {new Date().getFullYear()} GangNaengI AI · Periodontal Research</p>
        <p>NHANES 2013–2014 기반 연구용 분류 데모 · 의료 진단 도구가 아닙니다.</p>
      </div>
    </footer>
  );
}
