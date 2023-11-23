"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import "../../app/globals.css";
import TitleBar from "../../components/TitleBar/TitleBar";
import { ChannelCard } from "@/components/channel-card";
import DataChart from "@/components/DataChart/DataChart";
import axios from "axios";

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

export default function Page() {
  const [channelData, setChannelData] = useState<ChannelDataProp | null>(null);
  const router = useRouter();
  const { slug } = router.query;
  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    if (slug) {
      const encodedSlug = encodeURIComponent(slug as string);
      console.log(apiUrl + `/api/channel/${encodedSlug}`);
      axios.get(apiUrl + `/api/channel/${encodedSlug}`).then((response) => {
        console.log(response);
        setChannelData(response.data);
      });
    }
  }, [slug]);

  return (
    <>
      <TitleBar title={slug as string} redirectUrl="/" showHomeButton />
      <div className="flex justify-center">
        <div className="flex flex-col items-center">
          {channelData && (
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
          )}
        </div>
      </div>
      <div className="px-48 mb-10 mt-10">
        <div className="mb-12">
          <DataChart channel_name={slug as string}/>
        </div>
        <div className="mb-4">
          <DataChart channel_name={slug as string} requestUrl={`${process.env.NEXT_PUBLIC_API_URL}/api/subscribers/${slug as string}/7d`} graphTitle="7 Day Historical"/>
        </div>
      </div>
    </>
  );
}
