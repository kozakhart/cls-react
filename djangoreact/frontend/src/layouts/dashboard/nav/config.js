import SvgColor from '../../../components/svg-color';


const icon = (name) => <SvgColor src={`/assets/icons/navbar/${name}.svg`} sx={{ width: 1, height: 1 }} />;

const navConfig = [
  {
    title: 'Dashboard',
    path: '/cls/dashboard/app',
    icon: icon('ic_analytics'),
    groups: ['CLS', 'Dashboard']
  },
  {
    title: 'Database',
    path: '/cls/dashboard/database',
    icon: icon('ic_user'),
    groups: ['CLS', 'Database']
  },
  {
    title: 'Awaiting Approval',
    path: '/cls/dashboard/needs-approval',
    icon: icon('ic_user'),
    groups: ['CLS', 'Awaiting Approval']
  },
  {
    title: 'Language Certificates',
    path: '/cls/dashboard/language-certificates',
    icon: icon('ic_user'),
    groups: ['CLS', 'Language Certificates']
  },
  {
    title: 'Qualtrics Reports',
    path: '/cls/dashboard/qualtrics-reports',
    icon: icon('ic_report'),
    groups: ['CLS', 'Qualtrics Reports']
  },
  {
    title: 'LASER Database',
    path: '/cls/dashboard/laser-database',
    icon: icon('ic_report'),
    groups: ['CLS', 'LASER Database']
  },
  {
    title: 'Diagnostic Grids',
    path: '/cls/dashboard/diagnostic-grids',
    icon: icon('ic_report'),
    groups: ['CLS', 'Diagnostic Grids']
  }
  // {
  //   title: 'Generate Report',
  //   path: '/cls/dashboard/generate-reports',
  //   icon: icon('ic_analytics'),
  //   groups: ['CLS']
  // },
];

export default navConfig;
