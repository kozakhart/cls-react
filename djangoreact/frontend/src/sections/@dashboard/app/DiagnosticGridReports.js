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

Object.entries(chartData).forEach(([key, value]) => {
    chartLabels.push(key);
    chartSeries.push(value);
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
      formatter: (seriesName) => seriesName.toFixed(2), // Adjust the precision based on your data type
      // formatter: (seriesName) => fNumber(seriesName),
      title: {
          formatter: () => '',
        }, 
    },
    // x: {
    // },
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
      min:0,
      max: 1
    },
    yaxis: {
      labels: {
  //    rotate: -45, // Rotate labels by -45 degrees (adjust as needed)
    },
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