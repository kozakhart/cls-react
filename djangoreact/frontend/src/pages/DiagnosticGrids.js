import { Helmet } from 'react-helmet-async';
import { filter, set } from 'lodash';
import { sentenceCase } from 'change-case';
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
  Box

} from '@mui/material';

import Select, { SelectChangeEvent } from '@mui/material/Select';
// components
import { format, parseISO } from 'date-fns';

import DatePicker from 'react-datepicker';

import { is } from 'date-fns/locale';
import { DiagnosticGridReports } from '../sections/@dashboard/app';
import LoadingModal from '../components/loadingModal/LoadingModal';

import EditableCell from '../components/editablecell/EditableCell';

import UpdateNotification from '../components/updatenotification/UpdateNotification';
import DeleteNotification from '../components/deletenotification/DeleteNotification';

import Label from '../components/label';
import Iconify from '../components/iconify';
import Scrollbar from '../components/scrollbar';
// sections

import { UserListHead, UserListToolbar } from '../sections/@dashboard/user';
// mock

// ----------------------------------------------------------------------

export default function DiagnosticGrids() {
  const navigate = useNavigate();

  const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
  const diagnosticGridsUrl = process.env.REACT_APP_DIAGNOSTIC_GRIDS_URL;

  const today = new Date();
  const oneYearFromToday = new Date();
  oneYearFromToday.setFullYear(today.getFullYear() - 1);

  const [startDate, setStartDate] = useState(oneYearFromToday);
  const [endDate, setEndDate] = useState(new Date());
  const [language, setLanguage] = useState('All');
  const [programType, setProgramType] = useState('10');
  const [masterLoader, setMasterLoader] = useState(false);

  const [superiorData, setSuperiorData] = useState({});
  const [advancedData, setAdvancedData] = useState({});

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };
  const handleProgramChange = (event) => {
    setProgramType(event.target.value);
  };


  useEffect(() => {
    const fetchData = async () => {
          try {
            console.log('get languages from backend')


      } catch (error) {
        navigate('/cls/login', { replace: true });
        console.log(error);
      }
    };
    fetchData();
    }, []);
      
    const sendInfo = async () => {
      try {
        setMasterLoader(true);
        const csrfToken = Cookies.get('csrftoken');
        const formattedStartDate = format(startDate, 'MM/dd/yyyy');
        const formattedEndDate = format(endDate, 'MM/dd/yyyy');

        const bodyParameters = {
          language,
          programType,
          fromDate: formattedStartDate,
          toDate: formattedEndDate
        };
        const response = await axios.post(
          diagnosticGridsUrl,
          bodyParameters,
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': csrfToken,
              
            }
          }
        );
        console.log(response.data);
        setSuperiorData(response.data.superior_grid_results);
        console.log(response.data.advanced_grid_results);
        setAdvancedData(response.data.advanced_grid_results);
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

      <Container>

        <Card sx={{width: "40%", marginLeft:"20%", border: "3px solid #002e5d"}}>
          <Typography variant="h4" gutterBottom sx={{marginLeft:"30%", marginTop:"1vw"}}>
            Diagnostic Grids
          </Typography>
          
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
                      <MenuItem value="All">All</MenuItem>
                      <MenuItem value="Spanish">Spanish</MenuItem>
                      <MenuItem value="German">German</MenuItem>
                      <MenuItem value="Russian">Russian</MenuItem>
                  </Select>
          </Stack>
          <Stack direction="column" sx={{padding:'1vw'}}>
            <InputLabel id="demo-simple-select-label">Program Type</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={programType}
                    label="Program"
                    onChange={handleProgramChange}
                    sx={{width: "60%"}}
                >
                    <MenuItem value={10}>Ten</MenuItem>
                    <MenuItem value={20}>Twenty</MenuItem>
                    <MenuItem value={30}>Thirty</MenuItem>
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
                <Button variant="contained" startIcon={<Iconify icon="eva:arrow-circle-down-outline" />} onClick={sendInfo}>
                    Generate Reports
              </Button>
          </Stack>
        </Card>
        <LoadingModal isLoading={masterLoader} message="Retrieving data... Please wait..."/>
        {Object.keys(superiorData).length > 0 &&(
          <Grid item xs={12} md={10} lg={12}>
                  <DiagnosticGridReports
                    title="Superior Functions"
                    // subheader="(+43%) than last year"
                    chartData={superiorData} 
                  />
          </Grid>
          )
        }
        {Object.keys(advancedData).length > 0 &&(
          <Grid item xs={12} md={10} lg={12}>
                  <DiagnosticGridReports
                    title="Advanced Functions"
                    // subheader="(+43%) than last year"
                    chartData={advancedData} 
                  />
          </Grid>
          )
        }

      </Container>

    

    
    </>
  );
}      
