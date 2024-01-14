import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import PulseLoader from "react-spinners/PulseLoader";

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
import { useNavigate } from 'react-router-dom';
import Iconify from '../iconify';

export default function UpdateNotification({ fullName, byuid, netid, language, level, opiScore, wptScore, todaysDate, recordId, certificateType, closeFirstPopover} ) {
  const [isConfirmationOpen, setConfirmationOpen] = useState(false);
  const [fullNameValue, setFullName] = useState('');
  const [byuidValue, setBYUIDValue] = useState(byuid);
  const [netidValue, setNetIDValue] = useState('');
  const [languageValue, setLanguage] = useState('');
  const [levelValue, setLevel] = useState('');
  const [opiScoreValue, setOpiScore] = useState('');
  const [wptScoreValue, setWptScore] = useState('');
  const [todaysDateValue, setTodaysDate] = useState('');
  const [recordIdValue, setrecordId] = useState(recordId);
  const [certificateTypeValue, setCertificateType] = useState(false);
  const [loading, setLoading] = useState(false);

  const [updateData, setUpdateData] = useState(false);
  const [awardedConfirmation, setAwardedConfirmation] = useState(false);

  const navigate = useNavigate();
  const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
  const awardCertificateUrl = process.env.REACT_APP_AWARD_CERTIFICATE_URL;

  const handleCheckData = () => {
    // Set the flag to update data
    setLoading(true);
    setUpdateData(true);
    setConfirmationOpen(true);
  };

  const handleConfirmationClose = () => {
    setConfirmationOpen(false);
    setLoading(false);
  };

  const handleAwardedConfirmation = () => {
    setAwardedConfirmation(true);
  }
  const handleAwardedConfirmationClose = () => {
    setAwardedConfirmation(false);
    closeFirstPopover();
    navigate('/cls/dashboard/language-certificates', { replace: true });

  }
  useEffect(() => {
    if (updateData) {
      handleGetAllData(netid);
      setUpdateData(false); // Reset the flag
    }
  }, [updateData, netid]);

  const handleGetAllData = (netid) => {
    const netidElement = document.getElementById(netid);
    const byuidElement = document.getElementById(byuid);
    const fullNameElement = document.getElementById(fullName);
    const languageElement = document.getElementById(language);
    const levelElement = document.getElementById(level);
    const opiScoreElement = document.getElementById(opiScore);
    const wptScoreElement = document.getElementById(wptScore);
    const todaysDateElement = document.getElementById(todaysDate);
    const certificateTypeElement = document.getElementById(certificateType);

    const fullNameValue = fullNameElement.value;
    const netidValue = netidElement.value;
    try{
      const byuidValue = byuidElement.value;
      setBYUIDValue(byuidValue);
    }
    catch{
      console.log("No BYUID");
    }

    const languageValue = languageElement.value;
    const levelValue = levelElement.value;
    const opiScoreValue = opiScoreElement.value;
    const wptScoreValue = wptScoreElement.value;
    const todaysDateValue = todaysDateElement.value;
    try{
      const certificateTypeValue = certificateTypeElement.checked;
      setCertificateType(certificateTypeValue);
    }
    catch{
      console.log("No certificate type");
    }


    setFullName(fullNameValue);
    setNetIDValue(netidValue);
    setLanguage(languageValue);
    setLevel(levelValue);
    setOpiScore(opiScoreValue);
    setWptScore(wptScoreValue);
    setTodaysDate(todaysDateValue);

  };
    
  const handleAwardCertificate = async () => {
    console.log(fullNameValue, byuidValue, netidValue, languageValue, levelValue, opiScoreValue, wptScoreValue, todaysDateValue, recordIdValue, certificateTypeValue)
    const dataToSend = {
      FullName: fullNameValue,
      BYUID: byuidValue,
      NetID: netidValue,
      Language: languageValue,
      Level: levelValue,
      OPIScore: opiScoreValue,
      WPTScore: wptScoreValue,
      TodaysDate: todaysDateValue,
      RecordID: recordIdValue,
      CertificateType: certificateTypeValue,
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
            { type: 'award_one',
            dataToSend },
            {
              withCredentials: true,
              headers: {
                'X-CSRFToken': csrfToken,
              },
            }
          );
          // Handle the awardCertificateResponse as needed
          console.log(awardCertificateResponse.data);
          if (awardCertificateResponse.status === 200) {
            setLoading(false);
            setAwardedConfirmation(true);

          }
          
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
          {loading && (
          <PulseLoader
            loading={loading}
            size={5}
            aria-label="Loading Spinner"
            data-testid="loader"
            sx={{ height: 'inherit' }}
          />
        )}
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
          <Button
            onClick={() => {
              handleGetAllData(fullName, byuid, netid, language, level, opiScore, wptScore, todaysDate, recordId, certificateType);
              handleAwardCertificate();
              handleConfirmationClose();
            }}
            color="primary"
          >
            Yes
          </Button>
          <Button onClick={handleConfirmationClose} color="primary">
            No
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={awardedConfirmation} onClose={handleAwardedConfirmationClose}>
        <DialogTitle>Confirmation</DialogTitle>
        <DialogContent>
          Certificate awarded.
        </DialogContent>
        <DialogActions>
          <Button onClick={handleAwardedConfirmationClose} color="primary">
            OK
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
