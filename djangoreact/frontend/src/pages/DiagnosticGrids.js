import { Helmet } from 'react-helmet-async';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
// @mui
import '../theme/style.css'
import {
  Card,
  Stack,
  Button,
  Container,
  Grid,
  Typography,
  TextField,
  InputLabel,
  MenuItem,
  Box,
  Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle

} from '@mui/material';

import Select, { SelectChangeEvent } from '@mui/material/Select';
// components
import { format, parseISO } from 'date-fns';

import DatePicker from 'react-datepicker';

import { is } from 'date-fns/locale';
import { DiagnosticGridReports } from '../sections/@dashboard/app';
import LoadingModal from '../components/loadingModal/LoadingModal';

import Iconify from '../components/iconify';
// sections

// ----------------------------------------------------------------------

export default function DiagnosticGrids() {
  const navigate = useNavigate();

  const diagnosticGridsUrl = process.env.REACT_APP_POST_DIAGNOSTIC_GRIDS_URL;
  const getDataUrl = process.env.REACT_APP_GET_DIAGNOSTIC_GRIDS_URL

  const today = new Date();
  const oneYearFromToday = new Date();
  oneYearFromToday.setFullYear(today.getFullYear() - 1);

  const [startDate, setStartDate] = useState(oneYearFromToday);
  const [endDate, setEndDate] = useState(new Date());
  const [languageOptions, setLanguageOptions] = useState([]);
  const [language, setLanguage] = useState('All');
  const [masterLoader, setMasterLoader] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);

  const [allData, setAllData] = useState({})
  const [amSuperiorData, setAMSuperiorData] = useState({});
  const [ahSuperiorData, setAHSuperiorData] = useState({});
  const [alAdvancedData, setALAdvancedData] = useState({});
  const [ihAdvancedData, setIHAdvancedData] = useState({});
  const [superiorTotal, setSuperiorTotal] = useState(0);

  const [filteredAHSuperiorData, setFilteredAHSuperiorData] = useState({});
  const [filteredAMSuperiorData, setFilteredAMSuperiorData] = useState({});
  const [filteredALAdvancedData, setFilteredALAdvancedData] = useState({});
  const [filteredIHAdvancedData, setFilteredIHAdvancedData] = useState({});

  const [ihInsightDetails, setIHInsightDetails] = useState({});
  const [alInsightDetails, setALInsightDetails] = useState({});
  const [ahInsightDetails, setAHInsightDetails] = useState({});
  const [amInsightDetails, setAMInsightDetails] = useState({});

  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  const handleFileChange = (event) => {
    const files = event.target.files;
    const filesArray = Array.from(files);  // Convert to array
    setSelectedFiles(filesArray);
    handleClose();
  };

