import { Helmet } from 'react-helmet-async';
import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
import html2canvas from 'html2canvas';
// @mui
import ApexCharts from 'apexcharts';
import '../theme/style.css'
import MenuIcon from '@mui/icons-material/Menu';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import jsPDF from 'jspdf';

import {
  Card,
  Stack,
  Button,
  Container,
  Grid,
  IconButton,
  Typography,
  TextField,
  InputLabel,
  MenuItem,
  Menu,
  Box,
  List,
  ListItem,
  ListItemText,
  Divider,
  Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle

} from '@mui/material';

import Select, { SelectChangeEvent } from '@mui/material/Select';
// components
import { format, parseISO } from 'date-fns';

import DatePicker from 'react-datepicker';

import { is } from 'date-fns/locale';
import { DiagnosticGridReports, DiagnosticGroupChart } from '../sections/@dashboard/app';
import LoadingModal from '../components/loadingModal/LoadingModal';

import Iconify from '../components/iconify';
// sections

// ----------------------------------------------------------------------

export default function DiagnosticGrids() {
  const navigate = useNavigate();

  const diagnosticGridsUrl = process.env.REACT_APP_POST_DIAGNOSTIC_GRIDS_URL;
  const getDataUrl = process.env.REACT_APP_GET_DIAGNOSTIC_GRIDS_URL;

  const today = new Date();
  const oneYearFromToday = new Date();
  oneYearFromToday.setFullYear(today.getFullYear() - 1);

  const [startDate, setStartDate] = useState(oneYearFromToday);
  const [endDate, setEndDate] = useState(new Date());
  const [languageOptions, setLanguageOptions] = useState([]);
  const [language, setLanguage] = useState('All');
  const [testTypeOptions, setTestTypeOptions] = useState(['OPIc', 'OPI', 'WPT']);
  const [testType, setTestType] = useState('OPIc');
  const [masterLoader, setMasterLoader] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);

  const [allData, setAllData] = useState({})
  const [ahSuperiorData, setAHSuperiorData] = useState({});
  const [amSuperiorData, setAMSuperiorData] = useState({});
  const [alAdvancedData, setALAdvancedData] = useState({});
  const [ihAdvancedData, setIHAdvancedData] = useState({});
  const [imAdvancedData, setIMAdvancedData] = useState({});
  const [ilAdvancedData, setILAdvancedData] = useState({});
  const [nhIntermediateData, setNHIntermediateData] = useState({});
  const [nmIntermediateData, setNMIntermediateData] = useState({});
  const [nlIntermediateData, setNLIntermediateData] = useState({});

  const [superiorTotal, setSuperiorTotal] = useState(0);

  const [filteredAHSuperiorData, setFilteredAHSuperiorData] = useState({});
  const [filteredAMSuperiorData, setFilteredAMSuperiorData] = useState({});
  const [filteredALAdvancedData, setFilteredALAdvancedData] = useState({});
  const [filteredIHAdvancedData, setFilteredIHAdvancedData] = useState({});
  const [filteredIMAdvancedData, setFilteredIMAdvancedData] = useState({});
  const [filteredILAdvancedData, setFilteredILAdvancedData] = useState({});
  const [filteredNHIntermediateData, setFilteredNHIntermediateData] = useState({});
  const [filteredNMIntermediateData, setFilteredNMIntermediateData] = useState({});
  const [filteredNLIntermediateData, setFilteredNLIntermediateData] = useState({});

  const [nlInsightDetails, setNLInsightDetails] = useState({});
  const [nmInsightDetails, setNMInsightDetails] = useState({});
  const [nhInsightDetails, setNHInsightDetails] = useState({});
  const [ilInsightDetails, setILInsightDetails] = useState({});
  const [imInsightDetails, setIMInsightDetails] = useState({});
  const [ihInsightDetails, setIHInsightDetails] = useState({});
  const [alInsightDetails, setALInsightDetails] = useState({});
  const [amInsightDetails, setAMInsightDetails] = useState({});
  const [ahInsightDetails, setAHInsightDetails] = useState({});

  const [viewByGridType, setViewByGridType] = useState(true);

  const [open, setOpen] = useState(false);

  const [anchorEl, setAnchorEl] = useState(null);


