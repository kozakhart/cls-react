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
  console.log('The chart data', chartData)
  const [selectedBarData, setSelectedBarData] = useState([]);
  const [selectedBarLabels, setSelectedBarLabels] = useState([]);
  const [sortOrder, setSortOrder] = useState('asc');
  const [sortDetailOrder, setDetailSortOrder] = useState('asc');

  const [sortedData, setSortedData] = useState(chartData);
  const [detailSortedData, setDetailSortedData] = useState([]);
  const [detailName, setDetailName] = useState('')
const professionalColors = ['#f45f74','#8fd7d7', '#00b0be', '#ff8ca1', '#bdd373', '#98c127', '#ffcd8e', '#ffb255'];

const handleDeselect = () => {
  setSelectedBarData([]);
  setSelectedBarLabels([]);
};

const handleDetailSort = (order, data) => {
    const sorted = [...data].sort((a, b) => {
        const numA = a.data[0];
        const numB = b.data[0];
        return order === 'asc' ? numA - numB : numB - numA;
    });
    setSelectedBarData(sorted);
    setDetailSortOrder(order);
};


const handleSort = (order, data) => {
  console.log('The data', data)
  const sorted = Object.entries(data)
    .sort(([, a], [, b]) => {
      const numA = Number(a);
      const numB = Number(b);
      return order === 'asc' ? numA - numB : numB - numA;
    })
    .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});

  setSortedData(sorted);
  setSortOrder(order);
};


const handleAlphabeticalSort = (order) => {
  const sortOrderFACT = ['Function', 'Accuracy', 'Content', 'Text'];
  const sortOrderTACT = ['Text', 'Accuracy', 'Content', 'Function'];

  const sortOrder = order === 'asc' ? sortOrderFACT : sortOrderTACT;

  const sorted = Object.entries(sortedData)
    .sort(([keyA], [keyB]) => {
      // Find the index of the primary category
      const indexA = sortOrder.findIndex((word) => keyA.startsWith(word));
      const indexB = sortOrder.findIndex((word) => keyB.startsWith(word));

      // If in the same category, sort alphabetically within the category
      if (indexA === indexB) {
        return keyA.localeCompare(keyB);
      }

      // Otherwise, sort based on the category order
      return indexA - indexB;
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

  console.log('chartLabels', chartLabels);
    console.log('chartSeries', chartSeries);
  
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
      formatter: (value) => `${((value) * 100).toFixed(1)}%`,
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
    categories: selectedBarData.map(item => item.name),
    min: 0,
    max:1,
    
    title: {
      text: 'Average Percentage of Students That Need To Improve In Each Area',
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
          const detailSortedData = []

          const detailName = opts.w.config.series[opts.seriesIndex].name;
          const barData = details[detailName];
          
          setDetailName(detailName)

        Object.entries(details).forEach(([key, value]) => {
            if (key === detailName) {
                Object.entries(value).forEach(([key, value]) => {
                    formattedData.push({ name: key, data: [(value / total)] });
                    detailSortedData[key] = value;
                });
            }
        }     
        );
          
          Object.entries(formattedData).forEach(([key, value]) => {
            detailLabels.push(value.name);
          });
          setSelectedBarLabels(detailLabels);
          setSelectedBarData(formattedData);
          setDetailSortedData(detailSortedData);
          

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
            <Button onClick={() => handleAlphabeticalSort(sortOrder === 'asc' ? 'desc' : 'asc')}>
              FACT Sort
            </Button>
            <Button onClick={() => handleSort(sortOrder === 'asc' ? 'desc' : 'asc', sortedData)}>
              Value Sort
            </Button>
          </Box>
          <ReactApexChart type="bar" series={chartSeries} options={chartOptions} height={364} />
          {selectedBarData && selectedBarData.length > 0 && (
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