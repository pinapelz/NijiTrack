"use client";
import React, { useState } from "react";
import ChannelRow from "./SubscriberTableRow";

interface ChannelDataProp {
    channel_name: string;
    profile_pic: string;
    subscribers: number;
    sub_org: string;
    video_count: number;
    day_diff: number;
    views: number;
    diff_1d: number;
    diff_7d: number;
    diff_30d: number;
}

interface SubscriberDataTableProp {
    channel_data: ChannelDataProp[];
    timestamp: string;
}

type SortKey = keyof ChannelDataProp | "rank";

const DataTable = ({ channel_data, timestamp }: SubscriberDataTableProp) => {
    const [sortKey, setSortKey] = useState<SortKey>("subscribers");
    const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");
    const [indexName, setIndexName] = useState<string>("RANK");

    const handleSort = (key: SortKey) => {
        if (sortKey === key) {
            setSortOrder(sortOrder === "asc" ? "desc" : "asc");
        } else {
            setSortKey(key);
            setSortOrder("desc");
        }
        if (key === "sub_org") {
            setIndexName("INDEX");
        } else {
            setIndexName("RANK");
        }
    };

    const sortedData = [...channel_data].sort((a, b) => {
        let aValue: any, bValue: any;
        if (sortKey === "rank") {
            aValue = channel_data.indexOf(a) + 1;
            bValue = channel_data.indexOf(b) + 1;
        } else {
            aValue = a[sortKey as keyof ChannelDataProp];
            bValue = b[sortKey as keyof ChannelDataProp];
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
            <div
                className="text-center sm:mt-5"
                style={{ fontFamily: "Quantico, sans-serif" }}
            >
                <h1 className="text-2xl font-bold text-gray-800">
                    Subscriber Count
                </h1>
                <p className="text-gray-500 text-sm">
                    Updated Hourly. Retrieved at: {timestamp}
                </p>
            </div>
            <div className="px-2 sm:px-48 py-4 sm:py-8 relative rounded-l text-left overflow-auto">
                <table className="w-full text-m sm:text-xl text-black bg-white">
                    <thead
                        className="text-m sm:text-lg text-white rounded-md select-none"
                        style={{ backgroundColor: "black" }}
                    >
                        <tr>
                            <th
                                scope="col"
                                className="py-1 px-1 sm:px-3 hidden sm:table-cell"
                            >
                                {indexName}
                            </th>
                            <th
                                scope="col"
                                className="py-1 px-1 sm:px-3"
                            >
                                CHANNEL
                            </th>
                            <th
                                scope="col"
                                className="py-1 px-1 sm:px-3 hidden sm:table-cell cursor-pointer"
                                onClick={() => handleSort("sub_org")}
                            >
                                GROUP
                                {sortKey === "sub_org" && (
                                    <span className="ml-1">{sortOrder === "asc" ? "▲" : "▼"}</span>
                                )}
                            </th>
                            <th
                                scope="col"
                                className="py-1 px-1 sm:px-3 hidden sm:table-cell cursor-pointer"
                                onClick={() => handleSort("video_count")}
                            >
                                VIDEO COUNT
                                {sortKey === "video_count" && (
                                    <span className="ml-1">{sortOrder === "asc" ? "▲" : "▼"}</span>
                                )}
                            </th>
                            <th
                                scope="col"
                                className="py-1 px-1 sm:px-3 hidden sm:table-cell cursor-pointer"
                                onClick={() => handleSort("views")}
                            >
                                VIEW COUNT
                                {sortKey === "views" && (
                                    <span className="ml-1">{sortOrder === "asc" ? "▲" : "▼"}</span>
                                )}
                            </th>
                            <th
                                scope="col"
                                className="py-1 px-1 sm:px-3 cursor-pointer"
                                onClick={() => handleSort("subscribers")}
                            >
                                SUBSCRIBERS
                                {sortKey === "subscribers" && (
                                    <span className="ml-1">{sortOrder === "asc" ? "▲" : "▼"}</span>
                                )}
                            </th>
                            <th
                                scope="col"
                                className="py-1 px-1 sm:px-3"
                                onClick={() => handleSort("diff_1d")}
                            >
                                DIFF (24H)
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {sortedData.map((channel, index) => (
                            <ChannelRow
                                key={index}
                                channel={channel}
                                index={index}
                            />
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