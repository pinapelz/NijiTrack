import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';


ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);


interface DataChartProps {
  channel_name?: string;
  chartData?: any;
  graphTitle?: string;
}

const DataChart: React.FC<DataChartProps> = ({ channel_name, chartData, graphTitle }) => {
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: graphTitle || 'Historical Subscriber Data',
        font: {
          size: 18
        }
      },
    },
    scales: {
      x: {
        ticks: {
          autoSkip: true,
          maxTicksLimit: 10
        }
      }
    }
  };

  const data = {
    labels: chartData.labels,
    datasets: [
      {
        label: 'Subscriber Count',
        data: chartData.datasets,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  }


  return <Line options={options} data={data} />;
};

export default DataChart;