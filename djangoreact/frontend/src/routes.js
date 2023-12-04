import { Navigate, Route, Outlet, useRoutes, useNavigate } from 'react-router-dom';
// layouts
import Cookies from 'js-cookie'; // Import the js-cookie library
import { useEffect, useState } from 'react';
import axios from 'axios';
import DashboardLayout from './layouts/dashboard';
import SimpleLayout from './layouts/simple';

import GenerateReports from './pages/GenerateReports';
import UserPage from './pages/UserPage';
import LoginPage from './pages/LoginPage';
import Page404 from './pages/Page404';
import NeedsApprovalPagePage from './pages/NeedsApprovalPage';
import DashboardAppPage from './pages/DashboardAppPage';
import LanguageCertificatesPage from './pages/LanguageCertificatesPage';


// ----------------------------------------------------------------------

function ProtectedRoute({ element, auth, ...rest }) {
  return (
    <Route
      {...rest}
      element={auth ? element : <Navigate to="/login" replace />}
    />
  );
}

export default function Router() {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const csrfUrl = process.env.REACT_APP_GET_CSRF_URL;
  const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
  
  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const csrfToken = Cookies.get('csrftoken');
        const response = await axios.get(csrfUrl, {
         withCredentials: true,
          headers: {
            "X-CSRFToken": csrfToken,
          }, 
      });
        if (response.status === 200) {
          const tokenAuthentication = await axios.get(verifyTokenUrl, {
            withCredentials: true,
            headers: {
              "X-CSRFToken": csrfToken,
            },
          });
          if (tokenAuthentication.status === 200) {
            setIsAuthenticated(true);
            navigate('/dashboard/app', { replace: true });
            console.log('hello')
          }
        }
      } catch (error) {
        setIsAuthenticated(false);
        navigate('/login', { replace: true });
        console.error(error);
      }
    };

    checkAuthentication();
  }, []);
  
  const routes = useRoutes([
    {
      path: '/dashboard',
      element: isAuthenticated ? <DashboardLayout /> : <Navigate to="/login" />,
      children: [
        { element: <Navigate to="/dashboard/app" />, index: true },
        { path: 'app', element: <DashboardAppPage /> },
        { path: 'user', element: <UserPage /> },
        { path: 'needs-approval', element: <NeedsApprovalPagePage /> },
        { path: 'language-certificates', element: <LanguageCertificatesPage /> },
        { path: 'reports', element: <GenerateReports /> },
      ],
    },
    {
      path: 'login',
      element: <LoginPage />,
    },
    {
      element: <SimpleLayout />,
      children: [
        { element: <Navigate to="/dashboard/app" />, index: true },
        { path: '404', element: <Page404 /> },
        { path: '*', element: <Navigate to="/404" /> },
      ],
    },
    {
      path: '*',
      element: <Navigate to="/404" replace />,
    },
  ]);

  return routes;
}




