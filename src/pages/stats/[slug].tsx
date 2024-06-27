import type { GetServerSideProps } from "next";
import "../../app/globals.css";
import CompactTable from "@/components/CompactTable/CompactTable";
import DataChart from "@/components/DataChart/DataChart";
import Divider from "@/components/Divider/Divider";
import Footer from "@/components/Footer/Footer";
import { ChannelCard } from "@/components/channel-card";
import Head from "next/head";
import TitleBar from "../../components/TitleBar/TitleBar";

interface ChannelDataProp {
	channel_id: string;
	channel_name: string;
	profile_pic: string;
	subscribers: number;
	sub_org: string;
	video_count: number;
	view_count: number;
	next_milestone: string;
	days_until_next_milestone: string;
	next_milestone_date: string;
}

interface GraphDataProp {
	labels: string[];
	datasets: number[];
}

interface CompactTableProps {
	dates: string[];
	milestones: string[];
}

export const getServerSideProps: GetServerSideProps = async (context) => {
	const { slug } = context.params || {};

	const chartData = await getGraphData(slug as string);
	const channelData = await getChannelData(slug as string);
	const sevenDayGraphData = await get7DGraphData(slug as string);
	const milestoneData = await getMilestoneData(slug as string);

	return {
		props: {
			chartData,
			channelData,
			slug,
			sevenDayGraphData,
			milestoneData,
		},
	};
};

function Page({
	chartData,
	channelData,
	sevenDayGraphData,
	slug,
	milestoneData,
}: {
	chartData: GraphDataProp;
	channelData: ChannelDataProp;
	sevenDayGraphData: GraphDataProp;
	slug: string;
	milestoneData: CompactTableProps;
}) {
	console.log(milestoneData);
	return (
		<>
			<Head>
				<title>{slug as string} - PhaseTracker</title>
				<meta
					property="og:title"
					content={`${slug as string} - PhaseTracker`}
				/>
				<meta
					name="description"
					content={`Belonging to ${channelData.sub_org} with ${channelData.subscribers} subscribers`}
				/>
				<meta
					name="og:description"
					content={`${channelData.sub_org} - ${channelData.subscribers}`}
				/>
				<meta property="og:image" content={`${channelData.profile_pic}`} />
				<meta
					name="viewport"
					content="width=device-width, initial-scale=1.0"
				></meta>
				<meta name="author" content="Pinapelz"></meta>
			</Head>
			<TitleBar
				title={slug as string}
				redirectUrl="/"
				showHomeButton
				backgroundColor="black"
			/>
			<div className="flex justify-center">
				<div className="flex flex-col items-center">
					<ChannelCard
						channel_id={channelData.channel_id}
						name={channelData.channel_name}
						avatarUrl={channelData.profile_pic}
						subscriberCount={channelData.subscribers}
						videoCount={channelData.video_count}
						viewCount={channelData.view_count}
						suborg={channelData.sub_org}
						nextMilestone={channelData.next_milestone}
						nextMilestoneDays={channelData.days_until_next_milestone}
						nextMilestoneDate={channelData.next_milestone_date}
					/>
				</div>
			</div>
			<Divider text="Individual Data" />
			<div className="px-48 mb-10 mt-10">
				<div className="mb-12">
					<DataChart
						overrideBGColor="black"
						overrideBorderColor="black"
						chartData={chartData}
					/>
				</div>
				<div className="mb-12">
					<DataChart
						chartData={sevenDayGraphData}
						overrideBGColor="black"
						overrideBorderColor="black"
						graphTitle="7 Day Historical"
					/>
				</div>
				<Divider text="Milestones" />
				<div className="mb-12">
					<CompactTable
						tableData={{
							dates: milestoneData.dates,
							milestones: milestoneData.milestones,
						}}
					/>
					<p className="mt-2 font-semibold">For intervals which we did not record any data, the closest recorded datapoint is chosen</p>
				</div>
			</div>
			<Footer />
		</>
	);
}

async function getGraphData(slug: string) {
	const encodedSlug = encodeURIComponent(slug as string);
	const apiUrl = process.env.NEXT_PUBLIC_API_URL;
	const response = await fetch(apiUrl + `/api/subscribers/${encodedSlug}`, {
		headers: {
			"Cache-Control": "no-cache",
		},
		cache: "no-cache",
	});
	if (!response.ok) {
		console.log(response.statusText);
	}
	return response.json();
}

async function getChannelData(slug: string) {
	const encodedSlug = encodeURIComponent(slug as string);
	const apiUrl = process.env.NEXT_PUBLIC_API_URL;
	const response = await fetch(apiUrl + `/api/channel/${encodedSlug}`, {
		headers: {
			"Cache-Control": "no-cache",
		},
		cache: "no-cache",
	});
	if (!response.ok) {
		console.log(response.statusText);
	}
	return response.json();
}

async function get7DGraphData(slug: string) {
	const encodedSlug = encodeURIComponent(slug as string);
	const apiUrl = process.env.NEXT_PUBLIC_API_URL;
	const response = await fetch(apiUrl + `/api/subscribers/${encodedSlug}/7d`, {
		headers: {
			"Cache-Control": "no-cache",
		},
		cache: "no-cache",
	});
	if (!response.ok) {
		console.log(response.statusText);
	}
	return response.json();
}

async function getMilestoneData(slug: string) {
	const encodedSlug = encodeURIComponent(slug as string);
	const apiUrl = process.env.NEXT_PUBLIC_API_URL;
	const response = await fetch(
		apiUrl + `/api/subscribers/${encodedSlug}/milestones`,
		{
			headers: {
				"Cache-Control": "no-cache",
			},
			cache: "no-cache",
		},
	);
	if (!response.ok) {
		console.log(response.statusText);
	}
	return response.json();
}

export default Page;
