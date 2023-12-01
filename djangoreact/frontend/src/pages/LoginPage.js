// Import the necessary modules and components

import React, { useState } from 'react';
import axios from 'axios';
import { Helmet } from 'react-helmet-async';
import { styled } from '@mui/material/styles';
import { Link, Container, Typography, Divider, Stack, Button } from '@mui/material';
import useResponsive from '../hooks/useResponsive';
import Logo from '../components/logo';
import Iconify from '../components/iconify';
import { LoginForm } from '../sections/auth/login';

// ...
const StyledRoot = styled('div')(({ theme }) => ({
  [theme.breakpoints.up('md')]: {
    display: 'flex',
  },
}));

const DashboardBar = styled('div')({
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100%',
  height: '80px', // You can adjust the height as needed
  backgroundColor: '#002E5D',
  color: 'white', // Text color on the bar
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between', // Add space between the Logo and the right content
  padding: '0 16px', // Add some padding for space
});

const StyledSection = styled('div')(({ theme }) => ({
  width: '100%',
  maxWidth: 480,
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  boxShadow: theme.customShadows.card,
  backgroundColor: theme.palette.background.default,
}));

const StyledContent = styled('div')(({ theme }) => ({
  maxWidth: 480,
  margin: 'auto',
  minHeight: '100vh',
  display: 'flex',
  justifyContent: 'center',
  flexDirection: 'column',
  padding: theme.spacing(12, 0),
}));

export default function LoginPage() {
  const mdUp = useResponsive('up', 'md');
  const [formData, setFormData] = useState({ username: '', password: '' });

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  return (
    <>
      <Helmet>
        <title> Login | CLS Admin </title>
      </Helmet>

      <StyledRoot>
      <DashboardBar>
          <Logo sx={{  display: 'flex',
  alignItems: 'center'}}/>
        </DashboardBar>

        {mdUp && (
          <StyledSection>
            <Typography variant="h3" sx={{ px: 5, mt: 10, mb: 5 }}>
              Hi, Welcome Back
            </Typography>
          </StyledSection>
        )}

        <Container maxWidth="sm">
          <StyledContent>
            <Typography variant="h4" gutterBottom>
              Sign in to CLS Admin
            </Typography>

            {/* <Typography variant="body2" sx={{ mb: 5 }}>
              Don’t have an account? {''}
              <Link variant="subtitle2">Get started</Link>
            </Typography> */}

            {/* <Stack direction="row" spacing={2}>
              <Button fullWidth size="large" color="inherit" variant="outlined">
                <Iconify icon="eva:google-fill" color="#DF3E30" width={22} height={22} />
              </Button>

              <Button fullWidth size="large" color="inherit" variant="outlined">
                <Iconify icon="eva:facebook-fill" color= "#1877F2" width={22} height={22} />
              </Button>

              <Button fullWidth size="large" color="inherit" variant="outlined">
                <Iconify icon="eva:twitter-fill" color= "#1C9CEA" width={22} height={22} />
              </Button>
            </Stack> */}

            {/* <Divider sx={{ my: 3 }}>
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                OR
              </Typography>
            </Divider> */}

            {/* Render the Login component with the form fields */}
            <LoginForm
            formData={formData}
            handleFormChange={handleFormChange}
            />
          </StyledContent>
        </Container>
      </StyledRoot>
    </>
  );
}
