import React, { useState, useEffect, CSSProperties } from 'react';
import PulseLoader from "react-spinners/PulseLoader";
import { Helmet } from 'react-helmet-async';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { useTheme } from '@mui/material/styles';

import {
  Button,
  Container,
  Stack,
  Typography,
  Select,
  MenuItem,
  Checkbox,
  Grid
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

  const [selectedGraph, setSelectedGraph] = useState('Chart Type');
  const [scoreType, setScoreType] = useState('Score Type');
  const [userInput, setUserInput] = useState({});
  const [fromDate, setFromDate] = useState(new Date());
  const [toDate, setToDate] = useState(new Date());
  const [showGraph, setShowGraph] = useState(false);
  const [selectedData, setSelectedData] = useState(['Selected Data']);
  const [testDataLanguage, setTestDataLanguage] = useState(null);
  const [testDataScores, setTestDataScores] = useState(null);
  const [chartLabels, setChartLabels] = useState(['D', 'UR', 'NS', 'AR', 'NL', 'NM', 'NH', 'IL', 'IM', 'IH', 'AL', 'AM', 'AH', 'S']);
  const [reasons, setReasons] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate(); 

  const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
  const getLtiUrl = process.env.REACT_APP_LTI_URL;

  const handleGraphChange = (event) => {
    setSelectedGraph(event.target.value);
  };


  function countOccurrences(arr) {
    const counts = {};

    arr.forEach(item => {
      if (counts[item]) {
        counts[item]+= 1;
      } else {
        counts[item] = 1;
      }
    });

    return counts;
  }

  const handleUserInput = (event) => {
    // Update the userInput state based on user input (e.g., text fields)
    setUserInput({ ...userInput, [event.target.name]: event.target.value });
  };

  // Function to render the selected graph based on user input
  const handleGenerateReport = () => {
    // You can perform any necessary data fetching or processing here
    // For example, update the graph data based on user input
  
    // After data processing, set showGraph to true to render the graph
    setLoading(true);
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
          const response = await axios.post(getLtiUrl, {
            scoreType,
            fromDate,
            toDate,
            selectedData,
        }, {
            withCredentials: true,
            headers: {
              'X-CSRFToken': csrfToken,
              
            },
          });
          const testData = response.data;
            console.log('Test Data:', testData);
            const chartLabels = ['D', 'UR', 'NS', 'AR', 'NL', 'NM', 'NH', 'IL', 'IM', 'IH', 'AL', 'AM', 'AH', 'S'];

            const uniqueLanguages = [...new Set(testData.map((data) => data.language))];

            const scoreCounts = testData.reduce((accumulator, data) => {
              const { language, score } = data;
              if (!accumulator[language]) {
                accumulator[language] = {};
                chartLabels.forEach((label) => {
                  accumulator[language][label] = 0;
                });
              }
              accumulator[language][score] += 1;
              return accumulator;
            }, {});
            console.log('Unique Languages:', uniqueLanguages);
            console.log('Score Counts:', scoreCounts);
            setTestDataLanguage(uniqueLanguages);
            setTestDataScores(scoreCounts);
            console.log('Test Data:', testData);

            const reasons = testData.map(item => item.unit);
            const reasonCount = countOccurrences(reasons);
            const reasonLabelValuePairs = Object.entries(reasonCount).map(([label, value]) => ({ label, value }));
            setReasons(reasonLabelValuePairs.sort((a, b) => b.value - a.value));

            setShowGraph(true);
            setLoading(false);

  
        } else {
          console.log('Error');
        }
      } catch (error) {
        navigate('/login', { replace: true });
        console.log(error);
      }
    };
    fetchData();
  };
  
  const renderGraph = () => {
    if (showGraph) {
      if (selectedGraph === 'Radar Chart') {
        // Replace this with your actual OPI Scores graph component
        return <AppCurrentSubject
                title="Radar Chart"
                chartLabels={chartLabels}
                chartData={Object.keys(testDataScores).map(language => ({
                  name: language,
                  data: chartLabels.map(label => testDataScores[language][label] || 0),
                }))}
                chartColors={[...Array(6)].map(() => theme.palette.text.secondary)}
                />;
          
      }
       if (selectedGraph === 'Pie Chart') {

        return<AppCurrentVisits
              title="Reasons By Percentage"
              chartData={reasons}
              chartColors={[
                theme.palette.primary.main,
                theme.palette.info.main,
                theme.palette.warning.main,
                theme.palette.error.main,
              ]}
            />;
      }
      // Add more cases for other graph types as needed
    }
    return null; // or any other component to display when no graph is selected or after generating the report
  };

  return (
    <>
      <Helmet>
        <title> CLS Admin </title>
      </Helmet>

      <Container>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Typography variant="h4" gutterBottom>
            Generate Reports
          </Typography>
        </Stack>
        <div style={{ display: 'flex', alignItems: 'center' }}>
  <Select value={selectedGraph} onChange={handleGraphChange}>
    <MenuItem value="Radar Chart">Radar Chart</MenuItem>
    <MenuItem value="Pie Chart">Pie Chart</MenuItem>
  </Select>

  {selectedGraph === 'Radar Chart' && (
    <div style={{ display: 'flex', alignItems: 'center' }}>
      <Select value={scoreType} onChange={(event) => setScoreType(event.target.value)}>
        <MenuItem value="Score Type">Score Type</MenuItem>
        <MenuItem value="OPI">OPI</MenuItem>
        <MenuItem value="OPIc">OPIc</MenuItem>
        <MenuItem value="WPT">WPT</MenuItem>
      </Select>
      <DatePicker
        id="fromDate"
        selected={fromDate}
        onChange={(date) => setFromDate(date)}
        wrapperClassName="datePicker"
        showYearDropdown
      />
      <DatePicker
        id="toDate"
        selected={toDate}
        onChange={(date) => setToDate(date)}
        wrapperClassName="datePicker"
        showYearDropdown
        
      />
           <Select
              multiple
              value={selectedData}
              onChange={(event) => setSelectedData(event.target.value)}
              renderValue={() => 'Selected Data'}
            >
            {/* <MenuItem key='firstname' value='firstname'>
              <Checkbox checked={selectedData.includes('firstname')} />
              First Name
            </MenuItem>
            <MenuItem key='lastname' value='lastname'>
              <Checkbox checked={selectedData.includes('lastname')} />
              Last Name
            </MenuItem> */}
            <MenuItem key='score' value='score'>
              <Checkbox checked={selectedData.includes('score')} />
              Score
            </MenuItem>
            {/* <MenuItem key='major' value='major'>
              <Checkbox checked={selectedData.includes('major')} />
              Major
            </MenuItem> */}
            <MenuItem key='language' value='language'>
              <Checkbox checked={selectedData.includes('language')} />
              Language
            </MenuItem>
            </Select>
            <Button
              variant="contained"
              // startIcon={<Iconify icon="eva:plus-fill" />}
              onClick={handleGenerateReport}
              sx={{ padding: '0px !important', height: '48px', width: '110px' }}

            >
              <PulseLoader
              loading={loading}
              size={5}
              aria-label="Loading Spinner"
              data-testid="loader"
              sx={{ padding: '0px !important', height: 'inherit' }}
            />
              Generate Report
            </Button>
            
          </div>
  )}
  {selectedGraph === 'Pie Chart' && (
    <div style={{ display: 'flex', alignItems: 'center' }}>
      <Select value={scoreType} onChange={(event) => setScoreType(event.target.value)}>
        <MenuItem value="Score Type">Score Type</MenuItem>
        <MenuItem value="OPI">OPI</MenuItem>
        <MenuItem value="OPIc">OPIc</MenuItem>
        <MenuItem value="WPT">WPT</MenuItem>
      </Select>
      <DatePicker
        id="fromDate"
        selected={fromDate}
        onChange={(date) => setFromDate(date)}
        wrapperClassName="datePicker"
      />
      <DatePicker
        id="toDate"
        selected={toDate}
        onChange={(date) => setToDate(date)}
        wrapperClassName="datePicker"
      />
           <Select
              multiple
              value={selectedData}
              onChange={(event) => setSelectedData(event.target.value)}
              renderValue={() => 'Selected Data'}
            >
            {/* <MenuItem key='firstname' value='firstname'>
              <Checkbox checked={selectedData.includes('firstname')} />
              First Name
            </MenuItem>
            <MenuItem key='lastname' value='lastname'>
              <Checkbox checked={selectedData.includes('lastname')} />
              Last Name
            </MenuItem>
            <MenuItem key='score' value='score'>
              <Checkbox checked={selectedData.includes('score')} />
              Score
            </MenuItem> */}
            <MenuItem key='unit' value='unit'>
              <Checkbox checked={selectedData.includes('unit')} />
              Reason
            </MenuItem>
            {/* <MenuItem key='major' value='major'>
              <Checkbox checked={selectedData.includes('major')} />
              Major
            </MenuItem>
            <MenuItem key='language' value='language'>
              <Checkbox checked={selectedData.includes('language')} />
              Language
            </MenuItem> */}
            </Select>
            <Button
              variant="contained"
              onClick={handleGenerateReport}
            >
            <PulseLoader
              loading={loading}
              size={5}
              aria-label="Loading Spinner"
              data-testid="loader"
              sx={{ padding: '0px !important', height: 'inherit' }}
            />
              Generate Report
            </Button>
          </div>
          )}
</div>

        {/* Graph Selection Dropdown */}
        

        {/* Render the selected graph */}
        {renderGraph()}
        
      </Container>
    </>
  );
}
