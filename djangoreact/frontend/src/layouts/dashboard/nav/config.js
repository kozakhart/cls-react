import SvgColor from '../../../components/svg-color';


const icon = (name) => <SvgColor src={`/assets/icons/navbar/${name}.svg`} sx={{ width: 1, height: 1 }} />;

const navConfig = [
  {
    title: 'dashboard',
    path: '/cls/dashboard/app',
    icon: icon('ic_analytics'),
    groups: ['CLS']
  },
  {
    title: 'Database',
    path: '/cls/dashboard/user',
    icon: icon('ic_user'),
    groups: ['CLS']
  },
  {
    title: 'Awaiting Approval',
    path: '/cls/dashboard/needs-approval',
    icon: icon('ic_user'),
    groups: ['CLS']
  },
  {
    title: 'Language Certificates',
    path: '/cls/dashboard/language-certificates',
    icon: icon('ic_user'),
    groups: ['CLS']
  },
  {
    title: 'Qualtrics Reports',
    path: '/cls/dashboard/qualtrics-reports',
    icon: icon('ic_report'),
    groups: ['CLS']
  },
  {
    title: 'Generate Report',
    path: '/cls/dashboard/reports',
    icon: icon('ic_analytics'),
    groups: ['CLS']
  },
];

export default navConfig;
