import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
// @mui
import { Link, Stack, IconButton, InputAdornment, TextField, Checkbox } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import Cookies from 'js-cookie';
// components
import axios from 'axios';

import { set } from 'lodash';
import Iconify from '../../../components/iconify';
// ----------------------------------------------------------------------

export default function LoginForm({ formData, handleFormChange }) {
  const navigate = useNavigate();
  const { username, password } = formData;
  const [showPassword, setShowPassword] = useState(false);

  const loginUrl = process.env.REACT_APP_LOGIN_URL;

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i += 1) { // Fix for no-plusplus
        const cookie = cookies[i].trim();
        // Fix for prefer-template
        if (cookie.substring(0, name.length + 1) === `${name}=`) { 
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const handleLogin = async (event) => {
    event.preventDefault(); 
    const csrftoken = getCookie('csrftoken');
    try {
      const response = await fetch(loginUrl, { 
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log('Login successful:', data);
  
        navigate('/cls/dashboard/app', { replace: true });
        // Redirect or perform additional tasks
      } else {
        console.error('Login failed');
      }
    } catch (error) {
      console.error('An error occurred:', error);
    }
  };
  
  
  return (
    <>
    <form onSubmit={handleLogin}>
      <Stack spacing={3}>
      <TextField name="username" label="Username" value={formData.username} onChange={handleFormChange} />

      <TextField
        name="password"
        label="Password"
        type={showPassword ? 'text' : 'password'}
        value={formData.password}
        onChange={handleFormChange}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                <Iconify icon={showPassword ? 'eva:eye-fill' : 'eva:eye-off-fill'} />
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
      </Stack>

      <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ my: 2 }}>
        {/* <Checkbox
          name="remember"
          checked={formData.remember}
          onChange={handleFormChange}
        />
        <Link variant="subtitle2" underline="hover">
          Forgot password?
        </Link> */}
      </Stack>

      <LoadingButton fullWidth size="large" type="submit" variant="contained">
        Login
      </LoadingButton>
      </form>

    </>
  );
}
