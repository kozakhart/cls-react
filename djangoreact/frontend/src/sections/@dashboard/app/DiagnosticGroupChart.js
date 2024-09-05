import PropTypes from 'prop-types';
import React, { useState, useEffect } from 'react';
import ReactApexChart from 'react-apexcharts';
// @mui
import { Box, Card, CardHeader, Button } from '@mui/material';
// utils
// components
import { useChart } from '../../../components/chart';

// ----------------------------------------------------------------------

DiagnosticGroupChart.propTypes = {
  title: PropTypes.string,
  subheader: PropTypes.string,
  chartData: PropTypes.array.isRequired,
};

export default function DiagnosticGroupChart({ title, subheader, chartData = [], details, total, ...other }) {
    console.log('chartData for group', chartData);
  const [sortedData, setSortedData] = useState(chartData);
    
  const professionalColors = ['#f45f74','#8fd7d7'];
  // , '#00b0be', '#ff8ca1', '#bdd373', '#98c127', '#ffcd8e', '#ffb255'

  const chartLabels = [];

// Object.entries(sortedData).forEach(([key, value]) => {
//     chartLabels.push(key);
//     chartSeries.push({ name: key, data:[value] });
//   });
const seriesMap = {};

chartData.forEach(dataObject => {
    Object.entries(dataObject).forEach(([key, value]) => {
        if (!seriesMap[key]) {
            chartLabels.push(key);
            seriesMap[key] = [];
        }
        seriesMap[key].push(value);
    });
});

// Convert the seriesMap to chartSeries using map
const chartSeries = Object.keys(seriesMap).map(name => ({
    name,
    data: seriesMap[name]
}));
  console.log('chartLabels', chartLabels);
    console.log('chartSeries', chartSeries);
  
  const chartOptions = useChart({
    chart: {
        events: {
        // dataPointSelection: (event, chartContext, opts) => {
        //   // setSelectedBarData([]);
        //   // setSelectedBarLabels([]);
        //   const detailLabels = [];
        //   const formattedData = [];
        //   const detailSortedData = []

        //   const detailName = opts.w.config.series[opts.seriesIndex].name;
        //   const barData = details[detailName];
          
        //   setDetailName(detailName)

        // Object.entries(details).forEach(([key, value]) => {
        //     if (key === detailName) {
        //         Object.entries(value).forEach(([key, value]) => {
        //             formattedData.push({ name: key, data: [(value / total)] });
        //             detailSortedData[key] = value;
        //         });
        //     }
        // }     
        // );
          
        //   Object.entries(formattedData).forEach(([key, value]) => {
        //     detailLabels.push(value.name);
        //   });
        //   setSelectedBarLabels(detailLabels);
        //   setSelectedBarData(formattedData);
        //   setDetailSortedData(detailSortedData);
          

        //   },
        },
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
          reset: true,
          customIcons: [],
        },
        export: {
          csv: {
            filename: 'diagnostic_grid_data',
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
            filename: 'diagnostic_grid_graph',
          },
        },
        autoSelected: 'zoom',
      },
    },
    tooltip: {
    marker: { show: true },
    y: {
      formatter: (value) => `${(value * 100).toFixed(0)}%`,
      title: {
          formatter: () => '',
        }, 
    },
  },
    plotOptions: {
      bar: {
        horizontal: true,
        barHeight: '99%',
        borderRadius: 2,
        
      },
    },
    xaxis: {
      categories: chartLabels,
      min:0,
      max: 1,
      title: {
        text: 'Percent Of Students That Need To Improve In Each Area',
      },
      labels: {
      formatter: (value) => `${(value * 100).toFixed(0)}%`,
    },
    },
    yaxis: {
      showAlways: false,
      showEmpty: false,
      labels: {
      },
    },
    // fill: professionalColors,
  // colors: professionalColors,
      legend: {
      show: true,
      position: 'bottom',
      horizontalAlign: 'center',
      fontSize: '14px',
      labels: {
        colors: '#333', // Customize text color
        useSeriesColor: true, // If you want the legend colors to match the series
      },
      markers: {
        width: 10,
        height: 10,
        strokeWidth: 0,
        strokeColor: '#fff',
  //     fillColors: professionalColors, // Set marker colors
      },
      itemMargin: {
        horizontal: 10,
        vertical: 5,
      },
      onItemClick: {
          toggleDataSeries: false
      },
    },
  });

  return (
    <Card {...other}>
        <CardHeader title={title} subheader={subheader} />
        <Box sx={{ mx: 3 }} dir="ltr">
          {/* <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button onClick={() => handleAlphabeticalSort(sortOrder === 'asc' ? 'desc' : 'asc')}>
              FACT Sort
            </Button>
            <Button onClick={() => handleSort(sortOrder === 'asc' ? 'desc' : 'asc', sortedData)}>
              Value Sort
            </Button>
          </Box> */}
          <ReactApexChart type="bar" series={chartSeries} options={chartOptions} height={364} />
          {/* {selectedBarData && selectedBarData.length > 0 && (
            <div>
              <CardHeader title={`${detailName}`} />
              <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
                <Button onClick={() => handleDetailSort(sortDetailOrder === 'asc' ? 'desc' : 'asc', selectedBarData)}>
                  Sort By Value
                </Button>
                <Button onClick={handleDeselect} color="error">
                  Deselect
                </Button>
              </Box>
                 <ReactApexChart
                 key={JSON.stringify(selectedBarData)}
                  type="bar"
                  series={selectedBarData}
                  options={detailOptions}
                  height={364}
                />
            </div>
          )} */}
        </Box>
        <style>{`
          .apexcharts-menu-item.exportSVG {
            display: none;
          }
        `}</style>
        
      </Card>

  );
}