const getSchemaUrl = process.env.REACT_APP_GET_GRID_SCHEMA_URL;
const downloadSchema = () => {
  const csrfToken = Cookies.get('csrftoken');
    fetch(getSchemaUrl, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    }
  })
    .then(response => response.blob())
    .then(blob => {
      // Create a URL for the blob
      const url = window.URL.createObjectURL(blob);
      // Create an anchor (<a>) element with the URL
      const a = document.createElement('a');
      a.href = url;
      a.download = 'grid_schema.pdf'; // Set the file name for the download
      document.body.appendChild(a); // Append the anchor to the body
      a.click(); // Simulate a click on the anchor to trigger the download
      document.body.removeChild(a); // Clean up
      window.URL.revokeObjectURL(url); // Release the object URL
    })
    .catch(error => console.error('Error downloading the file:', error));
  };
  const fetchData = () => {
    try {
      const csrfToken = Cookies.get('csrftoken');
      axios.get(getDataUrl, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrfToken,
        },
      }).then(response => {
        console.log(response.data);
        
        const languages = Object.keys(response.data.languages).map(
          (key) => response.data.languages[key].language
        );
        languages.push('All');

        setLanguageOptions(languages);
        
        console.log(languages);
      }).catch(error => {
        navigate('/cls/login', { replace: true });
        console.log(error);
      });
    } catch (error) {
      navigate('/cls/login', { replace: true });
      console.log(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [getDataUrl, navigate]);
      
      const sendInfo = async () => {
        try {
          setAHSuperiorData({});
          setAMSuperiorData({});
          setALAdvancedData({});
          setIHAdvancedData({});
          setFilteredAHSuperiorData({});
          setFilteredALAdvancedData({});
          setFilteredAMSuperiorData({});
          setFilteredIHAdvancedData({});
          setIHInsightDetails({});
          setALInsightDetails({});
          setAMInsightDetails({});
          setAHInsightDetails({});
          setAllData({});

          setMasterLoader(true);
          const csrfToken = Cookies.get('csrftoken');
          const formattedStartDate = format(startDate, 'MM/dd/yyyy');
          const formattedEndDate = format(endDate, 'MM/dd/yyyy');
          const formData = new FormData();

          formData.append('language', language);
          formData.append('fromDate', formattedStartDate);
          formData.append('toDate', formattedEndDate);

          if (selectedFiles.length > 0) {
            selectedFiles.forEach(file => {
              formData.append('files', file);
            });
          }
          const response = await axios.post(
            diagnosticGridsUrl,
            formData,
            {
              withCredentials: true,
              headers: {
                'X-CSRFToken': csrfToken,
                
              }
            }
          );
          console.log(response.data);
          setAllData(response.data)
          setAMSuperiorData(response.data.am_superior_grid_results);
          const filteredAMSuperiorData = Object.fromEntries(
            Object.entries(response.data.am_superior_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0))
          );
          setFilteredAMSuperiorData(filteredAMSuperiorData);

          setAHSuperiorData(response.data.ah_superior_grid_results);
          const filteredAHSuperiorData = Object.fromEntries(
            Object.entries(response.data.ah_superior_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0))
          );
          setFilteredAHSuperiorData(filteredAHSuperiorData);

        setALAdvancedData(response.data.al_advanced_grid_results);
        const filteredALAdvancedData = Object.fromEntries(
          Object.entries(response.data.al_advanced_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0))
        );
        setFilteredALAdvancedData(filteredALAdvancedData);

        setIHAdvancedData(response.data.ih_advanced_grid_results);
        const filteredIHAdvancedData = Object.fromEntries(
          Object.entries(response.data.ih_advanced_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0))
        );
        setFilteredIHAdvancedData(filteredIHAdvancedData);
        setSuperiorTotal(response.data.superior_count)

        setIHInsightDetails(response.data.ih_insight_details);
        setALInsightDetails(response.data.al_insight_details);
        setAHInsightDetails(response.data.ah_insight_details);
        setAMInsightDetails(response.data.am_insight_details);
        console.log('Filter=', filteredAMSuperiorData, filteredAHSuperiorData, filteredALAdvancedData, filteredIHAdvancedData);
        // console.log('Details=', ihInsightDetails, alInsightDetails, ahInsightDetails, amInsightDetails);
        console.log('Details=', ahInsightDetails);

        setMasterLoader(false);

      } catch (error) {
        setMasterLoader(false);

        console.log(error);
      }

    }
  return (
    <>
      <Helmet>
        <title> CLS Admin </title>
      </Helmet>

      <Grid container spacing={0} justifyContent="center" alignItems="center">
        <Grid item xs={6} md={8} lg={8} sx={{ border: "3px solid #002e5d", borderRadius: "5px", marginTop: "1vw" }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1vw' }}>
            <Typography variant="h4" gutterBottom>
              OPIc Diagnostic Grids
            </Typography>
            <Box
                sx={{
                  display: 'flex', // Display buttons inline
                  gap: '0.5rem' // Space between buttons
                }}
              >
                <Button
                  variant="contained"
                  color="primary"
                  title="Select the CSV File that you want to upload"
                  onClick={handleOpen}
                >
                Upload CSV
                </Button>
              <Dialog open={open}>
                <DialogTitle>Upload Notification</DialogTitle>
                <DialogContent>
                  <DialogContentText>
                    Please select a CSV file with the following columns:<br/>
                    <strong>First Name, Last Name</strong> <br/>
                  </DialogContentText>
                </DialogContent>
                <DialogActions>
                  <label htmlFor="file-upload-input" style={{
                    display: 'inline-block',
                    padding: '6px 16px',
                    fontSize: '0.875rem',
                    minWidth: '64px',
                    boxSizing: 'border-box',
                    transition: 'background-color 0.3s, box-shadow 0.3s',
                    lineHeight: 1.75,
                    borderRadius: '4px',
                    letterSpacing: '0.02857em',
                    textTransform: 'uppercase',
                    backgroundColor: '#2065D1',
                    color: '#fff',
                    cursor: 'pointer',
                    textAlign: 'center',
                    textDecoration: 'none',
                    border: 'none',
                    outline: 'none'
                  }}>
                    OK
                  <input
                    type="file"
                    onChange={handleFileChange}
                    id="file-upload-input"
                    accept=".csv"
                    style={{
                      display: 'none'
                    }}
                  />
                  </label>
                  <Button color="error" onClick={handleClose}>Cancel</Button>
                </DialogActions>
              </Dialog>

            <Button
              variant="contained"
              color="primary"
              onClick={downloadSchema}
            >
              Download Database Schema
            </Button>
            </Box>
          </Box>
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginRight: "1vw" }}>
              {selectedFiles.length > 0 && selectedFiles.map((file, index) => (
                <div key={index} style={{ marginRight: "1vw" }}>
                  <Typography variant="caption">
                    Uploaded File: {file.name}
                  </Typography>
                  <Button
                    variant=""
                    color="primary"
                    size="small"
                    style={{ marginLeft: '1vw' }}
                    onClick={() => setSelectedFiles([])} // Use a function here
                  >
                    Clear
                  </Button>
                </div>
              ))}
            </div>
          <Stack direction="column" sx={{padding:'1vw'}}>
            <InputLabel id="demo-simple-select-label">Language</InputLabel>
                  <Select
                      labelId="demo-simple-select-label"
                      id="demo-simple-select"
                      value={language}
                      label="Language"
                      onChange={handleLanguageChange}
                      sx={{width: "60%"}}
                  > 
                    {languageOptions.map((lang, index) => (
                      <MenuItem key={index} value={lang}>{lang}</MenuItem>
                    ))}
                    
                  </Select>
          </Stack>

          <Stack direction="column" sx={{padding:'1vw'}}>
              <InputLabel id="demo-simple-select-label">Date Range</InputLabel>

              <Box sx={{ display: 'flex', gap: '10px' }}>
                <DatePicker
                  selected={startDate}
                  onChange={(date) => setStartDate(date)}
                  selectsStart
                  startDate={startDate}
                  endDate={endDate}
                  placeholderText="Start Date"
                  dateFormat="MM/dd/yyyy"
                />
              
                <DatePicker
                  selected={endDate}
                  onChange={(date) => setEndDate(date)}
                  selectsEnd
                  startDate={startDate}
                  endDate={endDate}
                  minDate={startDate}
                  placeholderText="End Date"
                  dateFormat="MM/dd/yyyy"
                />
              </Box>
          </Stack>
          <Stack direction="row"  sx={{padding:'1vw', justifyContent:'right'
          }}>
            {/* <Typography variant="caption">
              {selectedFiles.length} file(s) selected
            </Typography> */}
                <Button variant="contained" startIcon={<Iconify icon="eva:arrow-circle-down-outline" />} onClick={sendInfo}>
                    Generate Reports
              </Button>
          </Stack>
        </Grid>

        <LoadingModal isLoading={masterLoader} message="Retrieving data... Please wait..."/>

        {Object.keys(allData).length > 0 && (
          <Grid container justifyContent="center" item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
            <Card sx={{ width:"50%", p:2 }}>
              <div style={{ fontWeight: 'bold' }}>
              Students Who Scored A Superior (Will Not Display On Graph)
              </div>
              Superior Score Total = {superiorTotal}
            </Card>
          </Grid>
          )
        }
        {Object.keys(filteredAHSuperiorData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Advanced High (Sample Size = {ahSuperiorData['Total People']} Students)</div>
                          <div>Superior Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve to reach the Superior level?</div>
                        </>
                      }
                    chartData={filteredAHSuperiorData} 
                    details={ahInsightDetails}
                    total={ahSuperiorData['Total People']}
                  />
          </Grid>
          )
        }
        {Object.keys(filteredAMSuperiorData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Advanced Mid (Sample Size = {amSuperiorData['Total People']} Students)</div>
                          <div>Superior Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve to reach the Superior level?</div>
                        </>
                      }
                    chartData={filteredAMSuperiorData} 
                    details={amInsightDetails}
                    total={amSuperiorData['Total People']}
                  />
          </Grid>
          )
        }
        {Object.keys(filteredALAdvancedData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Advanced Low (Sample Size = {alAdvancedData['Total People']} Students)</div>
                          <div>Advanced Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve to reach the Superior level?</div>
                        </>
                      }
                    chartData={filteredALAdvancedData} 
                    details={alInsightDetails}
                    total={alAdvancedData['Total People']}
                  />
          </Grid>
          )
        }
        {Object.keys(filteredIHAdvancedData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Intermediate High (Sample Size = {ihAdvancedData['Total People']} Students)</div>
                          <div>Advanced Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve to reach the Superior level?</div>
                        </>
                      }
                    chartData={filteredIHAdvancedData} 
                    details={ihInsightDetails}
                    total={ihAdvancedData['Total People']}
                  />
          </Grid>
          )
        }

      </Grid>
        
    

    
    </>
  );
}      
