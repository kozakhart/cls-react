import { useState, useEffect, useLocation } from 'react';
// @mui
import { alpha } from '@mui/material/styles';
import { Box, Divider, Typography, Stack, MenuItem, Avatar, IconButton, Popover } from '@mui/material';
// mocks_
import axios from 'axios';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import account from '../../../_mock/account';

// ----------------------------------------------------------------------

const MENU_OPTIONS = [
  {
    label: 'Home',
    icon: 'eva:home-fill',
  },
  {
    label: 'Profile',
    icon: 'eva:person-fill',
  },
  {
    label: 'Settings',
    icon: 'eva:settings-2-fill',
  },
];

// ----------------------------------------------------------------------

export default function AccountPopover() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(null);

    const [username, setUsername] = useState('');
    const [groups, setGroups] = useState('');
  
    useEffect(() => {
      const fetchData = async () => {
        const csrfToken = Cookies.get('csrftoken');
        try {
          const response = await axios.get("http://localhost:8000/api/get-user-info/", {
            withCredentials: true,
            headers: {
              "X-CSRFToken": csrfToken,
            },
          });
          console.log(response);
          if (response.status === 200) {
            setUsername(response.data.user.username);
            setGroups(response.data.groups);
          }
        } catch (error) {
          // Handle errors, e.g., display an error message or take appropriate action
          console.error(error);
        }
      };
    
      // Fetch user information whenever the route changes
      fetchData();
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
  const handleOpen = (event) => {
    setOpen(event.currentTarget);
  };

  const handleClose = () => {
    setOpen(null);
  };

  const handleLogout = async () => {
    const csrfToken = Cookies.get("csrftoken");
    console.log(csrfToken);
    try {
      await axios.post('http://localhost:8000/api/logout/', null, {
        withCredentials: true, // Ensure cookies are sent with the request
        headers: {
          'X-CSRFToken': csrfToken,
        }, // Rename the CSRF cookie to match the Django expected default
      });
      navigate('/login', { replace: true });
      // You can add additional logic to handle the successful logout, such as redirecting the user to the login page.
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <>
      <IconButton
        onClick={handleOpen}
        style={{ backgroundColor: '#002E5D', color: '#002E5D' }}
        sx={{
          p: 0,
          ...(open && {
            '&:before': {
              zIndex: 1,
              content: "''",
              width: '100%',
              height: '100%',
              borderRadius: '50%',
              position: 'absolute',
              bgcolor: (theme) => alpha(theme.palette.grey[900], 0.8),
            },
          }),
        }}
      >
        <Avatar src={account.photoURL} alt="photoURL" />
      </IconButton>

      <Popover
        open={Boolean(open)}
        anchorEl={open}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: {
            p: 0,
            mt: 1.5,
            ml: 0.75,
            width: 180,
            '& .MuiMenuItem-root': {
              typography: 'body2',
              borderRadius: 0.75,
            },
          },
        }}
      >
        <Box sx={{ my: 1.5, px: 2.5 }}>
          <Typography variant="subtitle2" noWrap>
            {username}
          </Typography>
          <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
            {groups}
          </Typography>
        </Box>

        <Divider sx={{ borderStyle: 'dashed' }} />

        <Stack sx={{ p: 1 }}>
          {MENU_OPTIONS.map((option) => (
            <MenuItem key={option.label} onClick={handleClose}>
              {option.label}
            </MenuItem>
          ))}
        </Stack>

        <Divider sx={{ borderStyle: 'dashed' }} />

        <MenuItem onClick={handleLogout} sx={{ m: 1 }}>
          Logout
        </MenuItem>
      </Popover>
    </>
  );
}
