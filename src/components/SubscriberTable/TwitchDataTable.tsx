"use client";
import React, { useState } from "react";
import ChannelRow from "./TwitchTableRow";

interface TwitchChannelDataProp {
    channel_name: string;
    profile_pic: string;
    subscribers: number;
    sub_org: string;
    twitch_followers: number;
    total_sum: number;
    max_following?: number;
}


interface TwitchDataTableProp {
    channel_data: TwitchChannelDataProp[];
    timestamp: string;
}

type SortKey = keyof TwitchChannelDataProp | "rank" | "max_following";

const TwitchDataTable = ({ channel_data, timestamp }: TwitchDataTableProp) => {
    const [sortKey, setSortKey] = useState<SortKey>("twitch_followers");
    const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");
    const [indexName, setIndexName] = useState<string>("RANK");

    const handleSort = (key: SortKey) => {
        if (sortKey === key) {
            setSortOrder(sortOrder === "asc" ? "desc" : "asc");
        } else {
            setSortKey(key);
            setSortOrder("desc");
        }
        setIndexName(key === "sub_org" ? "INDEX" : "RANK");
    };

    const dataWithMax = channel_data.map((channel) => ({
        ...channel,
        max_following: Math.max(
            channel.subscribers || 0,
            channel.twitch_followers || 0
        ),
    }));

    const sortedData = [...dataWithMax].sort((a, b) => {
        let aValue: any, bValue: any;
        if (sortKey === "rank") {
            aValue = dataWithMax.indexOf(a) + 1;
            bValue = dataWithMax.indexOf(b) + 1;
        } else {
            aValue = a[sortKey];
            bValue = b[sortKey];
        }
        if (typeof aValue === "string") {
            return sortOrder === "asc"
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        }
        return sortOrder === "asc" ? aValue - bValue : bValue - aValue;
    });

    return (
        <>
            <div className="sm:hidden text-center text-red-600 font-semibold my-2">
                Limited data shown on mobile view!
            </div>
            <div className="text-center sm:mt-5" style={{ fontFamily: "Quantico, sans-serif" }}>
                <h1 className="text-2xl font-bold text-gray-800">The Twitch Table</h1>
                <p className="text-gray-500 text-sm">Updated Hourly. Retrieved at: {timestamp}</p>
            </div>

            <div className="flex justify-center mt-2 mb-4">
              <div className="bg-gray-100 rounded-lg p-4 shadow-sm text-sm md:text-base max-w-2xl">
                {/* Legend wrapper - stacked sections on all screen sizes */}
                <div className="flex flex-col gap-3">

                  {/* Column explanations */}
                  <div>
                    <h3 className="font-bold text-gray-800 mb-1">Column Explanations</h3>
                    <div>
                      <div className="flex items-start mb-1">
                        <span className="font-medium text-gray-700 mr-2 whitespace-nowrap">SUM(YT+TTV):</span>
                        <span className="text-gray-600">Total combined followers across both platforms</span>
                      </div>
                      <div className="flex items-start">
                        <span className="font-medium text-gray-700 mr-2 whitespace-nowrap">MAX(YT,TTV):</span>
                        <span className="text-gray-600">Highest follower count between platforms</span>
                      </div>
                    </div>
                  </div>

                  {/* Horizontal divider */}
                  <div className="border-t border-gray-300 w-full"></div>

                  {/* Color key */}
                  <div>
                    <h3 className="font-bold text-gray-800 mb-1">MAX Column Color Key</h3>
                    <div>
                      <div className="flex items-center mb-1">
                        <div className="h-3 w-3 bg-red-600 rounded-full mr-2 flex-shrink-0"></div>
                        <span className="text-gray-600">YouTube subscriber count is higher</span>
                      </div>
                      <div className="flex items-center">
                        <div className="h-3 w-3 bg-purple-600 rounded-full mr-2 flex-shrink-0"></div>
                        <span className="text-gray-600">Twitch follower count is higher</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="px-2 sm:px-48 py-4 sm:py-8 relative rounded-l text-left overflow-auto">
                <table className="w-full text-m sm:text-xl text-black bg-white">
                    <thead
                        className="text-m sm:text-lg text-white rounded-md select-none"
                        style={{ backgroundColor: "black" }}
                    >
                        <tr>
                            <th className="py-1 px-1 sm:px-3 hidden sm:table-cell">{indexName}</th>
                            <th className="py-1 px-1 sm:px-3">CHANNEL</th>
                            <th
                                className="py-1 px-1 sm:px-3 hidden sm:table-cell cursor-pointer"
                                onClick={() => handleSort("sub_org")}
                            >
                                GROUP
                                {sortKey === "sub_org" && (
                                    <span className="ml-1">{sortOrder === "asc" ? "▲" : "▼"}</span>
                                )}
                            </th>
                            <th
                                className="py-1 px-1 sm:px-3 cursor-pointer"
                                onClick={() => handleSort("subscribers")}
                            >
                                YOUTUBE SUBS
                                {sortKey === "subscribers" && (
                                    <span className="ml-1">{sortOrder === "asc" ? "▲" : "▼"}</span>
                                )}
                            </th>
                            <th
                                className="py-1 px-1 sm:px-3 cursor-pointer"
                                onClick={() => handleSort("twitch_followers")}
                            >
                                TWITCH FOLLOWS
                                {sortKey === "twitch_followers" && (
                                    <span className="ml-1">{sortOrder === "asc" ? "▲" : "▼"}</span>
                                )}
                            </th>
                            <th
                                className="py-1 px-1 sm:px-3 cursor-pointer hidden sm:table-cell"
                                onClick={() => handleSort("total_sum")}
                            >
                              SUM(YT+TTV)
                                {sortKey === "total_sum" && (
                                    <span className="ml-1">{sortOrder === "asc" ? "▲" : "▼"}</span>
                                )}
                            </th>
                            <th
                                className="py-1 px-1 sm:px-3 cursor-pointer"
                                onClick={() => handleSort("max_following")}
                            >
                                MAX(YT, TTV)
                                {sortKey === "max_following" && (
                                    <span className="ml-1">{sortOrder === "asc" ? "▲" : "▼"}</span>
                                )}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {sortedData.map((channel, index) => (
                            <ChannelRow key={index} channel={channel} index={index} />
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    );
};

export default TwitchDataTable;
export type { TwitchDataTableProp, TwitchChannelDataProp };
