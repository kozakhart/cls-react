import { Helmet } from 'react-helmet-async';
import { filter, set } from 'lodash';
import { sentenceCase } from 'change-case';
import { useEffect, useState } from 'react';
import PulseLoader from "react-spinners/PulseLoader";
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
// @mui
import '../theme/style.css'
import {
  Card,
  Table,
  Stack,
  Paper,
  Button,
  Popover,
  Checkbox,
  TableRow,
  MenuItem,
  TableBody,
  TableCell,
  Container,
  Typography,
  IconButton,
  TableContainer,
  TablePagination,
  Tooltip,
  TextField,
} from '@mui/material';
// components
import { is } from 'date-fns/locale';
import { format } from 'date-fns';

import DatePicker from "react-datepicker";
import EditableCell from '../components/editablecell/EditableCell';

import UpdateNotification from '../components/updatenotification/UpdateNotification';
import DeleteNotification from '../components/deletenotification/DeleteNotification';
import AwardCertificate from '../components/awardcertificate/AwardCertificate';

import Label from '../components/label';
import Iconify from '../components/iconify';
import Scrollbar from '../components/scrollbar';
// sections
import { UserListHead, UserListToolbar } from '../sections/@dashboard/needsapproval';

const TABLE_HEAD = [
  { id: 'name', label: 'Name', alignRight: false },
  { id: 'byuidtable', label: 'BYU ID', alignRight: false},
  { id: 'languagetable', label: 'Language', alignRight: false },
  { id: 'reason', label: 'Reason', alignRight: false},
  { id: 'level', label: 'Level', alignRight: false },
  { id: 'opi', label: 'OPI', alignRight: false },
  { id: 'wpt', label: 'WPT', alignRight: false },
  { id: 'opic', label: 'OPIc', alignRight: false },
  { id: 'award', label: 'Award', alignRight: false },
];

// ----------------------------------------------------------------------

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function applySortFilter(studentdata, comparator, query) {
  const stabilizedThis = studentdata.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  if (query && /\d/.test(query)) {
    // If query is a number, perform numeric comparison
    return studentdata.filter((student) =>
      (`${student.fieldData.BYUID} ${student.recordId}`).includes(query)
    );
  }
  if (query) {
    console.log('query:', query, studentdata);
    // return array.filter((name) => name.toLowerCase().indexOf(query.toLowerCase()) !== -1);
    return studentdata.filter((student) =>
      (`${student.fieldData.FirstName.toLowerCase()} ${student.fieldData.LastName.toLowerCase()} ${student.fieldData.Language.toLowerCase()}`).includes(query.toLowerCase())
    );
  }
  return stabilizedThis.map((el) => el[0]);
}

