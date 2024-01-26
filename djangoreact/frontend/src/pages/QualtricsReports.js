import React, { useState, useEffect, CSSProperties } from 'react';
import PulseLoader from "react-spinners/PulseLoader";
import { Helmet } from 'react-helmet-async';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { useTheme } from '@mui/material/styles';
import { set } from 'lodash';

import 'regenerator-runtime/runtime';

import {
  Button,
  Container,
  Stack,
  Typography,
  Select,
  MenuItem,
  Checkbox,
  Grid,
TextField,
IconButton,
Box
} from '@mui/material';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { fr } from 'date-fns/locale';

import {
  AppRadarChart,
  AppCurrentVisits,
  AppWebsiteVisits,
  AppTrafficBySite,
  AppWidgetSummary,
  AppCurrentSubject,
  AppConversionRates,
} from '../sections/@dashboard/app';
import Iconify from '../components/iconify';


export default function BlogPage() {
  const theme = useTheme();
  const navigate = useNavigate(); 

  const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
  const getQualtricsUrl = process.env.REACT_APP_QUALTRICS_URL;

  const [isLoading, setIsLoading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [qualtricsToken, setQualtricsToken] = useState('');
  const [response, setResponse] = useState(''); // server response
  const qualtricsTokenChange = (event) => {
    setQualtricsToken(event.target.value);
    };

  const handleFileChange = (event) => {
    const files = event.target.files;
    const filesArray = Array.from(files);  // Convert to array
    setSelectedFiles(filesArray);
  };
  

const handleFileUpload = () => {
    setIsLoading(true);
    const formData = new FormData();

    selectedFiles.forEach(file => {
        formData.append('files', file);
      });
    console.log(formData);
    console.log(qualtricsToken);
    formData.append('qualtricsToken', qualtricsToken);
    const fetchData = async () =>{
      try{
        const csrfToken = Cookies.get('csrftoken');
        const response = await axios.get(verifyTokenUrl, {
           withCredentials: true,
            headers: {
              "X-CSRFToken": csrfToken,
            }, 
        });
        if (response.status === 200) {
          const csrfToken = Cookies.get('csrftoken');
          const response = await axios.post(getQualtricsUrl, formData,
            {
            withCredentials: true,
            responseType: 'arraybuffer',
            headers: {
            'Content-Type': 'multipart/form-data',
              'X-CSRFToken': csrfToken,
              
            },
          });
          console.log(response);
          console.log(response.data); 
          const blob = new Blob([response.data], { type: 'application/zip' });

          // Generate a download link
          const link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);
          link.download = 'reports.zip';
        
          // Append the link to the document and trigger a click
          document.body.appendChild(link);
          link.click();
        
          // Remove the link from the document
          document.body.removeChild(link);
        } else {
          console.log('Error');
        }
        setIsLoading(false);
      } catch (error) {
        setIsLoading(false);
          if (error.response && error.response.status === 400) {
            console.log('Bad Request:', error.response.data);
          } else {
            navigate('/cls/login', { replace: true });
            console.log(error);
          }
      }
    };
    fetchData();
  };
  

  return (
    <>
      <Helmet>
        <title> CLS Admin </title>
      </Helmet>

      <Container>
      <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Typography variant="h4" gutterBottom>
            Generate Qualtrics Reports
          </Typography>
        </Stack>
        <Box>
      <TextField
        label="Enter Qualtrics Token"
        variant="outlined"
        margin="normal"
        fullWidth
        value={qualtricsToken}
        onChange={qualtricsTokenChange}
      />
    <Button
        component="label"
        htmlFor="file-upload-input"
        variant="contained"
        color="primary"
        sx={{ mr: 2 }}
        title="Select all CSV Files that you want to upload at the same time"
      >
       1. Select CSV Files
      </Button>
      <input
        type="file"
        multiple
        style={{ display: 'none' }}
        onChange={handleFileChange}
        id="file-upload-input"
      />
      <Typography variant="caption">
        {selectedFiles.length} file(s) selected
      </Typography>
      <Button
        variant="contained"
        color="primary"
        onClick={handleFileUpload}
        sx = {{ ml: 2 }}
      >
        <span style={{ visibility: isLoading ? 'hidden' : 'visible' }}>2. Upload CSV Files</span>
        {isLoading && (
          <div
            style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
            }}
          >
            <PulseLoader
              loading={isLoading}
              size={5}
              aria-label="Loading Spinner"
              data-testid="loader"
              sx={{ height: 'inherit' }}
            />
          </div>
        )}
      </Button>
    </Box>
      </Container>
    </>
  );
}
