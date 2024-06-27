import {
	CategoryScale,
	Chart as ChartJS,
	Legend,
	LineElement,
	LinearScale,
	PointElement,
	Title,
	Tooltip,
} from "chart.js";
import type React from "react";
import { Line } from "react-chartjs-2";

ChartJS.register(
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend,
);

interface DataChartProps {
	chartData?: any;
	graphTitle?: string;
	fullData?: boolean;
	overrideBorderColor?: string;
	overrideBGColor?: string;
}

const DataChart: React.FC<DataChartProps> = ({
	chartData,
	graphTitle,
	fullData,
	overrideBGColor,
	overrideBorderColor,
}) => {
	const options = {
		responsive: true,
		plugins: {
			legend: {
				position: "top" as const,
			},
			title: {
				display: true,
				text: graphTitle || "Historical Subscriber Data",
				font: {
					size: 18,
				},
			},
		},
		scales: {
			x: {
				ticks: {
					autoSkip: true,
					maxTicksLimit: 10,
				},
			},
		},
	};

	const data = {
		labels: chartData.labels,
		datasets: [
			{
				label: "Subscriber Count",
				data: chartData.datasets,
				borderColor: overrideBorderColor || "rgb(255, 99, 132)",
				backgroundColor: overrideBGColor || "rgba(255, 99, 132, 0.5)",
			},
		],
	};

	if (!fullData) {
		return <Line options={options} data={data} />;
	} else {
		return <Line options={options} data={chartData} />;
	}
};

export default DataChart;