export default function UserPage() {
  const [studentdata, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isChecked, setIsChecked] = useState(false);
  const [userList, setUserList] = useState([]);
  const [recordDate, setrecordDate] = useState(new Date());
  const [semesterDate, setsemesterDate] = useState(new Date());
  const [todaysDate, setTodaysDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [isPopoverOpen, setPopoverOpen] = useState(false);
  const [isPopoverCustomOpen, setPopoverCustomOpen] = useState(false);
  const [byuidValue, setByuidValue] = useState('None');
  const [languageValue, setLanguageValue] = useState('None');
  const [fullnameValue, setfullnameValue] = useState('');
  const [netidValue, setnetidValue] = useState('');

  const [open, setOpen] = useState(null);

  const [page, setPage] = useState(0);

  const [order, setOrder] = useState('asc');

  const [selected, setSelected] = useState([]);

  const [orderBy, setOrderBy] = useState('name');

  const [filterName, setFilterName] = useState('');

  const [rowsPerPage, setRowsPerPage] = useState(10);
  const navigate = useNavigate();

  const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
  const getCertificateDataUrl = process.env.REACT_APP_CERTIFICATE_DATA_URL;

  useEffect(() => {
    const getFormattedDate = () => {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0'); // Adding 1 because January is 0
      const day = String(today.getDate()).padStart(2, '0');
      return `${month}/${day}/${year}`;
    };

    setTodaysDate(getFormattedDate());
  }, []);
  const handleOpenMenu = (event) => {
    setOpen(event.currentTarget);
  };

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleSelectAllClick = (event) => {
    if (event.target.checked) {
      console.log('userList:', userList);
      const newSelecteds = userList.map((n) => n);
      setSelected(newSelecteds);
      console.log('newSelecteds:', newSelecteds); 
      return;
    }
    setSelected([]);
  };

  const handleCheckboxClick = (event, recordId) => {
    const selectedIndex = selected.indexOf(recordId);
    let newSelected = [];
    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, recordId);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(selected.slice(0, selectedIndex), selected.slice(selectedIndex + 1));
    }
    setSelected(newSelected);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setPage(0);
    setRowsPerPage(parseInt(event.target.value, 10));
  };

  const handleFilterByName = (event) => {
    setPage(0);
    setFilterName(event.target.value);
    return console.log('event.target.value:', event.target.value);

  };


  function UserTableRow({ user, handleCheckboxClick, handleOpenMenu }) {
    // console.log(user)
    const { recordId, firstname, lastname, byuid, netid, language, reason, level, opiScore, opiDate, wptScore, wptDate, opicScore, opicDate 
    } = user;
    const fullname = `${firstname} ${lastname}`;
    // console.log('recordId:', recordId);
    // const selectedUser = user.selected;
    const selectedUser = selected.indexOf(recordId) !== -1;

    const [isPopoverOpen, setPopoverOpen] = useState(false);
    const getNestedKey = (obj) => {
      if (obj === 'None') {
        return 'None';
      } 
        return obj ? Object.keys(obj)[0] : '';
    };
    const getNestedValue = (obj) => {
      if (obj === 'None') {
        return 'None';
      } 
        return obj ? Object.values(obj)[0] : '';
    };

    return (      
      <TableRow key={recordId} id={recordId} tabIndex={-1} hover role="checkbox" selected={selectedUser}>
        <TableCell padding="checkbox">
          <Checkbox checked={selectedUser} onChange={(event) => handleCheckboxClick(event, recordId)} />
        </TableCell>
        <TableCell component="th" scope="row" padding="none">
          <Stack direction="row" alignItems="center" spacing={2}>
            <Typography variant="subtitle2" noWrap>
              {firstname} {lastname}
            </Typography>
          </Stack>
        </TableCell>
        <TableCell align="left">{byuid}</TableCell>
        <TableCell align="left">{Object.values(reason)}</TableCell>
        <TableCell align="left">{Object.keys(language)[0]}</TableCell>
        <TableCell align="left">{level}</TableCell>
        <TableCell align="left">{getNestedKey(opiScore)} {opiDate}</TableCell>
        <TableCell align="left">{getNestedKey(wptScore)} {wptDate}</TableCell>
        <TableCell align="left">{getNestedKey(opicScore)}</TableCell>

        <TableCell align="center">
          <IconButton size="large" color="inherit" onClick={() => setPopoverOpen(true)}>
            <Iconify icon={'eva:more-vertical-fill'} />
          </IconButton>
          <Popover
              open={Boolean(isPopoverOpen)}
              anchorEl={isPopoverOpen}
              onClose={() => setPopoverOpen(false)}
              anchorOrigin={{ vertical: 'center', horizontal: 'center' }}
              transformOrigin={{ vertical: 'top', horizontal: 'center' }}
              PaperProps={{
                sx: {
                  p: 1,
                  width: '35%',
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  '& .MuiMenuItem-root': {
                    px: 1,
                    typography: 'body2',
                    borderRadius: 0.75,
                  },
                },
              }}
              >
          <Container>
          <div style={{ display: 'flex', justifyContent: 'right', paddingBottom: '1vh' }}>
                <AwardCertificate fullName={'fullnameID'} byuid={byuid} netid={'netID'} language={'languageID'} level={'levelID'} 
                opiScore={'opiscoreID'} wptScore={'wptscoreID'} 
                todaysDate={'todaysDateID'} recordId={recordId}
                />
                <MenuItem  style={{fontWeight: 'bold' }} onClick={() => setPopoverOpen(false)}>
                  <Iconify icon={'eva:close-square-outline'} sx={{ ml: 2, mr: 2 }}/>
                </MenuItem>
            </div>
                <Table>
                  <TableBody>
                    <TableRow>
                        <TableCell>Full Name:</TableCell>
                        <TableCell>
                        <EditableCell id='fullnameID' initialValue={fullname} _onChange={(value) => setfullnameValue(value)}/>
                        
                        </TableCell>
                    </TableRow>

                    <TableRow>
                    <TableCell>Net ID:</TableCell>
                        <TableCell>
                        <EditableCell id='netID' initialValue={netid}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                    <TableCell>Language:</TableCell>
                        <TableCell>
                        <EditableCell id='languageID' initialValue={Object.values(language)[0]}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Level:</TableCell>
                        <TableCell>
                        <EditableCell id='levelID' initialValue={level} />
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>OPI Score:</TableCell>
                        <TableCell>
                        <EditableCell id='opiscoreID' initialValue={getNestedValue(opiScore)} />
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>WPT Score:</TableCell>
                        <TableCell>
                        <EditableCell id='wptscoreID' initialValue={getNestedValue(wptScore)} />
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Date Awarded:</TableCell>
                        <TableCell>
                        <EditableCell id='todaysDateID' initialValue={todaysDate} />
                        </TableCell>
                    </TableRow>
                    
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>

          
              </TableBody>
              </Table>

          </Container>
        </Popover>
        </TableCell>
      </TableRow>
          
    );
  }
  const emptyRows = page > 0 ? Math.max(0, (1 + page) * rowsPerPage - userList.length) : 0;

  const filteredUsers = applySortFilter(studentdata, getComparator(order, orderBy), filterName);
  console.log('filteredUsers:', filteredUsers);
  const isNotFound = !filteredUsers.length && !!filterName;

  const handleSearch = async () => {
    setLoading(true);
    setPopoverOpen(false);
    console.log(languageValue, byuidValue)
    try {
      const csrfToken = Cookies.get('csrftoken');
      const response = await axios.get(verifyTokenUrl, {
        withCredentials: true,
        headers: {
          "X-CSRFToken": csrfToken,
        },
      });
  
      if (response.status === 200) {
        try {
          const formattedrecordDate = format(recordDate, 'MM/dd/yyyy');
          const formattedsemesterDate = format(semesterDate, 'MM/dd/yyyy');
          const csrfToken = Cookies.get('csrftoken');
          const response = await axios.post(getCertificateDataUrl, 
            {
              recordDate: formattedrecordDate,
              semesterDate: formattedsemesterDate,
              byuidValue,
              languageValue,
            }
            ,{withCredentials: true,
            headers: {
              'X-CSRFToken': csrfToken,
            },
          });
  
          const fetchedData = response.data;
          console.log(fetchedData);

          setData(fetchedData);
  
          const userList = fetchedData.map(item => `${item.recordId}`);
          setUserList(userList);
          setLoading(false);
          setIsLoading(false);
          setLanguageValue('None');
          setByuidValue('None');
        } catch (error) {
          console.log(error);
          setLanguageValue('None');
          setByuidValue('None');
          setLoading(false);
          
        }
      }
    } catch (error) {
      console.log(error);
      navigate('/cls/login', { replace: true });
      setLanguageValue('None');
      setByuidValue('None');
      setLoading(false);
    }
  };
  return (
    <>
      <Helmet>
        <title> CLS Admin </title>
      </Helmet>

      <Container>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Typography variant="h4" gutterBottom>
            Language Certificates
          </Typography>
        </Stack>

        <Card>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
      <Button
          variant="contained"
          onClick={() => setPopoverCustomOpen(true)}
          sx={{
            margin: '2% !important',
            height: '48px',
            width: '130px',
            marginTop: '10px',
            position: 'relative', // Set position relative to the button
          }}
        >
      <span style={{ visibility: loading ? 'hidden' : 'visible' }}>Create Custom</span>
      {loading && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
          }}
        >
          <PulseLoader
            loading={loading}
            size={5}
            aria-label="Loading Spinner"
            data-testid="loader"
            sx={{ height: 'inherit' }}
          />
        </div>
      )}
    </Button>
      <Popover
            open={Boolean(isPopoverCustomOpen)}
            anchorEl={isPopoverCustomOpen}
            onClose={() => setPopoverCustomOpen(false)}
            anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            transformOrigin={{ vertical: 'top', horizontal: 'center' }}
            PaperProps={{
              sx: {
                p: 1,
                width: '35%',
                position: 'fixed',
                marginTop: '6vw',

              },
            }}
          >
            <div>
          <Container>
          <div style={{ display: 'flex', justifyContent: 'right', paddingBottom: '1vh' }}>
                <AwardCertificate fullName={'fullnameID'} byuid={'byuID'} netid={'netID'} language={'languageID'} level={'levelID'} 
                opiScore={'opiscoreID'} wptScore={'wptscoreID'} recordId={'0'}
                todaysDate={'todaysDateID'}
                />
                <MenuItem  style={{fontWeight: 'bold' }} onClick={() => setPopoverCustomOpen(false)}>
                  <Iconify icon={'eva:close-square-outline'} sx={{ ml: 2, mr: 2 }}/>
                </MenuItem>
            </div>
                <Table>
                  <TableBody>
                    <TableRow>
                        <TableCell>Full Name:</TableCell>
                        <TableCell>
                        <EditableCell id='fullnameID'  _onChange={(value) => setfullnameValue(value)}/>
                        
                        </TableCell>
                    </TableRow>

                    <TableRow>

                    <TableCell>BYU ID:</TableCell>
                        <TableCell>
                        <EditableCell id='byuID' />
                        </TableCell>
                    </TableRow>

                    <TableRow>
                    <TableCell>Net ID:</TableCell>
                        <TableCell>
                        <EditableCell id='netID' />
                        </TableCell>
                    </TableRow>

                    <TableRow>
                    <TableCell>Language:</TableCell>
                        <TableCell>
                        <EditableCell id='languageID' />
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Level:</TableCell>
                        <TableCell>
                        <EditableCell id='levelID'  />
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>OPI Score:</TableCell>
                        <TableCell>
                        <EditableCell id='opiscoreID'  />
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>WPT Score:</TableCell>
                        <TableCell>
                        <EditableCell id='wptscoreID'  />
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Date Awarded:</TableCell>
                        <TableCell>
                        <EditableCell id='todaysDateID' initialValue={todaysDate} />
                        </TableCell>
                    </TableRow>
                    
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>

          
              </TableBody>
              </Table>

          </Container>
          </div>
      </Popover>

  <Button
  variant="contained"
  onClick={() => setPopoverOpen(true)}
  sx={{
    margin: '2% !important',
    height: '48px',
    width: '130px',
    marginTop: '10px',
    position: 'relative', // Set position relative to the button
  }}
