import PropTypes from 'prop-types';
// @mui
import { styled, alpha } from '@mui/material/styles';
import { useEffect, useState } from 'react';
import axios, { Axios } from 'axios';
import Cookies from 'js-cookie';
import { set } from 'lodash';
import { Toolbar, Tooltip, IconButton, Typography, OutlinedInput, InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
 } from '@mui/material';
// component
import { is } from 'date-fns/locale';

import Iconify from '../../../components/iconify';

// ----------------------------------------------------------------------
const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
const editUrl = process.env.REACT_APP_EDIT_RECORD_URL;
const StyledRoot = styled(Toolbar)(({ theme }) => ({
  height: 96,
  display: 'flex',
  justifyContent: 'space-between',
  padding: theme.spacing(0, 1, 0, 3),
}));

const StyledSearch = styled(OutlinedInput)(({ theme }) => ({
  width: 240,
  transition: theme.transitions.create(['box-shadow', 'width'], {
    easing: theme.transitions.easing.easeInOut,
    duration: theme.transitions.duration.shorter,
  }),
  '&.Mui-focused': {
    width: 320,
    boxShadow: theme.customShadows.z8,
  },
  '& fieldset': {
    borderWidth: `1px !important`,
    borderColor: `${alpha(theme.palette.grey[500], 0.32)} !important`,
  },
}));

// ----------------------------------------------------------------------

UserListToolbar.propTypes = {
  numSelected: PropTypes.number,
  filterName: PropTypes.string,
  onFilterName: PropTypes.func,
};


async function handleEdit(recordIds) {
  console.log(recordIds);
  recordIds.forEach(async (recordId) => {
    console.log(recordId);
  });
   
  try {
    const csrfToken = Cookies.get('csrftoken');
    const verifyResponse = await axios.get(verifyTokenUrl, {
      withCredentials: true,
      headers: {
        "X-CSRFToken": csrfToken,
      },
    });
    console.log(verifyResponse);

    if (verifyResponse.status === 200) {
      try {
        const editResponse = await axios.post(editUrl, {
          recordids: recordIds,
        }, {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrfToken,
          },
        });

        if (editResponse.status === 200) {
          console.log('Success');
        }
      } catch (error) {
        console.log(error, '1');
      }
    }
  } catch (error) {
    console.log(error, '2');
  }
}

export default function UserListToolbar({ numSelected, filterName, onFilterName, recordIds }) {
  const [isConfirmationOpen, setConfirmationOpen] = useState(false);
  const [isConfirmationOpen2, setConfirmationOpen2] = useState(false);

  const handleClick = () => {
    setConfirmationOpen(true);
  };

  const handleConfirmationClose = () => {
    setConfirmationOpen(false);
  };

  const handleConfirmationOpen2 = () => {
    setConfirmationOpen2(true);
  };
  const handleConfirmationClose2 = () => {
    setConfirmationOpen2(false);
  };

  return (
    <StyledRoot
      sx={{
        ...(numSelected > 0 && {
          color: 'primary.main',
          bgcolor: 'primary.lighter',
        }),
      }}
    >
      {numSelected > 0 ? (
          <Typography component="div" variant="subtitle1">
          <StyledSearch
          sx={{ marginRight: 5}}
            value={filterName}
            onChange={onFilterName}
            placeholder="Filter students..."
            startAdornment={
              <InputAdornment position="start">
                <Iconify icon="eva:search-fill" sx={{ color: 'text.disabled', width: 20, height: 20 }} />
              </InputAdornment>
            }
          />
        </Typography>
      ) : (
        <StyledSearch
          value={filterName}
          onChange={onFilterName}
          placeholder="Filter students..."
          startAdornment={
            <InputAdornment position="start">
              <Iconify icon="eva:search-fill" sx={{ color: 'text.disabled', width: 20, height: 20 }} />
            </InputAdornment>
          }
        />
      )}
      {numSelected > 0 ? (
      <Tooltip title="Approve Selected">

               <IconButton onClick={() => handleClick(recordIds)}>
                <Typography >
               {numSelected} selected
                </Typography>
                <Iconify icon="eva:checkmark-circle-outline" sx={{ color: 'green' }} />
                <Dialog open={isConfirmationOpen}>
                  <DialogTitle>Confirmation</DialogTitle>
                  <DialogContent>
                    Are you sure you want to approved the selected ({numSelected}) students?
                  </DialogContent>
                  <DialogActions>
                  <Button
                    onClick={(e) => {
                      handleEdit(recordIds);
                      handleConfirmationClose();
                      handleConfirmationOpen2();
                      e.stopPropagation();
                    }}>
                      Yes
                    </Button>
                    <Button onClick={(e) => {
                      handleConfirmationClose();
                      e.stopPropagation();
                    }}>
                      No
                    </Button>
                  </DialogActions>
                </Dialog>
                <Dialog open={isConfirmationOpen2}>
                  <DialogTitle>Confirmation</DialogTitle>
                  <DialogContent>
                    Successfully updated!
                  </DialogContent>
                  <DialogActions>
                  <Button
                    onClick={(e) => {
                      handleConfirmationClose2();
                      e.stopPropagation();
                    }}>
                      Okay
                    </Button>
                  </DialogActions>
                </Dialog>
              </IconButton>
        </Tooltip>
        
      ) : (
        null
      )}
      {/* {numSelected > 0 ? (
        <Tooltip title="Approve Selected">
          <IconButton onClick={handleClick}>
            <Iconify icon="eva:checkmark-circle-outline" sx={{ color: 'green' }}/>
          </IconButton>
        </Tooltip>
      ) : (
        <Tooltip title="Filter list">
          <IconButton>
            <Iconify icon="ic:round-filter-list" />
          </IconButton>
        </Tooltip>
      )} */}
    </StyledRoot>
  );
}
