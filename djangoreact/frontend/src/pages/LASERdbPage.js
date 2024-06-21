import React, { useState, useEffect, CSSProperties } from 'react';
import PulseLoader from "react-spinners/PulseLoader";
import { Helmet } from 'react-helmet-async';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { useTheme } from '@mui/material/styles';

import 'regenerator-runtime/runtime';

import {
  Button,
  Container,
  Stack,
  Typography,
  Select,
  Card,
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
import { set } from 'lodash';

import  LaserMenu  from '../components/lasermenu/LaserMenu';


import "react-datepicker/dist/react-datepicker.css";

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

  const verifySessionUrl = process.env.REACT_APP_VERIFY_SESSION_URL;
  const getSchemaUrl = process.env.REACT_APP_GET_SCHEMA_URL;
  const getLASERUrl = process.env.REACT_APP_LASER_URL;
  const saveQueryUrl = process.env.REACT_APP_SAVE_QUERY_URL;

  const [isLoading, setIsLoading] = useState(false);
  const [sqlQuery, setSqlQuery] = useState('');
  const [labelValue, SetLabelValue] = useState('Select * from data;');
  const [data, setData] = useState(null);
  const [queryCreation, setQueryCreation] = useState([]);
  const [queryName, setQueryName] = useState('');
  const [query, setQuery] = useState('');

  const sqlQueryChange = (event) => {
    setSqlQuery(event.target.value);
    };  

    const getData = (query) => {
      setData(query);
      setSqlQuery(query);
      console.log('Data received from LaserMenu:', query);
    };
    const startQueryCreation = (create) => {
        setQueryCreation(create);
    };

    useEffect(() => {
      const fetchSessionData = async () => {
        try {
          const response = await axios.get(verifySessionUrl, {
            withCredentials: true,
          });
    
          if (response.status === 200) {
            console.log('Session is active');
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
    
  const downloadSchema = () => {
    fetch(getSchemaUrl)
    .then(response => response.blob())
    .then(blob => {
      // Create a URL for the blob
      const url = window.URL.createObjectURL(blob);
      // Create an anchor (<a>) element with the URL
      const a = document.createElement('a');
      a.href = url;
      a.download = 'db_schema.csv'; // Set the file name for the download
      document.body.appendChild(a); // Append the anchor to the body
      a.click(); // Simulate a click on the anchor to trigger the download
      document.body.removeChild(a); // Clean up
      window.URL.revokeObjectURL(url); // Release the object URL
    })
    .catch(error => console.error('Error downloading the file:', error));
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

          const response = await axios.post(getLASERUrl, dataToSend,
            {
            withCredentials: true,
            headers: {
              'X-CSRFToken': csrfToken,
              
            },
          });
          console.log(response);
          console.log(response.data); 
          const blob = new Blob([response.data], { type: 'text/csv;charset=utf-8' });

          const csvURL = window.URL.createObjectURL(blob);
      
          const link = document.createElement('a');
          link.href = csvURL;
          link.download = 'query-results.csv';
      
          document.body.appendChild(link);
          link.click();
      
          document.body.removeChild(link);
        setIsLoading(false);
      } catch (error) {
        setIsLoading(false);
        if (error.response && error.response.status === 400) {
            console.log('Bad Request:', error.response.data);
        } else if (error.response && (error.response.status === 401 || error.response.status === 403)) {
            navigate('/cls/login', { replace: true });
            console.log(error);
        } else {
            console.log(error);
        }
      }
    };
    fetchData();
  };
  
  const exitQueryCreation = () => {
    setQueryCreation(false);
  }

  const dataToSend={
    'query_label': queryName,
    'query': query,
  };
  const saveQuery = async () => {
    const csrfToken = Cookies.get('csrftoken');

    const response = await axios.post(saveQueryUrl, dataToSend,
            {
            withCredentials: true,
            headers: {
              'X-CSRFToken': csrfToken,
              
            },
          });
    setQueryCreation(false);
    alert('Query saved');
    window.location.replace('/cls/dashboard/laser-database');
    
  }
  const queryNameChange = (event) => {
    setQueryName(event.target.value);
  }
  const queryDataChange = (event) => {
    setQuery(event.target.value);
  }

  return (
    <>
      <Helmet>
        <title> CLS Admin </title>
      </Helmet>

      <Container>
    
      <Stack direction="row" alignItems="center" justifyContent="space-between" mt={5}>
          <Typography variant="h4" gutterBottom>
            LASER Database Queries
          </Typography>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <LaserMenu sendQuery={getData} createQuery={startQueryCreation}/>
            <Button
              variant="contained"
              color="primary"
              onClick={downloadSchema}
              style={{ marginLeft: '1vw' }}
            >
              Download Database Schema
            </Button>
          </div>
        </Stack>
        <Box>
        {queryCreation ? 
            (<Card sx={{ m: 5, p:2 }}>
              <div style={{ display: 'flex' }}>
                <TextField label="Query Name" sx={{ pr:2 }} value={queryName} onChange={queryNameChange}/>
                <TextField label="Query" sx={{ pr:5, width:"50%" }} value={query} onChange={queryDataChange}/>
                <Button variant="contained" color="primary" sx={{ width:"12%" }} onClick={saveQuery}>Save Query</Button>
                <Button variant="contained" color="error" sx={{ marginLeft:"1vw", width:"10%"}} onClick={exitQueryCreation}>Exit</Button>
              </div>
            </Card>) 
            : 
            (
            <div>
              <TextField
              name="sqlQuery"
              label={labelValue}
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
            </div>
            )
          }
     
      
    </Box>
      </Container>
    </>
  );
}
