import { Helmet } from 'react-helmet-async';
import { faker } from '@faker-js/faker';
// @mui
import { useTheme } from '@mui/material/styles';
import { Grid, Container, Typography } from '@mui/material';
// components
import Cookies from 'js-cookie'; // Import the js-cookie library
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { set } from 'lodash';

import Iconify from '../components/iconify';
// sections
import {
  AppTasks,
  AppNewsUpdate,
  AppOrderTimeline,
  AppCurrentVisits,
  AppWebsiteVisits,
  AppTrafficBySite,
  AppWidgetSummary,
  AppCurrentSubject,
  AppConversionRates,
} from '../sections/@dashboard/app';

// ----------------------------------------------------------------------

export default function DashboardAppPage() {
  const [data, setData] = useState(null);
  const [entryDates, setEntryDates] = useState(null);
  const [userCount, setUserCount] = useState(null);
  const [dateData, setDateData] = useState(null);
  const [notApprovedCount, setNotApprovedCount] = useState(null);
  const [studentsPending, setStudentsPending] = useState(null);
  const [cancelStudents, setCancelStudents] = useState(null);
  const [languageCount, setLanguageCount] = useState(null);
  const [reasons, setReasons] = useState(null);
  const [spanishScores, setSpanishScores] = useState(null);
  const [chineseScores, setChineseScores] = useState(null);
  const [koreanScores, setKoreanScores] = useState(null);
  const [japaneseScores, setJapaneseScores] = useState(null);
  const [frenchScores, setFrenchScores] = useState(null);
  const [germanScores, setGermanScores] = useState(null);
  const [portScores, setPortScores] = useState(null);
  const [russianScores, setRussianScores] = useState(null);
  const [spanishTimeCount, setSpanishTimeCount] = useState(null);
  const [chineseTimeCount, setChineseTimeCount] = useState(null);
  const [koreanTimeCount, setKoreanTimeCount] = useState(null);
  const [japaneseTimeCount, setJapaneseTimeCount] = useState(null);
  const [frenchTimeCount, setFrenchTimeCount] = useState(null);
  const [germanTimeCount, setGermanTimeCount] = useState(null);
  const [portTimeCount, setPortTimeCount] = useState(null);
  const [russianTimeCount, setRussianTimeCount] = useState(null);
  const [testDataLanguage, setTestDataLanguage] = useState(null);
  const [testDataScores, setTestDataScores] = useState(null);
  const [ltiChartLabels, setLtiChartLabels] = useState(['D', 'UR', 'NS', 'AR', 'NL', 'NM', 'NH', 'IL', 'IM', 'IH', 'AL', 'AM', 'AH', 'S']);
  const theme = useTheme();
  const navigate = useNavigate();

  const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
  const filemakerUrl = process.env.REACT_APP_FILEMAKER_URL;


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

  function roundTimeAndSubtractHours(time, subtractHours) {
    const [initialHours, minutes, seconds] = time.split(':').map(Number);
    let hours = initialHours; // Use a different variable to store the updated hours
    
    if (minutes >= 30 || (minutes === 30 && seconds > 0)) {
      hours = (hours + 1) % 24; // Handle wrapping to the next day
    }
    
    // Subtract the specified number of hours
    hours -= subtractHours;
    
    // Handle negative hours by wrapping to the previous day
    if (hours < 0) {
      hours = 24 + hours;
    }
    
    return hours;
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(filemakerUrl, {
          withCredentials: true,
          headers: {
          },
        });
        console.log(response);
        if (response.status === 401 || response.status === 403) {
          navigate('/cls/login', { replace: true });
        }
        const fetchedData = response.data;
        setData(fetchedData);

        let notApprovedCount = fetchedData.response.data.filter((item) => item.fieldData.Approved === 'No').length;
        if (notApprovedCount === 0) {
          notApprovedCount = '0';
        }
        setNotApprovedCount(notApprovedCount);

        let studentsPending = fetchedData.response.data.filter((item) => item.fieldData.Approved === 'Pending').length;
        if (studentsPending === 0) {
          studentsPending = '0';
        }
        setStudentsPending(studentsPending);


        const userCount = fetchedData.response.data.length;
        setUserCount(userCount);

        const languages = fetchedData.response.data.map(item => item.fieldData.Language);
        const languageCount = countOccurrences(languages);
        const labelValuePairs = Object.entries(languageCount).map(([label, value]) => ({ label, value }));

        setLanguageCount(labelValuePairs.sort((a, b) => b.value - a.value)); 
        
        const reasons = fetchedData.response.data.map(item => item.fieldData.Reason);
        const reasonCount = countOccurrences(reasons);
        const reasonLabelValuePairs = Object.entries(reasonCount).map(([label, value]) => ({ label, value }));
        setReasons(reasonLabelValuePairs.sort((a, b) => b.value - a.value));
        
        const chartLabels = ['D', 'NL', 'NM', 'NH', 'IL', 'IM', 'IH', 'AL', 'AM', 'AH', 'S'];

        const spanishScores = fetchedData.response.data.filter((item) => item.fieldData.Language === 'SPAN').map(item => item.fieldData.Scores);
        const spanishScoreCount = countOccurrences(spanishScores);
        const spanishScoreLabelValuePairs = chartLabels.map(label => ({label,value: spanishScoreCount[label] || 0,}));
        setSpanishScores(spanishScoreLabelValuePairs);

        const chineseScores = fetchedData.response.data.filter((item) => item.fieldData.Language === 'CHIN').map(item => item.fieldData.Scores);
        const chineseScoreCount = countOccurrences(chineseScores);
        const chineseScoreLabelValuePairs = chartLabels.map(label => ({label,value: chineseScoreCount[label] || 0,}));        
        setChineseScores(chineseScoreLabelValuePairs);

        const koreanScores = fetchedData.response.data.filter((item) => item.fieldData.Language === 'KOREA').map(item => item.fieldData.Scores);
        const koreanScoreCount = countOccurrences(koreanScores);
        const koreanScoreLabelValuePairs = chartLabels.map(label => ({label,value: koreanScoreCount[label] || 0,}));
        setKoreanScores(koreanScoreLabelValuePairs);

        const japaneseScores = fetchedData.response.data.filter((item) => item.fieldData.Language === 'JAPAN').map(item => item.fieldData.Scores);
        const japaneseScoreCount = countOccurrences(japaneseScores);
        const japaneseScoreLabelValuePairs = chartLabels.map(label => ({label,value: japaneseScoreCount[label] || 0,}));
        setJapaneseScores(japaneseScoreLabelValuePairs);

        const frenchScores = fetchedData.response.data.filter((item) => item.fieldData.Language === 'FREN').map(item => item.fieldData.Scores);
        const frenchScoreCount = countOccurrences(frenchScores);
        const frenchScoreLabelValuePairs = chartLabels.map(label => ({label,value: frenchScoreCount[label] || 0,}));
        setFrenchScores(frenchScoreLabelValuePairs);

        const germanScores = fetchedData.response.data.filter((item) => item.fieldData.Language === 'GERM').map(item => item.fieldData.Scores);
        const germanScoreCount = countOccurrences(germanScores);
        const germanScoreLabelValuePairs = chartLabels.map(label => ({label,value: germanScoreCount[label] || 0,}));
        setGermanScores(germanScoreLabelValuePairs);

        const portScores = fetchedData.response.data.filter((item) => item.fieldData.Language === 'PORT').map(item => item.fieldData.Scores);
        const portScoreCount = countOccurrences(portScores);
        const portScoreLabelValuePairs = chartLabels.map(label => ({label,value: portScoreCount[label] || 0,}));
        setPortScores(portScoreLabelValuePairs);

        const russianScores = fetchedData.response.data.filter((item) => item.fieldData.Language === 'RUSS').map(item => item.fieldData.Scores);
        const russianScoreCount = countOccurrences(russianScores);
        const russianScoreLabelValuePairs = chartLabels.map(label => ({label,value: russianScoreCount[label] || 0,}));
        setRussianScores(russianScoreLabelValuePairs);

        const subtractedHours = 2;

        const spanishTimes = fetchedData.response.data.filter((item) => item.fieldData.Language === 'SPAN').map(item => item.fieldData.EntryTime);
        const roundedAndSubtractedTimes = spanishTimes.map(time => {
        const roundedHour = roundTimeAndSubtractHours(time, subtractedHours);return `${roundedHour.toString().padStart(2, '0')}`;});
        const spanishCount = countOccurrences(roundedAndSubtractedTimes);
        const hourlyCounts = Array(24).fill(0);
        
        Object.entries(spanishCount).forEach(([label, value]) => {const hour = parseInt(label, 10);hourlyCounts[hour] = value;});
                
        const sortedSpanishTimeCount = [...hourlyCounts];
        setSpanishTimeCount(sortedSpanishTimeCount);

        const chineseTimes = fetchedData.response.data.filter((item) => item.fieldData.Language === 'CHIN').map(item => item.fieldData.EntryTime);
        const roundedAndSubtractedChineseTimes = chineseTimes.map(time => {const roundedHour = roundTimeAndSubtractHours(time, subtractedHours);return `${roundedHour.toString().padStart(2, '0')}`;});
        const chineseCount = countOccurrences(roundedAndSubtractedChineseTimes);
        const chineseHourlyCounts = Array(24).fill(0);

        Object.entries(chineseCount).forEach(([label, value]) => {const hour = parseInt(label, 10);chineseHourlyCounts[hour] = value;});

        const sortedChineseTimeCount = [...chineseHourlyCounts];
        setChineseTimeCount(sortedChineseTimeCount);

        const koreanTimes = fetchedData.response.data.filter((item) => item.fieldData.Language === 'KOREA').map(item => item.fieldData.EntryTime);
        const roundedAndSubtractedKoreanTimes = koreanTimes.map(time => {const roundedHour = roundTimeAndSubtractHours(time, subtractedHours);return `${roundedHour.toString().padStart(2, '0')}`;});
        const koreanCount = countOccurrences(roundedAndSubtractedKoreanTimes);
        const koreanHourlyCounts = Array(24).fill(0);

        Object.entries(koreanCount).forEach(([label, value]) => {const hour = parseInt(label, 10);koreanHourlyCounts[hour] = value;});

        const sortedKoreanTimeCount = [...koreanHourlyCounts];
        setKoreanTimeCount(sortedKoreanTimeCount);

        const japaneseTimes = fetchedData.response.data.filter((item) => item.fieldData.Language === 'JAPAN').map(item => item.fieldData.EntryTime);
        const roundedAndSubtractedJapaneseTimes = japaneseTimes.map(time => {const roundedHour = roundTimeAndSubtractHours(time, subtractedHours);return `${roundedHour.toString().padStart(2, '0')}`;});
        const japaneseCount = countOccurrences(roundedAndSubtractedJapaneseTimes);
        const japaneseHourlyCounts = Array(24).fill(0);

        Object.entries(japaneseCount).forEach(([label, value]) => {const hour = parseInt(label, 10);japaneseHourlyCounts[hour] = value;});

        const sortedJapaneseTimeCount = [...japaneseHourlyCounts];
        setJapaneseTimeCount(sortedJapaneseTimeCount);

        const frenchTimes = fetchedData.response.data.filter((item) => item.fieldData.Language === 'FREN').map(item => item.fieldData.EntryTime);
        const roundedAndSubtractedFrenchTimes = frenchTimes.map(time => {const roundedHour = roundTimeAndSubtractHours(time, subtractedHours);return `${roundedHour.toString().padStart(2, '0')}`;});
        const frenchCount = countOccurrences(roundedAndSubtractedFrenchTimes);
        const frenchHourlyCounts = Array(24).fill(0);

        Object.entries(frenchCount).forEach(([label, value]) => {const hour = parseInt(label, 10);frenchHourlyCounts[hour] = value;});  

        const sortedFrenchTimeCount = [...frenchHourlyCounts];
        setFrenchTimeCount(sortedFrenchTimeCount);

        const germanTimes = fetchedData.response.data.filter((item) => item.fieldData.Language === 'GERM').map(item => item.fieldData.EntryTime);
        const roundedAndSubtractedGermanTimes = germanTimes.map(time => {const roundedHour = roundTimeAndSubtractHours(time, subtractedHours);return `${roundedHour.toString().padStart(2, '0')}`;});
        const germanCount = countOccurrences(roundedAndSubtractedGermanTimes);
        const germanHourlyCounts = Array(24).fill(0);

        Object.entries(germanCount).forEach(([label, value]) => {const hour = parseInt(label, 10);germanHourlyCounts[hour] = value;});

        const sortedGermanTimeCount = [...germanHourlyCounts];
        setGermanTimeCount(sortedGermanTimeCount);

        const portTimes = fetchedData.response.data.filter((item) => item.fieldData.Language === 'PORT').map(item => item.fieldData.EntryTime);
        const roundedAndSubtractedPortTimes = portTimes.map(time => {const roundedHour = roundTimeAndSubtractHours(time, subtractedHours);return `${roundedHour.toString().padStart(2, '0')}`;});
        const portCount = countOccurrences(roundedAndSubtractedPortTimes);
        const portHourlyCounts = Array(24).fill(0);

        Object.entries(portCount).forEach(([label, value]) => {const hour = parseInt(label, 10);portHourlyCounts[hour] = value;});

        const sortedPortTimeCount = [...portHourlyCounts];
        setPortTimeCount(sortedPortTimeCount);

        const russianTimes = fetchedData.response.data.filter((item) => item.fieldData.Language === 'RUSS').map(item => item.fieldData.EntryTime);
        const roundedAndSubtractedRussianTimes = russianTimes.map(time => {const roundedHour = roundTimeAndSubtractHours(time, subtractedHours);return `${roundedHour.toString().padStart(2, '0')}`;});
        const russianCount = countOccurrences(roundedAndSubtractedRussianTimes);
        const russianHourlyCounts = Array(24).fill(0);

        Object.entries(russianCount).forEach(([label, value]) => {const hour = parseInt(label, 10);russianHourlyCounts[hour] = value;});

        const sortedRussianTimeCount = [...russianHourlyCounts];
        setRussianTimeCount(sortedRussianTimeCount);
    
        
        const entryDates = fetchedData.response.data.map(item => item.fieldData.EntryDate);

        const currentDate = new Date();
        const oneDayFromNow = new Date();
        oneDayFromNow.setDate(currentDate.getDate() + 1);
        
        const twoDaysFromNow = new Date();
        twoDaysFromNow.setDate(currentDate.getDate() + 2);
        
        const threeDaysFromNow = new Date();
        threeDaysFromNow.setDate(currentDate.getDate() + 3);
        
        // Format these dates as "MM/DD/YYYY"
        const formatDate = (date) => {
          const mm = String(date.getMonth() + 1).padStart(2, '0');
          const dd = String(date.getDate()).padStart(2, '0');
          const yyyy = date.getFullYear();
          return `${mm}/${dd}/${yyyy}`;
        };
        
        const oneDayFormatted = formatDate(oneDayFromNow);
        const twoDaysFormatted = formatDate(twoDaysFromNow);
        const threeDaysFormatted = formatDate(threeDaysFromNow);
        
        // Filter the data based on the formatted dates
        const cancelStudentsArray = fetchedData.response.data.filter((item) => {
          const testDate = item.fieldData.LTISchedule.split('&')[0]
          const isPending = item.fieldData.Approved === "Pending"; // Extract "MM/DD/YYYY" from "MM/DD/YYYY&hh:mm AM/PM"
          return (
            (testDate === oneDayFormatted ||
            testDate === twoDaysFormatted ||
            testDate === threeDaysFormatted) &&
            isPending
          );
        });
        
        let cancelStudents = '0';

        if (cancelStudentsArray.length !== 0) {
          cancelStudents = cancelStudentsArray.length;
        }
        
        setCancelStudents(cancelStudents);
   
        const dateCounts = countOccurrences(entryDates);

        const isValidDate = (date) => {
            const timestamp = Date.parse(date);
            return !Number.isNaN(timestamp);
        };

        const sortedDateCounts = Object.keys(dateCounts)
            .filter(date => date.trim() !== "" && isValidDate(date)) // Use the custom function
            .sort((date1, date2) => new Date(date1) - new Date(date2))
            .reduce((acc, key) => {
                acc[key] = dateCounts[key];
                return acc;
            }, {});



        const keysArray = Object.keys(sortedDateCounts);
        const uniqueKeys = new Set(keysArray);
        const uniqueKeysArray = Array.from(uniqueKeys);
        setEntryDates(uniqueKeysArray);

        const valuesArray = Object.values(sortedDateCounts);
        setDateData(valuesArray);
      } catch (error) {
        console.error('Error fetching data:', error);
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
          navigate('/cls/login', { replace: true })};
          
      }
    };

    fetchData();
  }, []);
  if (!dateData) {
    // Render a loading indicator or null while dateData is not available
    return null;
  }
  return (
    <>
      <Helmet >
        <title> Admin </title>
      </Helmet>
      <Container maxWidth="xl">

        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <AppWidgetSummary title="Total Submissions" total={userCount ?? 0}/>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <AppWidgetSummary title="Student(s) Awaiting Approval" total={notApprovedCount ?? 0} color="info"/>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <AppWidgetSummary title="Student(s) Pending" total={studentsPending ?? 0} color="warning"/>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
              <AppWidgetSummary title="Potential Tests to Cancel" total={cancelStudents ?? 0} color="error"/>
          </Grid>

          <Grid item xs={12} md={10} lg={12}>
            <AppWebsiteVisits
              title="Student Requests"
              subheader={`Since ${entryDates[0]}`}              
              chartLabels= {entryDates}
              chartData={[
                {
                  name: 'Student Requests',
                  type: 'line',
                  fill: 'solid',
                  data: dateData,
                },
              ]}
            />
          </Grid>

          <Grid item xs={16} md={10} lg={6}>
            <AppCurrentVisits
              title="Languages By Percentage"
              chartData={languageCount}
              chartColors={[
                theme.palette.primary.main,
                theme.palette.info.main,
                theme.palette.warning.main,
                theme.palette.error.main,
              ]}
            />
          </Grid>

          <Grid item xs={16} md={10} lg={6}>
            <AppCurrentVisits
              title="Reasons By Percentage"
              chartData={reasons}
              chartColors={[
                theme.palette.primary.main,
                theme.palette.info.main,
                theme.palette.warning.main,
                theme.palette.error.main,
              ]}
            />
          </Grid>

          <Grid item xs={12} md={10} lg={12}>
            <AppConversionRates
              title="Languages Ranked"
              // subheader="(+43%) than last year"
              chartData={languageCount} 
            />
          </Grid>

          <Grid item xs={12} md={10} lg={12}>
          <AppCurrentSubject
            title="When Are Students Registering For Tests?"
            chartLabels={[
              '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
              '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'
            ]}
            chartData={[
              { name: 'Spanish', data: spanishTimeCount },
              { name: 'Chinese', data: chineseTimeCount },
              { name: 'Korean', data: koreanTimeCount },
              { name: 'Japanese', data: japaneseTimeCount },
              { name: 'French', data: frenchTimeCount },
              { name: 'German', data: germanTimeCount },
              { name: 'Portuguese', data: portTimeCount },
              { name: 'Russian', data: russianTimeCount },
            ]}
        chartColors={[...Array(6)].map(() => theme.palette.text.secondary)}
          />
        </Grid>

        <Grid item xs={12} md={10} lg={12}>
          <AppCurrentSubject
            title="OPI Scores"
            chartLabels={[
              'D', 'NL', 'NM', 'NH', 'IL', 'IM', 'IH', 'AL', 'AM', 'AH', 'S'
            ]}
            chartData={[
              { name: 'Spanish', data: spanishScores.map(item => item.value) },
              { name: 'Chinese', data: chineseScores.map(item => item.value) },
              { name: 'Korean', data: koreanScores.map(item => item.value) },
              { name: 'Japanese', data: japaneseScores.map(item => item.value) },
              { name: 'French', data: frenchScores.map(item => item.value) },
              { name: 'German', data: germanScores.map(item => item.value) },
              { name: 'Portuguese', data: portScores.map(item => item.value) },
              { name: 'Russian', data: russianScores.map(item => item.value) },
            ]}
                    chartColors={[...Array(6)].map(() => theme.palette.text.secondary)}
                  />
        </Grid>

        {/* <Grid item xs={12} md={10} lg={12}>
          <AppCurrentSubject
            title="OPI Scores Version 2"
            chartLabels={ltiChartLabels}
            chartData={Object.keys(testDataScores).map(language => ({
              name: language,
              data: ltiChartLabels.map(label => testDataScores[language][label] || 0),
            }))}
            chartColors={[...Array(6)].map(() => theme.palette.text.secondary)}
            />
        </Grid> */}

          {/* <Grid item xs={12} md={6} lg={8}>
            <AppNewsUpdate
              title="News Update"
              list={[...Array(5)].map((_, index) => ({
                id: faker.datatype.uuid(),
                title: faker.name.jobTitle(),
                description: faker.name.jobTitle(),
                image: `/assets/images/covers/cover_${index + 1}.jpg`,
                postedAt: faker.date.recent(),
              }))}
            />
          </Grid>

          <Grid item xs={12} md={6} lg={4}>
            <AppOrderTimeline
              title="Order Timeline"
              list={[...Array(5)].map((_, index) => ({
                id: faker.datatype.uuid(),
                title: [
                  '1983, orders, $4220',
                  '12 Invoices have been paid',
                  'Order #37745 from September',
                  'New order placed #XF-2356',
                  'New order placed #XF-2346',
                ][index],
                type: `order${index + 1}`,
                time: faker.date.past(),
              }))}
            />
          </Grid>

          <Grid item xs={12} md={6} lg={4}>
            <AppTrafficBySite
              title="Traffic by Site"
              list={[
                {
                  name: 'FaceBook',
                  value: 323234,
                  icon: <Iconify icon={'eva:facebook-fill'} color="#1877F2" width={32} />,
                },
                {
                  name: 'Google',
                  value: 341212,
                  icon: <Iconify icon={'eva:google-fill'} color="#DF3E30" width={32} />,
                },
                {
                  name: 'Linkedin',
                  value: 411213,
                  icon: <Iconify icon={'eva:linkedin-fill'} color="#006097" width={32} />,
                },
                {
                  name: 'Twitter',
                  value: 443232,
                  icon: <Iconify icon={'eva:twitter-fill'} color="#1C9CEA" width={32} />,
                },
              ]}
            />
          </Grid>

          <Grid item xs={12} md={6} lg={8}>
            <AppTasks
              title="Tasks"
              list={[
                { id: '1', label: 'Create FireStone Logo' },
                { id: '2', label: 'Add SCSS and JS files if required' },
                { id: '3', label: 'Stakeholder Meeting' },
                { id: '4', label: 'Scoping & Estimations' },
                { id: '5', label: 'Sprint Showcase' },
              ]}
            />
          </Grid> */}
        </Grid>
      </Container>
    </>
  );
}
