"use client"
import React from 'react';
import Image from 'next/image';
import { ChannelDataProp } from './SubscriberTable';

interface ChannelRowProps {
    channel: ChannelDataProp;
    index: number;
}

const ChannelRow: React.FC<ChannelRowProps> = ({ channel, index }) => (
<tr key={index} className="border-b hover:bg-gray-100 cursor-pointer" onClick={() => window.location.href = "/stats/"+channel.channel_name}>
        <td className="py-3 px-1 sm:px-3 hidden sm:table-cell">{index + 1}</td>
        <td className="py-3 px-1 sm:px-3 flex items-center">
            <Image
                src={channel.profile_pic}
                alt={channel.channel_name}
                width={50}
                height={50}
                className="rounded-full"
            />
            <span className="ml-2">
                {channel.channel_name}
            </span>
        </td>
        <td className="py-3 px-1 sm:px-3 hidden sm:table-cell">{channel.sub_org}</td>
        <td className="py-3 px-1 sm:px-3 hidden sm:table-cell">{channel.video_count}</td>
        <td className="py-3 px-1 sm:px-3">{Number(channel.subscribers).toLocaleString()}</td>
        <td className="py-3 px-1 sm:px-3">
            {channel.day_diff > 0 ? `+${Number(channel.day_diff).toLocaleString()}` : Number(channel.day_diff).toLocaleString()}
        </td>
    </tr>
);

export default ChannelRow;