const scoreMapping = {
  "nl_intermediate_grid_results": "Novice Low",
  "nm_intermediate_grid_results": "Novice Mid",
  "nh_intermediate_grid_results": "Novice High",
  "il_advanced_grid_results": "Intermediate Low",
  "im_advanced_grid_results": "Intermediate Mid",
  "ih_advanced_grid_results": "Intermediate High",
  "al_advanced_grid_results": "Advanced Low",
  "am_superior_grid_results": "Advanced Mid",
  "ah_superior_grid_results": "Advanced High"
};

const emptyKeys = Object.keys(allData)
  .filter((key) => {
    const value = allData[key];
    return key.indexOf("grid_results") !== -1 && Object.keys(value).length === 0;
  })
  .map((key) => scoreMapping[key]) // Map the filtered keys to human-readable names
  .filter((result) => result !== undefined); // Remove any undefined values (if mapping not found)

if (testType === "OPIc") {
  emptyKeys.push("Superior"); // Add "Superior Grid" manually if testTypeOptions is "OPIc"
}

  
  const handleViewByGridType = () => {
    setViewByGridType(!viewByGridType);
  };

  const handleTestTypeChange = (event) => {
    setTestType(event.target.value);
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

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

  const chartRefs = useRef([]);

const handleExportAllCharts = async () => {
  const screenshotPromises = [];

  // Loop through each chart ref and create a screenshot promise
  chartRefs.current.forEach((chartDiv) => {
    if (chartDiv) {
      // Temporarily disable box-shadow
      const originalBoxShadow = chartDiv.style.boxShadow;
      chartDiv.style.boxShadow = 'unset'; // or 'none'

      screenshotPromises.push(
        html2canvas(chartDiv, {
          backgroundColor: '#ffffff' // Ensure background is white
        }).then((canvas) => {
          // Restore original box-shadow
          chartDiv.style.boxShadow = originalBoxShadow;

          const width = canvas.width;
          const height = canvas.height;
          const imgData = canvas.toDataURL('image/png');
          return { imgData, width, height };
        })
      );
    }
  });


  // Resolve all screenshot promises concurrently
  const screenshots = await Promise.all(screenshotPromises);

  // Initialize jsPDF document based on the first chart's dimensions
  const firstScreenshot = screenshots[0];
  const pdf = jsPDF({
    orientation: firstScreenshot.width > firstScreenshot.height ? 'landscape' : 'portrait', // Set orientation dynamically
    unit: 'px',
    format: [firstScreenshot.width, firstScreenshot.height], // Use the dimensions of the first chart
  });

  // Add each screenshot as a new page
  screenshots.forEach((screenshot, index) => {
    const { imgData, width, height } = screenshot;

    // If it's not the first page, add a new page with the correct size
    if (index > 0) {
      pdf.addPage([width, height], width > height ? 'landscape' : 'portrait');
    }

    // Add the image to the PDF document with dynamic size
    pdf.addImage(imgData, 'PNG', 0, 0, width, height);
  });

  // Save the PDF document
  pdf.save('charts.pdf');
};


const getExampleCSVUrl = process.env.REACT_APP_GET_CSV_EXAMPLE_DIAGNOSTIC_GRIDS_URL;
const downloadExampleCSV = () => {
    const csrfToken = Cookies.get('csrftoken');
    fetch(getExampleCSVUrl, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
      }
    }
    )
    .then(response => response.blob())
    .then(blob => {
      // Create a URL for the blob
      const url = window.URL.createObjectURL(blob);
      // Create an anchor (<a>) element with the URL
      const a = document.createElement('a');
      a.href = url;
      a.download = 'example.csv'; // Set the file name for the download
      document.body.appendChild(a); // Append the anchor to the body
      a.click(); // Simulate a click on the anchor to trigger the download
      document.body.removeChild(a); // Clean up
      window.URL.revokeObjectURL(url); // Release the object URL
      handleMenuClose();
    })
    .catch(error => console.error('Error downloading the file:', error));
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
      handleMenuClose();
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
          setIMAdvancedData({});
          setILAdvancedData({});
          setNHIntermediateData({});
          setNMIntermediateData({});
          setNLIntermediateData({});

          setFilteredAHSuperiorData({});
          setFilteredALAdvancedData({});
          setFilteredAMSuperiorData({});
          setFilteredIHAdvancedData({});
          setFilteredIMAdvancedData({});
          setFilteredILAdvancedData({});
          setFilteredNHIntermediateData({});
          setFilteredNMIntermediateData({});
          setFilteredNLIntermediateData({});

          setNLInsightDetails({});
          setNMInsightDetails({});
          setNHInsightDetails({});
          setILInsightDetails({});
          setIMInsightDetails({});
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
          formData.append('testType', testType);

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

          if (response.data.csv_file) {
            const csvBase64 = response.data.csv_file;  // Get the base64 CSV from the response

            // Decode the base64-encoded CSV to a string
            const csvContent = atob(csvBase64);

            // Convert the CSV content into a Blob for download
            const blob = new Blob([csvContent], { type: 'text/csv' });

            // Create a link to trigger the download
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'missing_candidates.csv';  // Specify the CSV file name
            document.body.appendChild(link);

            // Trigger the download
            link.click();

            // Clean up the DOM
            document.body.removeChild(link);
        } else {
            console.log('CSV file not found in the response');
        }
          
          setAHSuperiorData(response.data.ah_superior_grid_results);
          const filteredAHSuperiorData = Object.fromEntries(
            Object.entries(response.data.ah_superior_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0 &&
            key !== 'Total People' && 
            key !== 'Total Function Count'))
            );
          setFilteredAHSuperiorData(filteredAHSuperiorData);

          setAMSuperiorData(response.data.am_superior_grid_results);
          const filteredAMSuperiorData = Object.fromEntries(
            Object.entries(response.data.am_superior_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0 &&
            key !== 'Total People' && 
            key !== 'Total Function Count' &&
            key !== 'Total People' && 
            key !== 'Total Function Count'))
            );
          setFilteredAMSuperiorData(filteredAMSuperiorData);

          setALAdvancedData(response.data.al_advanced_grid_results);
          const filteredALAdvancedData = Object.fromEntries(
            Object.entries(response.data.al_advanced_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0 &&
            key !== 'Total People' && 
            key !== 'Total Function Count'))
            );
          setFilteredALAdvancedData(filteredALAdvancedData);

          setIHAdvancedData(response.data.ih_advanced_grid_results);
          const filteredIHAdvancedData = Object.fromEntries(
            Object.entries(response.data.ih_advanced_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0 &&
            key !== 'Total People' && 
            key !== 'Total Function Count'))
            );
          setFilteredIHAdvancedData(filteredIHAdvancedData);
          setSuperiorTotal(response.data.superior_count)

          setIMAdvancedData(response.data.im_advanced_grid_results);
          const filteredIMAdvancedData = Object.fromEntries(
            Object.entries(response.data.im_advanced_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0 &&
            key !== 'Total People' && 
            key !== 'Total Function Count'))
            );
          setFilteredIMAdvancedData(filteredIMAdvancedData);

          setILAdvancedData(response.data.il_advanced_grid_results);
          const filteredILAdvancedData = Object.fromEntries(
            Object.entries(response.data.il_advanced_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0 &&
            key !== 'Total People' && 
            key !== 'Total Function Count'))
            );
          setFilteredILAdvancedData(filteredILAdvancedData);

          setNLIntermediateData(response.data.nl_intermediate_grid_results);
          const filteredNLIntermediateData = Object.fromEntries(
            Object.entries(response.data.nl_intermediate_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0 &&
            key !== 'Total People' && 
            key !== 'Total Function Count'))
            );
          setFilteredNLIntermediateData(filteredNLIntermediateData);

          setNMIntermediateData(response.data.nm_intermediate_grid_results);
          const filteredNMIntermediateData = Object.fromEntries(
            Object.entries(response.data.nm_intermediate_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0 &&
            key !== 'Total People' && 
            key !== 'Total Function Count'))
            );
          setFilteredNMIntermediateData(filteredNMIntermediateData);

          setNHIntermediateData(response.data.nh_intermediate_grid_results);
          const filteredNHIntermediateData = Object.fromEntries(
            Object.entries(response.data.nh_intermediate_grid_results).filter(([key, value]) => typeof value === 'number' && (value % 1 !== 0 || value === 0 || value === 1.0 &&
            key !== 'Total People' && 
            key !== 'Total Function Count'))
            );
          setFilteredNHIntermediateData(filteredNHIntermediateData);

          setNLInsightDetails(response.data.nl_insight_details);
          setNMInsightDetails(response.data.nm_insight_details);
          setNHInsightDetails(response.data.nh_insight_details);
          setILInsightDetails(response.data.il_insight_details);
          setIMInsightDetails(response.data.im_insight_details);
          setIHInsightDetails(response.data.ih_insight_details);
          setALInsightDetails(response.data.al_insight_details);
          setAMInsightDetails(response.data.am_insight_details);
          setAHInsightDetails(response.data.ah_insight_details);
        console.log('Filter=', filteredAMSuperiorData, filteredAHSuperiorData, filteredALAdvancedData, filteredIHAdvancedData, filteredIMAdvancedData, filteredILAdvancedData, filteredNHIntermediateData, filteredNMIntermediateData, filteredNLIntermediateData);
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
              <Dialog open={open}>
                <DialogTitle>Upload Notification</DialogTitle>
                <DialogContent>
                  <DialogContentText>
                    This is an optional step. Please select a CSV file with the following columns:<br/>
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

            <div>
              <Button
                variant="contained"
                color="primary"
                aria-label="menu"
                onClick={handleMenuOpen}
              >
                Additional Resources
                <MenuIcon sx={{marginLeft:1}} />
              </Button>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
                    anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'right',
                  }}
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
              >
                <MenuItem onClick={downloadSchema}>
                  <Button
                    variant="text"
                    color="primary"
                    sx={{
                      width: "100%",
                      '&:hover': {
                        backgroundColor: 'transparent', // Removes the background color on hover
                      },
                    }}
                  >
                    Download Function Schemas
                  </Button>
                </MenuItem>
                <MenuItem onClick={downloadExampleCSV}>
                  <Button
                    variant="text"
                    color="primary"
                    sx={{
                      width: "100%",
                      '&:hover': {
                        backgroundColor: 'transparent', // Removes the background color on hover
                      },
                    }}
                  >
                    Download Example CSV
                  </Button>
                </MenuItem>
              </Menu>
            </div>
            </Box>
          </Box>

          <Stack direction="column" sx={{padding:'1vw'}}>
            <InputLabel id="demo-simple-select-label">Test Type</InputLabel>
                  <Select
                      labelId="demo-simple-select-label"
                      id="demo-simple-select"
                      value={testType}
                      label="Test Type"
                      onChange={handleTestTypeChange}
                      sx={{width: "60%"}}
                  > 
                    {testTypeOptions.map((test, index) => (
                      <MenuItem key={index} value={test}>{test}</MenuItem>
                    ))}
                    
                  </Select>
          </Stack>
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
                      <div style={{ display: 'flex', justifyContent: 'flex-end', marginRight: "1vw" }}>
              {selectedFiles.length > 0 && selectedFiles.map((file, index) => (
                <div key={index} style={{ marginRight: "1vw" }}>
                  <Typography variant="caption">
                    Uploaded File: {file.name}
                  </Typography>
                  <Button
                    variant="text"
                    color="error"
                    size="small"
                    style={{ marginLeft: '1vw' }}
                    onClick={() => setSelectedFiles([])} // Use a function here
                  >
                    Clear
                  </Button>
                </div>
              ))}
            </div>
          <Stack direction="row"  sx={{padding:'1vw', justifyContent:'right'
          }}>

            {/* <Typography variant="caption">
              {selectedFiles.length} file(s) selected
            </Typography> */}
                <Button
                  variant="contained"
                  color="primary"
                  title="Select the CSV File that you want to upload"
                  onClick={handleOpen}
                  sx={{marginRight: "1vw"}}
                >
                Upload CSV
                </Button>
                <Button variant="contained" startIcon={<Iconify icon="eva:arrow-circle-down-outline" />} onClick={sendInfo}>
                    Generate Reports
              </Button>
          </Stack>
        </Grid>

        <LoadingModal isLoading={masterLoader} message="Retrieving data... Please wait..."/>

        {Object.keys(allData).length > 0 && (
          <Grid container justifyContent="left" item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
<Card sx={{ width: "50%", p: 1, boxShadow: 1, overflowY: 'auto' }}>
      <Typography variant="subtitle1" sx={{ fontWeight: 'bold', marginBottom: 1 }}>
        Scores Not Present In Results
      </Typography>
      <div>
        {emptyKeys.length > 0 ? (
          <Grid container spacing={2}>
            {emptyKeys.map((key, index) => (
              <Grid item xs={6} key={index}>
                <List sx={{ padding: 0 }}>
                  <ListItem sx={{ padding: "4px 0" }}>
                    <ListItemText primary={key} />
                  </ListItem>
                  <Divider sx={{ margin: "4px 0" }} />
                </List>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Typography variant="body2" sx={{ padding: 1 }}>No empty results</Typography>
        )}
      </div>
    </Card>
           <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', mt: 2 }}>
      <FormControlLabel
        control={<Checkbox />}
        label="Group Grid Types"
        sx={{ marginLeft: 1 }} // Set max height
        onChange={handleViewByGridType}
      />
      <Button 
        onClick={handleExportAllCharts} 
      >
        Export All Charts as PDF
      </Button>
    </Box>
          </Grid>
          )
        } 
        {viewByGridType ? (
        <>
        

        {Object.keys(filteredAHSuperiorData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
            <div ref={(el) => { chartRefs.current[0] = el; }} style={{ backgroundColor: '#ffffff' }}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Advanced High (Sample Size = {ahSuperiorData['Total People']} Students)</div>
                          <div>Superior Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve?</div>
                        </>
                      }
                    chartData={filteredAHSuperiorData} 
                    details={ahInsightDetails}
                    total={ahSuperiorData['Total People']}
                  />
            </div>
          </Grid>
          )
        }
        {Object.keys(filteredAMSuperiorData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
            <div ref={(el) => { chartRefs.current[1] = el; }} style={{ backgroundColor: '#ffffff' }}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Advanced Mid (Sample Size = {amSuperiorData['Total People']} Students)</div>
                          <div>Superior Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve?</div>
                        </>
                      }
                    chartData={filteredAMSuperiorData} 
                    details={amInsightDetails}
                    total={amSuperiorData['Total People']}
                  />
            </div>
          </Grid>
          )
        }
        {Object.keys(filteredALAdvancedData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
            <div ref={(el) => { chartRefs.current[2] = el; }} style={{ backgroundColor: '#ffffff' }}>

                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Advanced Low (Sample Size = {alAdvancedData['Total People']} Students)</div>
                          <div>Advanced Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve?</div>
                        </>
                      }
                    chartData={filteredALAdvancedData} 
                    details={alInsightDetails}
                    total={alAdvancedData['Total People']}
                  />
            </div>
          </Grid>
          )
        }
        {Object.keys(filteredIHAdvancedData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
            <div ref={(el) => { chartRefs.current[3] = el; }} style={{ backgroundColor: '#ffffff' }}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Intermediate High (Sample Size = {ihAdvancedData['Total People']} Students)</div>
                          <div>Advanced Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve?</div>
                        </>
                      }
                    chartData={filteredIHAdvancedData} 
                    details={ihInsightDetails}
                    total={ihAdvancedData['Total People']}
                  />
            </div>
          </Grid>
          )
        }
        {Object.keys(filteredIMAdvancedData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
            <div ref={(el) => { chartRefs.current[4] = el; }} style={{ backgroundColor: '#ffffff' }}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Intermediate Mid (Sample Size = {imAdvancedData['Total People']} Students)</div>
                          <div>Advanced Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve?</div>
                        </>
                      }
                    chartData={filteredIMAdvancedData} 
                    details={imInsightDetails}
                    total={imAdvancedData['Total People']}
                  />
            </div>
          </Grid>
          )
        }
        {Object.keys(filteredILAdvancedData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
            <div ref={(el) => { chartRefs.current[5] = el; }} style={{ backgroundColor: '#ffffff' }}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Intermediate Low (Sample Size = {ilAdvancedData['Total People']} Students)</div>
                          <div>Advanced Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve?</div>
                        </>
                      }
                    chartData={filteredILAdvancedData} 
                    details={ilInsightDetails}
                    total={ilAdvancedData['Total People']}
                  />
            </div>
          </Grid>
          )
        }
        {Object.keys(filteredNHIntermediateData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
              <div ref={(el) => { chartRefs.current[6] = el; }} style={{ backgroundColor: '#ffffff' }}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Novice High (Sample Size = {nhIntermediateData['Total People']} Students)</div>
                          <div>Intermediate Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve?</div>
                        </>
                      }
                    chartData={filteredNHIntermediateData} 
                    details={nhInsightDetails}
                    total={nhIntermediateData['Total People']}
                  />
              </div>
          </Grid>
          )
        }
        {Object.keys(filteredNMIntermediateData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
            <div ref={(el) => { chartRefs.current[7] = el; }} style={{ backgroundColor: '#ffffff' }}>            
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Novice Mid (Sample Size = {nmIntermediateData['Total People']} Students)</div>
                          <div>Intermediate Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve?</div>
                        </>
                      }
                    chartData={filteredNMIntermediateData} 
                    details={nmInsightDetails}
                    total={nmIntermediateData['Total People']}
                  />
            </div>
          </Grid>
          )
        }
        {Object.keys(filteredNLIntermediateData).length > 0 &&(
          <Grid item xs={6} md={8} lg={12} sx={{marginTop:"2vw"}}>
            <div ref={(el) => { chartRefs.current[8] = el; }} style={{ backgroundColor: '#ffffff' }}>
                  <DiagnosticGridReports
                    title={
                        <>
                          <div>{language} Novice Low (Sample Size = {nlIntermediateData['Total People']} Students)</div>
                          <div>Intermediate Diagnostic Grid</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve?</div>
                        </>
                      }
                    chartData={filteredNLIntermediateData} 
                    details={nlInsightDetails}
                    total={nlIntermediateData['Total People']}
                  />
            </div>
          </Grid>
          )
        }
      
      </>
      ) : (
        <Grid item xs={6} md={8} lg={12}>
          <Grid item sx={{marginTop:"2vw"}}>
          <div ref={(el) => { chartRefs.current[9] = el; }} style={{ backgroundColor: '#ffffff' }}>

                  <DiagnosticGroupChart
                    title={
                        <>
                          <div>
                            {language} (Sample Size = { 
                              (ahSuperiorData['Total People'] || 0) + (amSuperiorData['Total People'] || 0)
                            })
                          </div>
                          <div>Grouped Superior Diagnostic Grids</div>
                        </>
                      }
                    subheader={
                        <>
                          <div>What features do examinees need to improve?</div>
                        </>
                      }
                    testTypes={['Advanced High', 'Advanced Mid']}
                    chartData={[filteredAHSuperiorData, filteredAMSuperiorData]} 
                    details={nlInsightDetails}
                    total={(ahSuperiorData['Total People'] || 0) + (amSuperiorData['Total People'] || 0)}
                  />
          </div>
          </Grid>
          <Grid item sx={{marginTop:"2vw"}}>
            <div ref={(el) => { chartRefs.current[10] = el; }} style={{ backgroundColor: '#ffffff' }}>

                    <DiagnosticGroupChart
                      title={
                          <>
                            <div>{language} (Sample Size = {
                              (alAdvancedData['Total People'] || 0) + (ihAdvancedData['Total People'] || 0)
                              })
                            </div>
                            <div>Grouped Advanced Diagnostic Grids</div>
                          </>
                        }
                      subheader={
                          <>
                            <div>What features do examinees need to improve?</div>
                          </>
                        }
                      testTypes={['Advanced Low', 'Intermediate High']}
                      chartData={[filteredALAdvancedData, filteredIHAdvancedData]} 
                      details={nlInsightDetails}
                      total={(alAdvancedData['Total People'] || 0) + (ihAdvancedData['Total People'] || 0)
                      }
                    />
              </div>
              </Grid>
              <Grid item sx={{marginTop:"2vw"}}>
              <div ref={(el) => { chartRefs.current[11] = el; }} style={{ backgroundColor: '#ffffff' }}>

                      <DiagnosticGroupChart
                        title={
                            <>
                              <div>{language} (Sample Size = {
                                (imAdvancedData['Total People'] || 0) + (ilAdvancedData['Total People'] || 0) + (nhIntermediateData['Total People'] || 0)
                                })
                              </div>
                              <div>Grouped Intermediate Diagnostic Grids</div>
                            </>
                          }
                        subheader={
                            <>
                              <div>What features do examinees need to improve?</div>
                            </>
                          }
                        testTypes={['Intermediate Mid', 'Intermediate Low', 'Novice High']}
                        chartData={[filteredIMAdvancedData, filteredILAdvancedData, filteredNHIntermediateData]} 
                        details={nlInsightDetails}
                        total={(imAdvancedData['Total People'] || 0) + (ilAdvancedData['Total People'] || 0) + (nhIntermediateData['Total People'] || 0)}
                      />
              </div>

            </Grid>

          </Grid>

      )
      }
      </Grid>

        
      

    
    </>
  );
}      
