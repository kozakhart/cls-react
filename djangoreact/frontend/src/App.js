import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
// routes
// import Router from './routes';
// theme
import ThemeProvider from './theme';
// components
import { StyledChart } from './components/chart';
import ScrollToTop from './components/scroll-to-top';
import DashboardLayout from './layouts/dashboard';
import LoginPage from './pages/LoginPage';
import GenerateReports from './pages/GenerateReports';
import DatabasePage from './pages/DatabasePage';
import Page404 from './pages/Page404';
import NeedsApprovalPage from './pages/NeedsApprovalPage';
import DashboardAppPage from './pages/DashboardAppPage';
import LanguageCertificatesPage from './pages/LanguageCertificatesPage';
import QualtricsReports from './pages/QualtricsReports';
import LASERdbPage from './pages/LASERdbPage';

export default function App() {
  return (
  //  <AuthProvider>
    <HelmetProvider>
      <BrowserRouter>
        <ThemeProvider>
          <ScrollToTop />
          <StyledChart />
          <Routes>
            <Route path="/cls" element={<DashboardLayout />}>
                <Route index element={<Navigate to="dashboard/app" replace />} />
                <Route path="dashboard/app" element={<DashboardAppPage />} />
                <Route path="dashboard/database" element={<DatabasePage />} />
                <Route path="dashboard/needs-approval" element={<NeedsApprovalPage />} />
                <Route path="dashboard/language-certificates" element={<LanguageCertificatesPage />} />
                <Route path="dashboard/qualtrics-reports" element={<QualtricsReports />} />
                <Route path="dashboard/laser-database" element={<LASERdbPage />} />
                {/* <Route path="dashboard/generate-reports" element={<GenerateReports />} /> */}
                <Route path="404" element={<Page404 />} />

                {/* Add more authenticated routes here */}
            </Route>
            <Route path="/cls/login" element={<LoginPage />} />
            <Route path="/" element={<Navigate to="/cls/login" replace />} />
            {/* Define other routes here */}
            <Route path="*" element={<Navigate to="/cls/404" replace />} />
        </Routes>
        </ThemeProvider>
      </BrowserRouter>
    </HelmetProvider>
  //  </AuthProvider>
  );
}