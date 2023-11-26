import { GetServerSideProps } from "next";
import "../../app/globals.css";
import TitleBar from "../../components/TitleBar/TitleBar";
import { ChannelCard } from "@/components/channel-card";
import DataChart from "@/components/DataChart/DataChart";
import Footer from "@/components/Footer/Footer";

interface ChannelDataProp {
  channel_name: string;
  profile_pic: string;
  subscribers: number;
  sub_org: string;
  video_count: number;
  next_milestone: string;
  days_until_next_milestone: string;
  next_milestone_date: string;
}

interface GraphDataProp{
  labels: string[];
  datasets: number[];
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { slug } = context.params || {};

  const chartData = await getGraphData(slug as string);
  const channelData = await getChannelData(slug as string);
  const sevenDayGraphData = await get7DGraphData(slug as string);

  return {
    props: {
      chartData,
      channelData,
      slug,
      sevenDayGraphData
    },
  };
};

function Page({ chartData, channelData, sevenDayGraphData, slug }: { chartData: GraphDataProp, channelData: ChannelDataProp, sevenDayGraphData: GraphDataProp, slug: string }) {
  return (
    <>
      <TitleBar title={slug as string} redirectUrl="/" showHomeButton backgroundColor="black" />
      <div className="flex justify-center">
        <div className="flex flex-col items-center">
            <ChannelCard
              name={channelData.channel_name}
              avatarUrl={channelData.profile_pic}
              subscriberCount={channelData.subscribers}
              videoCount={channelData.video_count}
              suborg={channelData.sub_org}
              nextMilestone={channelData.next_milestone}
              nextMilestoneDays={channelData.days_until_next_milestone}
              nextMilestoneDate={channelData.next_milestone_date}
            />
        </div>
      </div>
      <div className="px-48 mb-10 mt-10">
        <div className="mb-12">
          <DataChart overrideBGColor="black" overrideBorderColor="black" chartData={chartData}/>
        </div>
        <div className="mb-12">
          <DataChart chartData={sevenDayGraphData} overrideBGColor="black" overrideBorderColor="black" graphTitle="7 Day Historical"/>
        </div>
      </div>
      <Footer />
    </>
  );
}

async function getGraphData(slug: string){
  const encodedSlug = encodeURIComponent(slug as string);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL
  const response = await fetch(apiUrl+`/api/subscribers/${encodedSlug}`, {
      headers: {
          'Cache-Control': 'no-cache'
      },
      cache: 'no-cache'
  });
  if(!response.ok){
      console.log(response.statusText);
  }
  return response.json();
}

async function getChannelData(slug: string){
  const encodedSlug = encodeURIComponent(slug as string);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL
  const response = await fetch(apiUrl+`/api/channel/${encodedSlug}`, {
      headers: {
          'Cache-Control': 'no-cache'
      },
      cache: 'no-cache'
  });
  if(!response.ok){
      console.log(response.statusText);
  }
  return response.json();
}

async function get7DGraphData(slug: string){
  const encodedSlug = encodeURIComponent(slug as string);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL
  const response = await fetch(apiUrl+`/api/subscribers/${encodedSlug}/7d`, {
      headers: {
          'Cache-Control': 'no-cache'
      },
      cache: 'no-cache'
  });
  if(!response.ok){
      console.log(response.statusText);
  }
  return response.json();
}


export default Page;
