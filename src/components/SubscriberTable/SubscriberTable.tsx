import React from "react";
import ChannelRow from "./SubscriberTableRow";

interface ChannelDataProp {
	channel_name: string;
	profile_pic: string;
	subscribers: number;
	sub_org: string;
	video_count: number;
	day_diff: number;
	views: number;
}

interface SubscriberDataTableProp {
	channel_data: ChannelDataProp[];
	timestamp: string;
}

const DataTable = ({ channel_data, timestamp }: SubscriberDataTableProp) => {
	if (!channel_data) {
		return null;
	}

	return (
		<>
			<div className="text-center sm:mt-5">
				<h1 className="text-2xl font-bold text-gray-800">Subscriber Count</h1>
				<h2 className="text-xl text-gray-800">Click on a row to view more details!</h2>
				<p className="text-gray-500 text-sm">Updated Hourly. Data Below Retrieved: {timestamp}</p>
			</div>
			<div className="px-2 sm:px-48 py-4 sm:py-8 relative rounded-l text-left overflow-auto">
				<table className="w-full text-m sm:text-xl text-black bg-white">
					<thead
						className="text-m sm:text-lg text-white rounded-md"
						style={{ backgroundColor: "black" }}
					>
						<tr>
							<th
								scope="col"
								className="py-1 px-1 sm:px-3 hidden sm:table-cell"
							>
								RANK
							</th>
							<th scope="col" className="py-1 px-1 sm:px-3">
								CHANNEL
							</th>
							<th
								scope="col"
								className="py-1 px-1 sm:px-3 hidden sm:table-cell"
							>
								GROUP
							</th>
							<th
								scope="col"
								className="py-1 px-1 sm:px-3 hidden sm:table-cell"
							>
								VIDEO COUNT
							</th>
							<th
								scope="col"
								className="py-1 px-1 sm:px-3 hidden sm:table-cell"
							>
								VIEW COUNT
							</th>
							<th scope="col" className="py-1 px-1 sm:px-3">
								SUBSCRIBERS
							</th>
							<th scope="col" className="py-1 px-1 sm:px-3">
								DIFF (24H)
							</th>
						</tr>
					</thead>
					<tbody>
						{channel_data.map((channel, index) => (
							<ChannelRow key={index} channel={channel} index={index} />
						))}
					</tbody>
				</table>
			</div>
		</>
	);
};

export default DataTable;
export type { SubscriberDataTableProp };
export type { ChannelDataProp };
