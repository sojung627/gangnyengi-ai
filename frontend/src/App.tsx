import { SiteHeader } from "./components/layout/SiteHeader";
import { SiteFooter } from "./components/layout/SiteFooter";
import { PredictionPage } from "./pages/PredictionPage";
import "./App.css";

export default function App() {
  return (
    <div className="app-shell">
      <SiteHeader />
      <PredictionPage />
      <SiteFooter />
    </div>
  );
}
