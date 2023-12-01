import PropTypes from 'prop-types';
import ReactApexChart from 'react-apexcharts';
// @mui
import { useTheme, styled } from '@mui/material/styles';
import { Box, Card, CardHeader } from '@mui/material';
// utils
import { fNumber } from '../../../utils/formatNumber';
// components
import { useChart } from '../../../components/chart';

// ----------------------------------------------------------------------

const CHART_HEIGHT = 100;
const LEGEND_HEIGHT = 10;

const StyledChartWrapper = styled('div')(({ theme }) => ({
  height: CHART_HEIGHT,
  marginTop: theme.spacing(5),
  '& .apexcharts-canvas svg': { height: CHART_HEIGHT },
  '& .apexcharts-canvas svg,.apexcharts-canvas foreignObject': {
    overflow: 'visible',
  },
  '& .apexcharts-legend': {
    height: LEGEND_HEIGHT,
    alignContent: 'center',
    position: 'relative !important',
    borderTop: `solid 1px ${theme.palette.divider}`,
    top: `calc(${CHART_HEIGHT - LEGEND_HEIGHT}px) !important`,
  },
}));
// ----------------------------------------------------------------------

AppCurrentVisits.propTypes = {
  title: PropTypes.string,
  subheader: PropTypes.string,
  chartColors: PropTypes.arrayOf(PropTypes.string),
  chartData: PropTypes.array,
};

export default function AppCurrentVisits({ title, subheader, chartColors, chartData, ...other }) {
  const theme = useTheme();

  const chartLabels = chartData.map((i) => `${i.label}: ${i.value}`);

  const chartSeries = chartData.map((i) => i.value);
  const totalSum = chartSeries.reduce((acc, value) => acc + value, 0);

  const chartOptions = {
    chart: 
      {
      toolbar: {
        show: true,
        offsetX: 0,
        offsetY: 0,
        tools: {
          download: true,
          selection: true,
          zoom: true,
          zoomin: true,
          zoomout: true,
          pan: true,
          reset: true, // Or use your custom reset button
          customIcons: [],
        },
        export: {
          csv: {
            filename: undefined,
            columnDelimiter: ',',
            headerCategory: 'category',
            headerValue: 'value',
            dateFormatter(timestamp) {
              return new Date(timestamp).toDateString();
            },
          },
          svg: {
            filename: undefined,
          },
          png: {
            filename: undefined,
          },
        },
        autoSelected: 'zoom',
      },
    },
    colors: chartColors,
    labels: chartLabels ,
    legend: { show: false},
    stroke: { colors: [theme.palette.background.paper] },
    dataLabels: { enabled: true, dropShadow: { enabled: false } },
    tooltip: {
      fillSeriesColor: false,
      y: {
        formatter: (value, { series, seriesIndex }) => {
          const percentage = ((value / totalSum) * 100).toFixed(2);
          const language = chartLabels[seriesIndex].split(':')[0]; // Extract the part before the colon
          return `(${percentage}%)`;
        },
        title: {
          formatter: (seriesName) => `${seriesName}`,
        },
      },
    },
    plotOptions: {
      pie: { donut: { labels: { show: false } } },
    },
  };

  return (
    <Card {...other}>
      <CardHeader title={title} subheader={subheader} />

        <Box dir="ltr">
        <ReactApexChart type="pie" series={chartSeries} options={chartOptions} height={300}/>
        </Box>

    </Card>
  );
}
