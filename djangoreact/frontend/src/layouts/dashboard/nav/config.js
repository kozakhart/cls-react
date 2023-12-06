// component
import SvgColor from '../../../components/svg-color';

// ----------------------------------------------------------------------

const icon = (name) => <SvgColor src={`/assets/icons/navbar/${name}.svg`} sx={{ width: 1, height: 1 }} />;

const navConfig = [
  {
    title: 'dashboard',
    path: '/cls/dashboard/app',
    icon: icon('ic_analytics'),
  },
  {
    title: 'Database',
    path: '/cls/dashboard/user',
    icon: icon('ic_user'),
  },
  {
    title: 'Awaiting Approval',
    path: '/cls/dashboard/needs-approval',
    icon: icon('ic_user'),
  },
  {
    title: 'Language Certificates',
    path: '/cls/dashboard/language-certificates',
    icon: icon('ic_user'),
  },
  {
    title: 'Generate Report',
    path: '/cls/dashboard/reports',
    icon: icon('ic_analytics'),
  },
  // {
  //   title: 'Not found',
  //   path: '/404',
  //   icon: icon('ic_disabled'),
  // },
];

export default navConfig;
