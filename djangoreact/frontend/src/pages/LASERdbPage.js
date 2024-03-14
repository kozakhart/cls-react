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
  TextareaAutosize,
  Grid,
TextField,
IconButton,
InputAdornment,
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
  const getLASERUrl = process.env.REACT_APP_LASER_URL;

  const [isLoading, setIsLoading] = useState(false);
  const [sqlQuery, setSqlQuery] = useState('');
  const sqlQueryChange = (event) => {
    setSqlQuery(event.target.value);
    };  

const handleQuery = () => {
    setIsLoading(true);
    const formattedSqlQuery = sqlQuery.replace(/\s+/g, ' ');
    const dataToSend={
      'sqlQuery': formattedSqlQuery
    };
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
          const response = await axios.post(getLASERUrl, dataToSend,
            {
            withCredentials: true,
            headers: {
              'X-CSRFToken': csrfToken,
              
            },
          });
          console.log(response);
          console.log(response.data); 
          const blob = new Blob([response.data], { type: 'text/csv' });

          const csvURL = window.URL.createObjectURL(blob);
      
          const link = document.createElement('a');
          link.href = csvURL;
          link.download = 'query-results.csv';
      
          document.body.appendChild(link);
          link.click();
      
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
            LASER Database Querys
          </Typography>
        </Stack>
        <Box>
          
      <TextField
      name="sqlQuery"
      label="Enter SQL Query"
      variant="outlined"
      margin="normal"
      fullWidth
      multiline
      rows={20}
      maxRows={200}
      value={sqlQuery}
      onChange={sqlQueryChange}
      />
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
      <Button
        variant="contained"
        color="primary"
        onClick={handleQuery}
        >
        <span style={{ visibility: isLoading ? 'hidden' : 'visible' }}>Execute Query</span>
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
      </div>
    </Box>
      </Container>
    </>
  );
}
