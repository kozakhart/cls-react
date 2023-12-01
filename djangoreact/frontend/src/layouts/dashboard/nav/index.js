import PropTypes from 'prop-types';
import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie'; // Import the js-cookie library
// @mui
import { styled, alpha } from '@mui/material/styles';
import { Box, Link, Button, Drawer, Typography, Avatar, Stack, useMediaQuery } from '@mui/material';
// mock
import account from '../../../_mock/account';
// hooks
import useResponsive from '../../../hooks/useResponsive';
// components
import Logo from '../../../components/logo';
import Scrollbar from '../../../components/scrollbar';
import NavSection from '../../../components/nav-section';
//
import navConfig from './config';

// ----------------------------------------------------------------------
const NAV_WIDTH = 280;

const StyledAccount = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(2, 2.5),
  borderRadius: Number(theme.shape.borderRadius) * 1.5,
  backgroundColor: alpha(theme.palette.grey[500], 0.12),
}));

// ----------------------------------------------------------------------

Nav.propTypes = {
  openNav: PropTypes.bool,
  onCloseNav: PropTypes.func,
};
// await 

export default function Nav({ openNav, onCloseNav }) {
  const { pathname } = useLocation();
  const [username, setUsername] = useState('');
  const [groups, setGroups] = useState('');

  const isDesktop = useResponsive('up', 'lg');
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
  
    if (openNav) {
      onCloseNav();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname, openNav]);
  const renderContent = (
    <Scrollbar
      sx={{
        height: 1,
        '& .simplebar-content': { height: 1, display: 'flex', flexDirection: 'column',},
      }}
    >
      <Box
        sx={{
          px: 2.5,
          py: 3.25,
          display: 'flex',
          backgroundColor: '#002E5D',
          width: '100%',
          
        }}
      >
          <Logo sx={{ paddingTop: '10px'}}/>
          {/* <Typography
          variant="h6"
          sx={{
            color: 'white', // Set the text color
            zIndex: '1 !important', // Make sure it's above other content
          }}
        >
          Need More Features?
        </Typography> */}
      </Box>

      <Box sx={{ mb: 5, mx: 2.5, }}>
        <Link underline="none">
          <StyledAccount>
            <Avatar src={account.photoURL} alt="photoURL" />

            <Box sx={{ ml: 2 }}>
              <Typography variant="subtitle2" sx={{ color: 'text.primary' }}>
                {username}
              </Typography>

              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                {groups}
              </Typography>
            </Box>
          </StyledAccount>
        </Link>
      </Box>

      <NavSection data={navConfig} />

      {/* <Box sx={{ px: 2.5, pb: 3, mt: 10 }}> */}
        <Stack alignItems="center" spacing={3} sx={{ pt: 5, borderRadius: 2, position: 'relative' }}>

          <Box sx={{ textAlign: 'center' }}>
            <Typography gutterBottom variant="h6">
              Need More Features?
            </Typography>

            {/* <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Click Here
            </Typography> */}
          </Box>

          <Button href="http://localhost:8000/admin/" target="_blank" variant="contained">
            Admin Backend
          </Button>
        </Stack>
      {/* </Box> */}
    </Scrollbar>
  );
  

  return (
    <Box
      component="nav"
      sx={{
        flexShrink: { lg: 0 },
        width: { lg: NAV_WIDTH },
      }}
    >
      {isDesktop ? (
        <Drawer
          open
          variant="permanent"
          PaperProps={{
            sx: {
              width: NAV_WIDTH + 10,
              border: '0px',
              bgcolor: 'background.default',

            },
          }}
        >
          {renderContent}
        </Drawer>
      ) : (
        <Drawer
          open={openNav}
          onClose={onCloseNav}
          ModalProps={{
            keepMounted: true,
          }}
          PaperProps={{
            sx: { width: NAV_WIDTH },
          }}
        >
          {renderContent}
        </Drawer>
      )}
    </Box>
  );
}
