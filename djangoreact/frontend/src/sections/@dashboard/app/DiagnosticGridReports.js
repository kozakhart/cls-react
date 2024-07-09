import PropTypes from 'prop-types';
import ReactApexChart from 'react-apexcharts';
// @mui
import { Box, Card, CardHeader } from '@mui/material';
// utils
import { fNumber } from '../../../utils/formatNumber';
// components
import { useChart } from '../../../components/chart';

// ----------------------------------------------------------------------

DiagnosticGridReports.propTypes = {
  title: PropTypes.string,
  subheader: PropTypes.string,
  chartData: PropTypes.object.isRequired,
};

export default function DiagnosticGridReports({ title, subheader, chartData, ...other }) {

  const chartLabels = [];
const chartSeries = [];

Object.keys(chartData).forEach((key, index) => {
  const label = Object.keys(chartData[index])[0]; // Assuming each object has one key
  chartLabels.push(label);
  chartSeries.push(chartData[index][label]);
});
  console.log(chartLabels);
  console.log(chartSeries);
  

  const colors = ['#00E396', '#FEB019']; // Define your alternating colors

  const chartOptions = useChart({
    chart: {
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
    tooltip: {
      marker: { show: false },
      y: {
        formatter: (seriesName) => fNumber(seriesName),
        title: {
          formatter: () => '',
        },
      },
    },
    plotOptions: {
      bar: {
        horizontal: true,
        barHeight: '28%',
        borderRadius: 2,
      },
    },
    xaxis: {
      categories: chartLabels,
    },
    fill: {
      colors: chartSeries.map((_, index) => colors[index % colors.length]),
    },
  });

  return (
    <Card {...other}>
      <CardHeader title={title} subheader={subheader} />

      <Box sx={{ mx: 3 }} dir="ltr">
        <ReactApexChart type="bar" series={[{ data: chartSeries }]} options={chartOptions} height={364} />
      </Box>
    </Card>
  );
}