>
  <span style={{ visibility: loading ? 'hidden' : 'visible' }}>Award Certificates</span>
  {loading && (
    <div
      style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
      }}
    >
      <PulseLoader
        loading={loading}
        size={5}
        aria-label="Loading Spinner"
        data-testid="loader"
        sx={{ height: 'inherit' }}
      />
    </div>
  )}
</Button>

    <Typography variant="subtitle2" sx={{ px: 4, py: 0 }}>
      {filteredUsers.length} Students found
    </Typography>
  </div>
  <UserListToolbar 
    numSelected={selected.length} 
    filterName={filterName}
    onFilterName={handleFilterByName} 
  />
</div>
          <Popover
            open={Boolean(isPopoverOpen)}
            anchorEl={isPopoverOpen}
            onClose={() => setPopoverOpen(false)}
            anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            transformOrigin={{ vertical: 'top', horizontal: 'center' }}
            PaperProps={{
              sx: {
                p: 1,
                width: '35%',
                position: 'fixed',
                marginTop: '6vw',

              },
            }}
          >
          <Container>
          <div style={{ display: 'flex', justifyContent: 'flex-end', paddingBottom: '1vh' }}>
              <MenuItem onClick={() => handleSearch()}>
                  <Iconify icon={'eva:search-outline'} sx={{ ml: 2, mr: 2 }}/>
              </MenuItem>
              <MenuItem style={{ fontWeight: 'bold' }} onClick={() => setPopoverOpen(false)}>
                  <Iconify icon={'eva:close-square-outline'} sx={{ ml: 2, mr: 2 }}/>
              </MenuItem>
          </div>

                <Table>
                  <TableBody>

                    <TableRow>
                        <TableCell>Select Students From:</TableCell>
                        <TableCell>
                        <DatePicker
                            id="semesterDate"
                            selected={semesterDate}
                            onChange={(date) => setsemesterDate(date)}
                            wrapperClassName="datePicker"
                          />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Scores Valid From:</TableCell>
                        <TableCell>
                        <DatePicker
                            id="recordDate"
                            selected={recordDate}
                            onChange={(date) => setrecordDate(date)}
                            wrapperClassName="datePicker"
                          />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Language</TableCell>
                        <TableCell>
                        <EditableCell initialValue='None' _onChange={(value) => setLanguageValue(value)}/>
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>BYU ID</TableCell>
                        <TableCell>
                        <EditableCell initialValue='None' _onChange={(value) => setByuidValue(value)}/>
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
                    <TableRow>
                        <TableCell sx={{borderColor: "white !important"}}/>
                        <TableCell sx={{borderColor: "white !important"}}/>
                    </TableRow>
              </TableBody>
              </Table>

          </Container>
        </Popover>



          <Scrollbar>
            <TableContainer sx={{ minWidth: 800 }}>


            <div>
            {isLoading ? (
              <div style={{margin:'10px'}}>
              <p>Waiting for user input...</p>
              </div>
            ) : (
              <div>
                <Table>
                <UserListHead
                  order={order}
                  orderBy={orderBy}
                  headLabel={TABLE_HEAD}
                  rowCount={userList.length}
                  numSelected={selected.length}
                  onRequestSort={handleRequestSort}
                  onSelectAllClick={handleSelectAllClick}
                />
            <TableBody>
            {filteredUsers.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((user) => (
                      <UserTableRow
                        key={user.recordId}
                        id={user.recordId}
                        user={user}
                        handleCheckboxClick={handleCheckboxClick}
                        handleOpenMenu={handleOpenMenu}
                      />
                    ))}
            </TableBody>
                </Table>
              </div>
            )}
          </div>

            {isNotFound && (
                  <TableBody>
                    <TableRow>
                      <TableCell align="center" colSpan={6} sx={{ py: 3 }}>
                        <Paper
                          sx={{
                            textAlign: 'center',
                          }}
                        >
                          <Typography variant="h6" paragraph>
                            Not found
                          </Typography>

                          <Typography variant="body2">
                            No results found for &nbsp;
                            <strong>&quot;{filterName}&quot;</strong>.
                            <br /> Try checking for typos or using complete words.
                          </Typography>
                        </Paper>
                      </TableCell>
                    </TableRow>
                  </TableBody>
            )}
            </TableContainer>
          </Scrollbar>

          <TablePagination
            rowsPerPageOptions={[10, 25, 100]}
            component="div"
            count={userList.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Card>
      </Container>
    </>
  );
}      
