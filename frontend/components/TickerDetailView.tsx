import React from 'react';
import Image from 'next/image';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
  ChartData
} from 'chart.js';

// Register the necessary components for the chart
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface TickerDetailViewProps {
    ticker: string;
    onClose: () => void;
}

const options: ChartOptions<"line"> = {
  responsive: true,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  scales: {
    y: {
      type: 'linear',
      display: true,
      position: 'left',
    },
    y1: {
      type: 'linear',
      display: true,
      position: 'right',
      grid: {
        drawOnChartArea: false,
      },
    },
  }
};

const labels = ['January', 'February', 'March', 'April', 'May', 'June'];

const data: ChartData<"line"> = {
    labels,
    datasets: [
      {
        label: 'Validations',
        data: [10, 9, 15, 30, 50, 70],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        yAxisID: 'y',
      },
      {
        label: 'Invalidations',
        data: [70, 28, 63, 47, 20, 15],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        yAxisID: 'y1',
      }
    ],
  };

const TickerDetailView: React.FC<TickerDetailViewProps> = ({ ticker, onClose }) => {
    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center p-4 z-50">
            <div className="relative bg-white p-4 rounded-lg" style={{ width: '800px' }}>
                <button onClick={onClose} className="absolute top-2 right-2">
                    <Image src="/close.svg" alt="Close" width={20} height={20} />
                </button>
                <h2 className="font-bold text-xl text-black">Ticker Details: {ticker}</h2>
                <div className="my-4">
                    <Line options={options} data={data} />
                </div>
            </div>
        </div>
    );
};

export default TickerDetailView;
