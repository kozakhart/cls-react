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

// , lastName, approved, reason, language,
//    testdate1, time1, time2, testdate2, time3, time4, testscheduled, certificatestatus, cometocampus, 
//    cannotcome, email, emailsent, ltischedule, phone, scores, byuid, netid, entrydate, entrytime, 
//    major, secondmajor, minor, previousexperience 
export default function UpdateNotification({firstnameID, lastnameID, approvedID, reasonID, languageID, languageotherID, testdate1ID, time1ID, time2ID, testdate2ID, 
  time3ID, time4ID, testscheduledID, certificatestatusID, cometocampusID, cannotcomeID, emailID, emailsentID, ltischeduleID, phoneID, 
  scoresID, byuidID, netidID, entrydateID, entrytimeID, majorID, secondmajorID, minorID, previousexperienceID, recordId}) {
  const [isConfirmationOpen, setConfirmationOpen] = useState(false);
  const [firstNameValue, setFirstNameValue] = useState('');
  const [lastNameValue, setLastNameValue] = useState('');
  const [approvedValue, setApprovedValue] = useState('');
  const [reasonValue, setReasonValue] = useState('');
  const [languageValue, setLanguageValue] = useState('');
  const [languageotherValue, setLanguageOtherValue] = useState('');
  const [testdate1Value, setTestDate1Value] = useState('');
  const [time1Value, setTime1Value] = useState('');
  const [time2Value, setTime2Value] = useState('');
  const [testdate2Value, setTestDate2Value] = useState('');
  const [time3Value, setTime3Value] = useState('');
  const [time4Value, setTime4Value] = useState('');
  const [testscheduledValue, setTestScheduledValue] = useState('');
  const [certificatestatusValue, setCertificateStatusValue] = useState('');
  const [cometocampusValue, setComeToCampusValue] = useState('');
  const [cannotcomeValue, setCannotComeValue] = useState('');
  const [emailValue, setEmailValue] = useState('');
  const [emailsentValue, setEmailSentValue] = useState('');
  const [ltischeduleValue, setLTIScheduleValue] = useState('');
  const [phoneValue, setPhoneValue] = useState('');
  const [scoresValue, setScoresValue] = useState('');
  const [byuidValue, setBYUIDValue] = useState('');
  const [netidValue, setNetIDValue] = useState('');
  const [entrydateValue, setEntryDateValue] = useState('');
  const [entrytimeValue, setEntryTimeValue] = useState('');
  const [majorValue, setMajorValue] = useState('');
  const [secondmajorValue, setSecondMajorValue] = useState('');
  const [minorValue, setMinorValue] = useState('');
  const [previousexperienceValue, setPreviousExperienceValue] = useState('');
  const [updateData, setUpdateData] = useState(false);

  const updateRecordUrl = `${process.env.REACT_APP_UPDATE_RECORD_URL}${recordId}/`;
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
      handleGetAllData(firstnameID, lastnameID, approvedID, reasonID, languageID, languageotherID, testdate1ID, time1ID, time2ID, testdate2ID,
        time3ID, time4ID, testscheduledID, certificatestatusID, cometocampusID, cannotcomeID, emailID, emailsentID, ltischeduleID, phoneID,
        scoresID, byuidID, netidID, entrydateID, entrytimeID, majorID, secondmajorID, minorID, previousexperienceID);
      setUpdateData(false); // Reset the flag
    }
  }, [updateData, firstnameID, lastnameID, approvedID, reasonID, languageID, languageotherID, testdate1ID, time1ID, time2ID, testdate2ID,
    time3ID, time4ID, testscheduledID, certificatestatusID, cometocampusID, cannotcomeID, emailID, emailsentID, ltischeduleID, phoneID,
    scoresID, byuidID, netidID, entrydateID, entrytimeID, majorID, secondmajorID, minorID, previousexperienceID]);

  const handleGetAllData = (firstnameID, lastnameID, approvedID, reasonID, languageID, languageotherID, testdate1ID, time1ID, time2ID, testdate2ID,
    time3ID, time4ID, testscheduledID, certificatestatusID, cometocampusID, cannotcomeID, emailID, emailsentID, ltischeduleID, phoneID,
    scoresID, byuidID, netidID, entrydateID, entrytimeID, majorID, secondmajorID, minorID, previousexperienceID) => {
    const firstnameElement = document.getElementById(firstnameID);
    const lastnameElement = document.getElementById(lastnameID);
    const approvedElement = document.getElementById(approvedID);
    const reasonElement = document.getElementById(reasonID);
    const languageElement = document.getElementById(languageID);
    const languageotherElement = document.getElementById(languageotherID);
    const testdate1Element = document.getElementById(testdate1ID);
    const time1Element = document.getElementById(time1ID);
    const time2Element = document.getElementById(time2ID);
    const testdate2Element = document.getElementById(testdate2ID);
    const time3Element = document.getElementById(time3ID);
    const time4Element = document.getElementById(time4ID);
    const testscheduledElement = document.getElementById(testscheduledID);
    const certificatestatusElement = document.getElementById(certificatestatusID);
    const cometocampusElement = document.getElementById(cometocampusID);
    const cannotcomeElement = document.getElementById(cannotcomeID);
    const emailElement = document.getElementById(emailID);
    const emailsentElement = document.getElementById(emailsentID);
    const ltischeduleElement = document.getElementById(ltischeduleID);
    const phoneElement = document.getElementById(phoneID);
    const scoresElement = document.getElementById(scoresID);
    const byuidElement = document.getElementById(byuidID);
    const netidElement = document.getElementById(netidID);
    const entrydateElement = document.getElementById(entrydateID);
    const entrytimeElement = document.getElementById(entrytimeID);
    const majorElement = document.getElementById(majorID);
    const secondmajorElement = document.getElementById(secondmajorID);
    const minorElement = document.getElementById(minorID);
    const previousexperienceElement = document.getElementById(previousexperienceID);

    console.log(firstnameElement);
    console.log(lastnameElement);
    const firstNameValue = firstnameElement.value;
    const lastNameValue = lastnameElement.value;
    const approvedValue = approvedElement.value;
    const reasonValue = reasonElement.value;
    const languageValue = languageElement.value;
    const languageotherValue = languageotherElement.value;
    const testdate1Value = testdate1Element.value;
    const time1Value = time1Element.value;
    const time2Value = time2Element.value;
    const testdate2Value = testdate2Element.value;
    const time3Value = time3Element.value;
    const time4Value = time4Element.value;
    const testscheduledValue = testscheduledElement.value;
    const certificatestatusValue = certificatestatusElement.value;
    const cometocampusValue = cometocampusElement.value;
    const cannotcomeValue = cannotcomeElement.value;
    const emailValue = emailElement.value;
    const emailsentValue = emailsentElement.value;
    const ltischeduleValue = ltischeduleElement.value;
    const phoneValue = phoneElement.value;
    const scoresValue = scoresElement.value;
    const byuidValue = byuidElement.value;
    const netidValue = netidElement.value;
    const entrydateValue = entrydateElement.value;
    const entrytimeValue = entrytimeElement.value;
    const majorValue = majorElement.value;
    const secondmajorValue = secondmajorElement.value;
    const minorValue = minorElement.value;
    const previousexperienceValue = previousexperienceElement.value;

    setFirstNameValue(firstNameValue);
    setLastNameValue(lastNameValue);
    setApprovedValue(approvedValue);
    setReasonValue(reasonValue);
    setLanguageValue(languageValue);
    setLanguageOtherValue(languageotherValue);
    setTestDate1Value(testdate1Value);
    setTime1Value(time1Value);
    setTime2Value(time2Value);
    setTestDate2Value(testdate2Value);
    setTime3Value(time3Value);
    setTime4Value(time4Value);
    setTestScheduledValue(testscheduledValue);
    setCertificateStatusValue(certificatestatusValue);
    setComeToCampusValue(cometocampusValue);
    setCannotComeValue(cannotcomeValue);
    setEmailValue(emailValue);
    setEmailSentValue(emailsentValue);
    setLTIScheduleValue(ltischeduleValue);
    setPhoneValue(phoneValue);
    setScoresValue(scoresValue);
    setBYUIDValue(byuidValue);
    setNetIDValue(netidValue);
    setEntryDateValue(entrydateValue);
    setEntryTimeValue(entrytimeValue);
    setMajorValue(majorValue);
    setSecondMajorValue(secondmajorValue);
    setMinorValue(minorValue);
    setPreviousExperienceValue(previousexperienceValue);
  };
  const navigate = useNavigate();

  const handleUpdateData = () => {
    
    const dataToSend = {
      FirstName: firstNameValue,
      LastName: lastNameValue,
      Approved: approvedValue,
      Reason: reasonValue,
      Language: languageValue,
      LanguageOther: languageotherValue,
      TestDate1: testdate1Value,
      Time1: time1Value,
      Time2: time2Value,
      TestDate2: testdate2Value,
      Time3: time3Value,
      Time4: time4Value,
      TestScheduled: testscheduledValue,
      CertificateStatus: certificatestatusValue,
      ComeToCampus: cometocampusValue,
      CannotCome: cannotcomeValue,
      Email: emailValue,
      EmailSent: emailsentValue,
      LTISchedule: ltischeduleValue,
      Phone: phoneValue,
      Scores: scoresValue,
      BYUID: byuidValue,
      NetID: netidValue,
      EntryDate: entrydateValue,
      EntryTime: entrytimeValue,
      Major: majorValue,
      SecondMajor: secondmajorValue,
      Minor: minorValue,
      PreviousExperience: previousexperienceValue,
      RecordID: recordId
      // Other data to send
    };
    const csrfToken = Cookies.get("csrftoken");
    axios
    .post(updateRecordUrl, dataToSend, {
      withCredentials: true,
      headers: {
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => {
        console.log('Data updated successfully:', response);
        setConfirmationOpen(false);
        navigate('/cls/dashboard/user', { replace: true });
      })
      .catch((error) => {
        console.error('Error updating data:', error);
      });
  };
  
  return (
    <Container style={{padding:'0'}}>
      <div style={{ display: 'flex', justifyContent: 'left'}}>
        <MenuItem
        onClick={() => {
          handleCheckData();
          handleGetAllData(firstnameID, lastnameID, approvedID, reasonID, languageID, languageotherID, testdate1ID, time1ID, time2ID, testdate2ID,
            time3ID, time4ID, testscheduledID, certificatestatusID, cometocampusID, cannotcomeID, emailID, emailsentID, ltischeduleID, phoneID,
            scoresID, byuidID, netidID, entrydateID, entrytimeID, majorID, secondmajorID, minorID, previousexperienceID);
        }}
        style={{fontWeight: 'bold' }}>
          <Iconify icon={'eva:edit-fill'} sx={{ mr: 1 }}/>
          Update
        </MenuItem>
      </div>

      <Dialog open={isConfirmationOpen} onClose={handleConfirmationClose}>
        <DialogTitle>Confirmation</DialogTitle>
        <DialogContent>
          Are you sure you want to update this data?
        </DialogContent>
        <DialogActions>
        <Button onClick={() => {
            handleGetAllData(firstnameID, lastnameID, approvedID, reasonID, languageID, languageotherID, testdate1ID, time1ID, time2ID, testdate2ID,
              time3ID, time4ID, testscheduledID, certificatestatusID, cometocampusID, cannotcomeID, emailID, emailsentID, ltischeduleID, phoneID,
              scoresID, byuidID, netidID, entrydateID, entrytimeID, majorID, secondmajorID, minorID, previousexperienceID);
            handleUpdateData();
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
