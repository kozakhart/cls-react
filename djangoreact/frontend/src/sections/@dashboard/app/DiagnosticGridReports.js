import PropTypes from 'prop-types';
import React, { useState, useEffect } from 'react';
import ReactApexChart from 'react-apexcharts';
// @mui
import { Box, Card, CardHeader, Button } from '@mui/material';
// utils
// components
import { useChart } from '../../../components/chart';

// ----------------------------------------------------------------------

DiagnosticGridReports.propTypes = {
  title: PropTypes.string,
  subheader: PropTypes.string,
  chartData: PropTypes.object.isRequired,
};

export default function DiagnosticGridReports({ title, subheader, chartData, details, total, ...other }) {
  const [selectedBarData, setSelectedBarData] = useState([]);
  const [selectedBarLabels, setSelectedBarLabels] = useState([]);
  const [sortOrder, setSortOrder] = useState('asc');
  const [sortedData, setSortedData] = useState(chartData);
const professionalColors = ['#f45f74','#8fd7d7', '#00b0be', '#ff8ca1', '#bdd373', '#98c127', '#ffcd8e', '#ffb255'];

useEffect(() => {
  console.log("SelectedBarData updated:", selectedBarData);
}, [selectedBarData]);

useEffect(() => {
  console.log("SelectedBarLabels updated:", selectedBarLabels);
}, [selectedBarLabels]);

const handleDeselect = () => {
  setSelectedBarData([]);
  setSelectedBarLabels([]);
};

const handleSort = (order) => {
  const sorted = Object.entries(sortedData)
    .sort(([, a], [, b]) => {
      // Ensure values are numbers
      const numA = Number(a);
      const numB = Number(b);
      return order === 'asc' ? numA - numB : numB - numA;
    })
    .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});
    
  setSortedData(sorted);
  setSortOrder(order);
};


  const chartLabels = [];
  const chartSeries = [];




Object.entries(sortedData).forEach(([key, value]) => {
    chartLabels.push(key);
    chartSeries.push({ name: key, data:[value] });
  });
  
  const detailOptions = useChart({
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
      formatter: (value) => `${((value) * 100).toFixed(0)}%`,
      title: {
          formatter: () => '',
        }, 
    },
  },
  plotOptions: {
    bar: {
      horizontal: true, // Change to true if you want horizontal bars
      barHeight: '99%',
      borderRadius: 2,
    },
  },
  xaxis: {
    categories: selectedBarLabels, // Keep this empty if you do not need labels
    min: 0,
    max:1,
    
    title: {
      text: 'Percentage of Students That Need To Improve In Each Area',
    },
    labels: {formatter: (value) => `${((value) * 100).toFixed(0)}%`},
  },
  yaxis: {
    showAlways: true, // Show y-axis labels
    showEmpty: false,
    // labels: {formatter: (seriesName) => fNumber(seriesName)},
  },

    fill: {
      colors: professionalColors,
    },
    colors: professionalColors,
    legend: {
      show: true,
      position: 'bottom',
      horizontalAlign: 'center',
      fontSize: '14px',
      labels: {
        colors: '#333',
        useSeriesColor: false,
      },
      markers: {
        width: 10,
        height: 10,
        strokeWidth: 0,
        strokeColor: '#fff',
        fillColors: professionalColors,
      },
      itemMargin: {
        horizontal: 10,
        vertical: 5,
      },
      onItemClick: {
        toggleDataSeries: false,
      },
    },
  });

  const chartOptions = useChart({
    chart: {
        events: {
        dataPointSelection: (event, chartContext, opts) => {
          // setSelectedBarData([]);
          // setSelectedBarLabels([]);
          const detailLabels = [];
          const formattedData = [];

          const detailName = opts.w.config.series[opts.seriesIndex].name;
          const barData = details[detailName];
          
          console.log('detail', details)
          console.log('detail name', detailName)
          console.log('barData', barData)

        Object.entries(details).forEach(([key, value]) => {
            if (key === detailName) {
                Object.entries(value).forEach(([key, value]) => {
                    formattedData.push({ name: key, data: [(value / total)] });
                });
            }
        }     
        );
          console.log("formatted", formattedData, "chart", chartSeries);
          
          Object.entries(formattedData).forEach(([key, value]) => {
            console.log('key', key, 'value', value);
            detailLabels.push(value.name);
          });
          setSelectedBarLabels(detailLabels);
          setSelectedBarData(formattedData);

          console.log('detailLabels', detailLabels, 'chartLabels', chartLabels);
          // console.log(detailSeries[0].y);
          // console.log(detailSeries.y);
        },
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
          reset: true, // Or use your custom reset button
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
    fill: professionalColors,
    colors: professionalColors,
      legend: {
      show: true,
      position: 'bottom',
      horizontalAlign: 'center',
      fontSize: '14px',
      labels: {
        colors: '#333', // Customize text color
        useSeriesColor: false, // If you want the legend colors to match the series
      },
      markers: {
        width: 10,
        height: 10,
        strokeWidth: 0,
        strokeColor: '#fff',
        fillColors: professionalColors, // Set marker colors
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
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button onClick={() => handleSort(sortOrder === 'asc' ? 'desc' : 'asc')}>
              Sort {sortOrder === 'asc' ? 'Descending' : 'Ascending'}
            </Button>
          </Box>
          <ReactApexChart type="bar" series={chartSeries} options={chartOptions} height={364} />
          {selectedBarData && selectedBarData.length > 0 && (
            <div>
              <CardHeader title="Additional Details" />
              <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
                <Button onClick={handleDeselect} color="error">
                  Deselect
                </Button>
              </Box>
                <ReactApexChart
                key={selectedBarLabels.join(",") + selectedBarData.length}
                  type="bar"
                  series={selectedBarData}
                  options={detailOptions}
                  height={364}
                />
            </div>
          )}
        </Box>
        <style>{`
          .apexcharts-menu-item.exportSVG {
            display: none;
          }
        `}</style>
        
      </Card>

  );
}