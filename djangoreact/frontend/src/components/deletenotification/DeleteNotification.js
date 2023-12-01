import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import {
  Container,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from '@mui/material';
import Iconify from '../iconify';

export default function DeleteNotification({recordId}) {
  const [isConfirmationOpen, setConfirmationOpen] = useState(false);

  const handleCheckData = () => {
    setConfirmationOpen(true);
  };

  const handleConfirmationClose = () => {
    setConfirmationOpen(false);
  };

  const handleUpdateData = () => {
    const csrfToken = Cookies.get("csrftoken");

    axios
      .post(`http://localhost:8000/api/delete/${recordId}/`, recordId, {
        withCredentials: true,
        headers: {
          "X-CSRFToken": csrfToken,
        },
      }
      )
      .then((response) => {
        console.log('Data updated successfully:', response);
        setConfirmationOpen(false);
      })
      .catch((error) => {
        console.error('Error updating data:', error);
      });
  };

  return (
    <Container style={{padding:'0'}}>
      <div style={{ display: 'flex', justifyContent: 'left'}}>
        <MenuItem onClick={handleCheckData} style={{fontWeight: 'bold', color: 'red'}}>
          <Iconify icon={'eva:trash-2-outline'} sx={{ mr: 1}} />
          Delete
        </MenuItem>
      </div>

      <Dialog open={isConfirmationOpen} onClose={handleConfirmationClose}>
        <DialogTitle>Confirmation</DialogTitle>
        <DialogContent>
          Are you sure you want to delete this entry?
        </DialogContent>
        <DialogActions>
          <Button onClick={handleUpdateData} color="primary">
            Yes
          </Button>
          <Button onClick={handleConfirmationClose} color="primary">
            No
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
