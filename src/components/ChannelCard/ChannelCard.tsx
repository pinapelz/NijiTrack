import React from 'react';
import Image from 'next/image';
import Countdown from '../Countdown';

type ChannelCardProps = {
  channel_id: string;
  name: string;
  avatarUrl: string;
  subscriberCount: number;
  videoCount: number;
  viewCount: number;
  suborg?: string;
  nextMilestone: string;
  nextMilestoneDays: string;
  nextMilestoneDate: string;
};

const ChannelCard: React.FC<ChannelCardProps> = ({
  channel_id,
  name,
  avatarUrl,
  subscriberCount,
  videoCount,
  viewCount,
  suborg,
  nextMilestone,
  nextMilestoneDays,
  nextMilestoneDate,
}) => {
  return (
    <div className="max-w-4xl w-full mb-4 mt-4 rounded-xl overflow-hidden shadow-lg bg-gradient-to-r from-gray-800 via-gray-900 to-gray-800 p-4 sm:p-8 hover:shadow-2xl transition-all duration-300">
      <div className="flex flex-col sm:flex-row items-center mb-6">
        <Image
          src={avatarUrl}
          alt={name}
          width={80}
          height={80}
          className="rounded-full border-4 border-white"
        />
        <div className="mt-4 sm:mt-0 sm:ml-6 text-center sm:text-left">
          <h3 className="text-xl sm:text-2xl font-bold text-white">
            {name}
          </h3>
          {suborg && (
            <p className="text-sm sm:text-md text-gray-400">
              {suborg}
            </p>
          )}
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-8 text-center mb-6">
        <div>
          <p className="text-lg sm:text-xl font-bold text-white">
            {subscriberCount.toLocaleString()}
          </p>
          <p className="text-xs sm:text-sm text-gray-400">
            Subscribers
          </p>
        </div>
        <div>
          <p className="text-lg sm:text-xl font-bold text-white">
            {videoCount.toLocaleString()}
          </p>
          <p className="text-xs sm:text-sm text-gray-400">
            Videos
          </p>
        </div>
        <div>
          <p className="text-lg sm:text-xl font-bold text-white">
            {viewCount.toLocaleString()}
          </p>
          <p className="text-xs sm:text-sm text-gray-400">
            Views
          </p>
        </div>
      </div>
      <div className="bg-gray-700 rounded-lg p-4 sm:p-0 mb-6">
        <p className="text-md sm:text-lg font-semibold text-white">
          Next Milestone: {Number(nextMilestone).toLocaleString()}
        </p>
        <p className="text-xs sm:text-sm text-gray-300">
          Estimated Date: {nextMilestoneDate}
        </p>
        <div className="flex justify-center sm:p-2">
          <Countdown targetDate={nextMilestoneDate} />
        </div>
      </div>
      <button
        onClick={() => window.open(`https://youtube.com/channel/${channel_id}`, '_blank')}
        className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200"
      >
        View Channel on YouTube
      </button>
    </div>
  );
};

export default ChannelCard;