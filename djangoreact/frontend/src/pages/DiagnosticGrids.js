import { Helmet } from 'react-helmet-async';
import { filter, set } from 'lodash';
import { sentenceCase } from 'change-case';
import { useEffect, useState } from 'react';
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
  Typography,
  TextField,
  InputLabel,
  MenuItem

} from '@mui/material';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { DateRangePicker } from '@mui/x-date-pickers-pro/DateRangePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
// components
import { is } from 'date-fns/locale';
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
  const filemakerUrl = process.env.REACT_APP_FILEMAKER_URL;

  const [age, setAge] = useState('');

  const handleChange = (event) => {
    setAge(event.target.value);
  };


  useEffect(() => {
    const fetchData = async () => {
          try {
            console.log('hi')


      } catch (error) {
        // navigate('/cls/login', { replace: true });
        console.log(error);
      }
    };
    fetchData();
    }, []);
      
  return (
    <>
      <Helmet>
        <title> CLS Admin </title>
      </Helmet>

      <Container>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Typography variant="h4" gutterBottom>
            Diagnostic Grids
          </Typography>
          <Button variant="contained" startIcon={<Iconify icon="eva:plus-fill" />}>
            New User
          </Button>
          
          </Stack>

        <Card>
          <InputLabel id="demo-simple-select-label">Language</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={age}
                    label="Age"
                    onChange={handleChange}
                >
                    <MenuItem value={10}>Ten</MenuItem>
                    <MenuItem value={20}>Twenty</MenuItem>
                    <MenuItem value={30}>Thirty</MenuItem>
                </Select>

            <InputLabel id="demo-simple-select-label">Program Type</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={age}
                    label="Age"
                    onChange={handleChange}
                >
                    <MenuItem value={10}>Ten</MenuItem>
                    <MenuItem value={20}>Twenty</MenuItem>
                    <MenuItem value={30}>Thirty</MenuItem>
                </Select>

                <LocalizationProvider dateAdapter={AdapterDayjs}>
                <InputLabel id="demo-simple-select-label">Date Range</InputLabel>

                    <DateRangePicker
                        localeText={{
                        start: '',
                        end: '',
                        }}
                    />
                </LocalizationProvider>
        </Card>
      </Container>

    

    
    </>
  );
}      
