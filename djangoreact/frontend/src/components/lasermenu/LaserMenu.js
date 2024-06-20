import * as React from 'react';
import Button from '@mui/material/Button';
import MenuList from '@mui/material/MenuList';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import Typography from '@mui/material/Typography';
import { useEffect, useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';

import Iconify from '../iconify';





export default function BasicMenu({ sendQuery, createQuery }) {

    const [queryData, setQueryData] = React.useState([]);
    const verifySessionUrl = process.env.REACT_APP_VERIFY_SESSION_URL;
    const getQueryUrl = process.env.REACT_APP_GET_QUERY_URL;
    const navigate = useNavigate(); 

    const handleButtonClick = (query) => {
      sendQuery(query);
    };
    const handleQuery = () => {
      createQuery(true);
    };

    const retrieveQueryData = async () => {
        try {
          const response = await axios.get(getQueryUrl, {
            withCredentials: true,
          });
    
          if (response.status === 200) {
            setQueryData(response.data);
            console.log('Query data retrieved:', response.data);
          } else {
            console.error('Failed to retrieve query data');
          }
        } catch (error) {
          console.error('Failed to retrieve query data:', error);
        }
      };



    useEffect(() => {
        const fetchSessionData = async () => {
          try {
            const response = await axios.get(verifySessionUrl, {
              withCredentials: true,
            });
      
            if (response.status === 200) {
              console.log('Session is active');
              await retrieveQueryData();
            } else {
              console.log('Session is not active');
              navigate('/cls/login', { replace: true });
            }
          } catch (error) {
            console.error('Failed to verify session:', error);
            navigate('/cls/login', { replace: true });
          }
        };
      
        fetchSessionData();
        
      }, [navigate]); 

  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };


  return (
    <div>
      <Button
        id="basic-button"
        aria-controls={open ? 'basic-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        onClick={handleClick}
        color="primary"
        variant="contained"
      >
        My Queries
      </Button>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
      >
        <MenuItem onClick={handleQuery}>
        <Iconify icon={'eva:plus-circle-outline'} sx={{ mr: 1 }}/>
          <ListItemText>Add New Query</ListItemText>
        </MenuItem>

        {queryData.map((query) => (
            <MenuItem key={query.id}
            onClick={() => handleButtonClick(query.query)}
            >
                {query.query_label}
            </MenuItem>
        ))}

      </Menu>
    </div>
  
);

}
