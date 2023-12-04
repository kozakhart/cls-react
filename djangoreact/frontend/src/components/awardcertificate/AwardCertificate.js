import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from '@mui/material';
import { set } from 'lodash';
import Iconify from '../iconify';

export default function UpdateNotification({netid}) {
  const [isConfirmationOpen, setConfirmationOpen] = useState(false);
  const [netidValue, setNetIDValue] = useState('');
  const [updateData, setUpdateData] = useState(false);

  const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
  const awardCertificateUrl = process.env.REACT_APP_AWARD_CERTIFICATE_URL;

  const handleCheckData = () => {
    // Set the flag to update data
    setUpdateData(true);
    setConfirmationOpen(true);
  };

  const handleConfirmationClose = () => {
    setConfirmationOpen(false);
  };

  useEffect(() => {
    if (updateData) {
      handleGetAllData(netid);
      setUpdateData(false); // Reset the flag
    }
  }, [updateData, netid]);

  const handleGetAllData = (netid) => {
    const netidElement = document.getElementById(netid);
    
    const netidValue = netidElement.value;

    setNetIDValue(netidValue);
  };
  const navigate = useNavigate();
    
  const handleAwardCertificate = async () => {
    const dataToSend = {
      NetID: netidValue,
      // Other data to send
    };
    
    try {
      const csrfToken = Cookies.get('csrftoken');
      
      const verifyTokenResponse = await axios.get(verifyTokenUrl, {
        withCredentials: true,
        headers: {
          "X-CSRFToken": csrfToken,
        },
      });
  
      if (verifyTokenResponse.status === 200) {
        try {
          const awardCertificateResponse = await axios.post(
            awardCertificateUrl,
            { dataToSend },
            {
              withCredentials: true,
              headers: {
                'X-CSRFToken': csrfToken,
              },
            }
          );
  
          // Handle the awardCertificateResponse as needed
          console.log(awardCertificateResponse.data);
        } catch (error) {
          console.error('Error in awarding certificate:', error);
        }
      }
    } catch (error) {
      console.error('Error verifying token:', error);
    }
  };
  

  return (
    <Container style={{padding:'0'}}>
      <div style={{ display: 'flex', justifyContent: 'left'}}>
        <MenuItem
        onClick={() => {
          handleCheckData();
          handleGetAllData(netid);
        }}
        style={{fontWeight: 'bold' }}>
        <Iconify icon={'eva:email-outline'} sx={{ mr: 2 }}/>
          Award Certificate
        </MenuItem>
      </div>

      <Dialog open={isConfirmationOpen} onClose={handleConfirmationClose}>
        <DialogTitle>Confirmation</DialogTitle>
        <DialogContent>
          Are you sure you want to send this certificate to {netidValue}@byu.edu?
        </DialogContent>
        <DialogActions>
        <Button onClick={() => {
            handleGetAllData(netid);
            handleAwardCertificate();
          }} color="primary"> Yes
          </Button>
          <Button onClick={handleConfirmationClose} color="primary">
            No
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
