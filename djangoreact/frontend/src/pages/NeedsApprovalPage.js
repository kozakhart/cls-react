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
  TextField,
} from '@mui/material';
// components
import { is } from 'date-fns/locale';
import EditableCell from '../components/editablecell/EditableCell';

import UpdateNotification from '../components/updatenotification/UpdateNotification';
import DeleteNotification from '../components/deletenotification/DeleteNotification';

import Label from '../components/label';
import Iconify from '../components/iconify';
import Scrollbar from '../components/scrollbar';
// sections
import { UserListHead, UserListToolbar } from '../sections/@dashboard/needsapproval';
// mock

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: 'name', label: 'Name', alignRight: false },
  { id: 'byuid', label: 'BYU ID', alignRight: false},
  { id: 'language', label: 'Language', alignRight: false },
  { id: 'reason', label: 'Reason', alignRight: false },
  { id: 'come_to_campus', label: 'Come To Campus', alignRight: false },
  { id: 'more', label: 'More Info', alignRight: false },
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
  const navigate = useNavigate();
  const verifyTokenUrl = process.env.REACT_APP_VERIFY_TOKEN_URL;
  const needApprovalUrl = process.env.REACT_APP_NEED_APPROVAL_URL;
  const handleClickedBox = () => {
    setIsChecked(!isChecked); 
  };

  useEffect(() => {
    const fetchData = async () => {
      try{
        const csrfToken = Cookies.get('csrftoken');
        const response = await axios.get(verifyTokenUrl, {
           withCredentials: true,
            headers: {
              "X-CSRFToken": csrfToken,
            }, 
        });
        if (response.status === 200) {
      try {
        const csrfToken = Cookies.get('csrftoken');
      const response = await axios.get(needApprovalUrl, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrfToken,
        },
      });
      const fetchedData = response.data;
      if (fetchedData && fetchedData.response && fetchedData.response.data) {
        setData(fetchedData.response.data);
      
        const userList = fetchedData.response.data.map(item => `${item.recordId}`);
        setUserList(userList);
        setIsLoading(false);
      } else {
        console.log("Data structure is invalid or undefined.");
      }

      } catch (error) {
        console.log(error);
      }
    }
  }
  catch (error) {
    navigate('/cls/login', { replace: true });
    console.log(error);
  }
    };
    fetchData();
    }, []);


  const [open, setOpen] = useState(null);

  const [openData, setOpenData] = useState(null);

  const [page, setPage] = useState(0);

  const [order, setOrder] = useState('asc');

  const [selected, setSelected] = useState([]);

  const [orderBy, setOrderBy] = useState('name');

  const [filterName, setFilterName] = useState('');

  const [rowsPerPage, setRowsPerPage] = useState(10);

  const handleOpenMenu = (event) => {
    setOpen(event.currentTarget);
  };

  const handleCloseMenu = () => {
    setOpen(null);
  };

  const handleDataOpenMenu = (event) => {
    setOpenData(event.currentTarget);
  };

  const handleDataCloseMenu = () => {
    setOpenData(null);
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
    const { FirstName, LastName, Approved, Reason, Language, LanguageOther, TestDate1, Time1, Time2, TestDate2, Time3, Time4, TestScheduled, CertificateStatus, 
      ComeToCampus, CannotCome, Email, EmailSent, LTISchedule, Phone, Scores, BYUID, NetID, EntryDate, EntryTime,  
      Major, SecondMajor, Minor, PreviousExperience
    
    } = user.fieldData;
    const { recordId }= user;
    console.log('recordId:', recordId);
    // const selectedUser = user.selected;
    const selectedUser = selected.indexOf(recordId) !== -1;

    const [isPopoverOpen, setPopoverOpen] = useState(false);
    return (      
      <TableRow key={recordId} id={recordId} tabIndex={-1} hover role="checkbox" selected={selectedUser}>
        <TableCell padding="checkbox">
          <Checkbox checked={selectedUser} onChange={(event) => handleCheckboxClick(event, recordId)} />
        </TableCell>
        <TableCell component="th" scope="row" padding="none">
          <Stack direction="row" alignItems="center" spacing={2}>
            <Typography variant="subtitle2" noWrap>
              {FirstName} {LastName}
            </Typography>
          </Stack>
        </TableCell>
        <TableCell align="left">{BYUID}</TableCell>
        <TableCell align="left">{Language}</TableCell>
        <TableCell align="left">{Reason}</TableCell>
        <TableCell align="left">{ComeToCampus}</TableCell>
        <TableCell align="center">
          <IconButton size="large" color="inherit" onClick={() => setPopoverOpen(true)}>
            <Iconify icon={'eva:more-vertical-fill'} />
          </IconButton>
          <Popover
            open={Boolean(isPopoverOpen)}
            anchorEl={isPopoverOpen}
            onClose={isPopoverOpen}
            anchorOrigin={{ vertical: 'center', horizontal: 'center' }} // Center the anchor
            transformOrigin={{ vertical: 'top', horizontal: 'center' }}
            PaperProps={{
              sx: {
                p: 1,
                width: '25%',
                '& .MuiMenuItem-root': {
                  px: 1,
                  typography: 'body2',
                  borderRadius: 0.75,
                },
              },
            }}
          >
          <Container>
          <div style={{ display: 'flex', justifyContent: 'left', paddingBottom: '1vh' }}>
                <UpdateNotification firstnameID={'firstnameID'} lastnameID={'lastnameID'} approvedID={'approvedID'} reasonID={'reasonID'} languageID={'languageID'} languageotherID={'languageotherID'}
                testdate1ID={'testdate1ID'} time1ID={'time1ID'} time2ID={'time2ID'} testdate2ID={'testdate2ID'} time3ID={'time3ID'} time4ID={'time4ID'} testscheduledID={'testscheduledID'}
                certificatestatusID={'certificatestatusID'} cometocampusID={'cometocampusID'} cannotcomeID={'cannotcomeID'} emailID={'emailID'} emailsentID={'emailsentID'}
                ltischeduleID={'ltischeduleID'} phoneID={'phoneID'} scoresID={'scoresID'} byuidID={'byuidID'} netidID={'netidID'} entrydateID={'entrydateID'} entrytimeID={'entrytimeID'}
                majorID={'majorID'} secondmajorID={'secondmajorID'} minorID={'minorID'} previousexperienceID={'previousexperienceID'} recordId={recordId}
                />
                <DeleteNotification recordId={recordId}/>
                <MenuItem  style={{fontWeight: 'bold' }} onClick={() => setPopoverOpen(false)}>
                  X
                </MenuItem>
            </div>
                <Table>
                  <TableBody>
                    <TableRow>
                        <TableCell>First Name:</TableCell>
                        <TableCell>
                        <EditableCell id='firstnameID' initialValue={FirstName} />
                        </TableCell>
                    </TableRow>
                  
                    <TableRow>
                        <TableCell>Last Name:</TableCell>
                        <TableCell>
                        <EditableCell id='lastnameID' initialValue={LastName}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Approved:</TableCell>
                        <TableCell>
                        <EditableCell id='approvedID' initialValue={Approved}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Reason:</TableCell>
                        <TableCell>
                        <EditableCell id='reasonID' initialValue={Reason}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Language:</TableCell>
                        <TableCell>
                        <EditableCell id='languageID' initialValue={Language}/>
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Language Other:</TableCell>
                        <TableCell>
                        <EditableCell id='languageotherID' initialValue={LanguageOther}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Test Scheduled:</TableCell>
                        <TableCell>
                        <EditableCell id='testscheduledID' initialValue={TestScheduled}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>LTI Schedule:</TableCell>
                        <TableCell>
                        <EditableCell id='ltischeduleID' initialValue={LTISchedule}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Test Date 1:</TableCell>
                        <TableCell>
                        <EditableCell id='testdate1ID' initialValue={TestDate1}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Time 1:</TableCell>
                        <TableCell>
                        <EditableCell id='time1ID' initialValue={Time1}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Time 2:</TableCell>
                        <TableCell>
                        <EditableCell id='time2ID' initialValue={Time2}/>  
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Test Date 2:</TableCell>
                        <TableCell>
                        <EditableCell id='testdate2ID' initialValue={TestDate2}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Time 3:</TableCell>
                        <TableCell>
                        <EditableCell id='time3ID' initialValue={Time3}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Time 4:</TableCell>
                        <TableCell>
                        <EditableCell id='time4ID' initialValue={Time4}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Certificate Status:</TableCell>
                        <TableCell>
                        <EditableCell id='certificatestatusID' initialValue={CertificateStatus}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Come To Campus:</TableCell>
                        <TableCell>
                        <EditableCell id='cometocampusID' initialValue={ComeToCampus}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Cannot Come:</TableCell>
                        <TableCell>
                        <EditableCell id='cannotcomeID' initialValue={CannotCome}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Email:</TableCell>
                        <TableCell>
                        <EditableCell id='emailID' initialValue={Email}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Email Sent:</TableCell>
                        <TableCell>
                        <EditableCell id='emailsentID' initialValue={EmailSent}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Phone:</TableCell>
                        <TableCell>
                        <EditableCell id='phoneID' initialValue={Phone}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Scores:</TableCell>
                        <TableCell>
                        <EditableCell id='scoresID' initialValue={Scores}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>BYU ID:</TableCell>
                        <TableCell>
                        <EditableCell id='byuidID' initialValue={BYUID}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Net ID:</TableCell>
                        <TableCell>
                        <EditableCell id='netidID' initialValue={NetID}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Entry Date:</TableCell>
                        <TableCell>
                        <EditableCell id='entrydateID' initialValue={EntryDate}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Entry Time:</TableCell>
                        <TableCell>
                        <EditableCell id='entrytimeID' initialValue={EntryTime}/>  
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Major:</TableCell>
                        <TableCell>
                        <EditableCell id='majorID' initialValue={Major}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Second Major:</TableCell>
                        <TableCell>
                        <EditableCell id='secondmajorID' initialValue={SecondMajor}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Minor:</TableCell>
                        <TableCell>
                        <EditableCell id='minorID' initialValue={Minor}/>
                        </TableCell>
                    </TableRow>

                    <TableRow>
                        <TableCell>Previous Experience:</TableCell>
                        <TableCell>
                        <EditableCell id='previousexperienceID' initialValue={PreviousExperience}/>
                        </TableCell>
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

  return (
    <>
      <Helmet>
        <title> CLS Admin </title>
      </Helmet>

      <Container>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Typography variant="h4" gutterBottom>
            Students Needing Approval
          </Typography>
        </Stack>

        <Card>
          <UserListToolbar 
          numSelected={selected.length} 
          filterName={filterName}
          onFilterName={handleFilterByName} 

          />
          <Typography variant="subtitle2" sx={{ px: 4, py: 0 }}>
            {filteredUsers.length} Students found
          </Typography>
          <Scrollbar>
            <TableContainer sx={{ minWidth: 800 }}>


            <div>
            {isLoading ? (
              <p>Loading...</p>
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

      <Popover
        open={Boolean(open)}
        anchorEl={open}
        onClose={handleCloseMenu}
        anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: {
            p: 1,
            width: 140,
            '& .MuiMenuItem-root': {
              px: 1,
              typography: 'body2',
              borderRadius: 0.75,
            },
          },
        }}
      >
        <MenuItem onClick={handleDataOpenMenu}>
          <Iconify icon={'eva:edit-fill'} sx={{ mr: 2 }}/>
          Edit
        </MenuItem>

        <MenuItem sx={{ color: 'error.main' }}>
          <Iconify icon={'eva:trash-2-outline'} sx={{ mr: 2 }} />
          Delete
        </MenuItem>
      </Popover>

    
    </>
  );
}      
