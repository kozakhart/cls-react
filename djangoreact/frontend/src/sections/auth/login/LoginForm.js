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
  const csrfUrl = process.env.REACT_APP_GET_CSRF_URL;
  const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
  const loginUrl = process.env.REACT_APP_LOGIN_URL;

  const getCsrfToken = async  () => {
    try {
      const res = await axios.get(csrfUrl, {
        withCredentials: true,
      });
    } catch (error) {
      console.log(error);
      console.log("Something went wrong");
    }
  };
  // useEffect(() => {

  // }, []);
  const handlelogin = async (e) => {
    e.preventDefault();
    try {
      const fetchCsrfToken = await getCsrfToken();
      const csrfToken = Cookies.get("x-csrftoken");

      const res = await axios.post(
        loginUrl,  
        {
          username,
          password,
        },
        { withCredentials: true,
        headers: {
          "X-CSRFToken": csrfToken,
        }, }
      );
      const tokenAuthentication = await axios.get(verifyTokenUrl, {
        withCredentials: true,
        headers: {
          "X-CSRFToken": csrfToken,
        },
      });
      if (tokenAuthentication.status === 200) {
        navigate('/cls/dashboard/app', { replace: true });
        console.log('hello dash')
      }

    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
    <form onSubmit={handlelogin}>
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
