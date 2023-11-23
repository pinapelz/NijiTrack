

import React, {useEffect, useState} from 'react';
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





interface Dataset {
  label: string;
  data: number[];
  borderColor: string;
  backgroundColor: string;
}

interface DataChartResponseProps {
  labels: string[];
  datasets: Dataset[];
}

interface DataChartProps {
  channel_name: string;
  requestUrl?: string;
  graphTitle?: string;
}

const DataChart: React.FC<DataChartProps> = ({ channel_name, requestUrl, graphTitle }) => {
  const [data, setData] = useState<DataChartResponseProps | null>();
  const apiUrl = process.env.NEXT_PUBLIC_API_URL

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(requestUrl || `${apiUrl}/api/subscribers/${channel_name}`);
        const json = await response.json();
        setData({
          labels: json.labels,
          datasets: [
            {
              label: 'Subscriber Count',
              data: json.datasets,
              borderColor: 'rgb(255, 99, 132)',
              backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
          ],
        });
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [apiUrl, channel_name, requestUrl]);

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

  if (!data) {
    return <div>Loading...</div>;
  }

  return <Line options={options} data={data} />;
};

export default DataChart;