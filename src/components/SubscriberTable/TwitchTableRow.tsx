"use client";
import Image from "next/image";
import type React from "react";
import type { TwitchChannelDataProp } from "./TwitchDataTable";

interface TwitchRowProps {
	channel: TwitchChannelDataProp;
	index: number;
}

const TwitchTableRow: React.FC<TwitchRowProps> = ({ channel, index }) => (
	<tr
		key={index}
		className="border-b hover:bg-gray-100 cursor-pointer"
		onClick={() => (window.location.href = "/stats/" + channel.channel_name)}
	>
		<td className="py-3 px-1 sm:px-3 hidden sm:table-cell">{index + 1}</td>
		<td className="py-3 px-1 sm:px-3 flex items-center">
			<Image
				src={channel.profile_pic}
				alt={channel.channel_name}
				width={50}
				height={50}
				className="rounded-full"
			/>
			<span className="ml-2 hidden sm:block">{channel.channel_name}</span>
			<span className="ml-2 sm:hidden">{
				(() => {
					const words = channel.channel_name.split(' ');
					if (words.length >= 2) {
						return `${words[0][0]}.${words[1][0]}`;
					} else if (words.length === 1) {
						return `${words[0][0]}.`;
					}
					return '';
				})()
			}</span>
		</td>
		<td className="py-3 px-1 sm:px-3 hidden sm:table-cell">
			{channel.sub_org}
		</td>
		<td className="py-3 px-1 sm:px-3">
			{Number(channel.subscribers).toLocaleString()}
		</td>
		<td className="py-3 px-1 sm:px-3">
			{Number(channel.twitch_followers).toLocaleString()}
		</td>
		<td className="py-3 px-1 sm:px-3 hidden sm:table-cell">
			{Number(channel.total_sum).toLocaleString()}
		</td>
		<td className="py-2 px-3 font-bold">
  {channel.max_following !== undefined && (
    <span
      className={
        channel.twitch_followers > channel.subscribers
          ? "text-purple-500" // Twitch color
          : channel.subscribers > channel.twitch_followers
          ? "text-red-600" // YouTube color
          : ""
      }
    >
      {channel.max_following.toLocaleString() || "0"}
    </span>
  )}
</td>

	</tr>
);

export default TwitchTableRow;
