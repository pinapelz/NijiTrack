import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface ChannelCardProps {
	channel_id: string;
	name: string;
	avatarUrl: string;
	subscriberCount: number;
	videoCount: number;
	viewCount: number;
	suborg: string;
	nextMilestone: string;
	nextMilestoneDays: string;
	nextMilestoneDate: string;
}

export function ChannelCard(props: ChannelCardProps) {
	const {
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
	} = props;
	return (
		<Card className="w-[500px] shadow-lg rounded-lg overflow-hidden mt-4 py-4">
			<CardHeader>
				<div className="flex items-center space-x-4 p-4">
					<Avatar>
						<AvatarImage src={avatarUrl} />
						<AvatarFallback>PR</AvatarFallback>
					</Avatar>
					<div>
						<a
							className="hover:underline"
							href={`https://youtube.com/channel/${channel_id}`}
						>
							<CardTitle>{name}</CardTitle>
						</a>
						<Badge variant="secondary">{suborg}</Badge>
					</div>
				</div>
			</CardHeader>
			<CardContent className="px-4 py-2 space-y-4">
				<div className="flex flex-col items-center">
					<span className="text-l text-gray-600">Subscribers</span>
					<span className="font-semibold">
						{Number(subscriberCount).toLocaleString()}
					</span>
				</div>
				<div className="flex flex-col items-center">
					<span className="text-l text-gray-600">Videos</span>
					<span className="font-semibold">{videoCount}</span>
				</div>
				<div className="flex flex-col items-center">
					<span className="text-l text-gray-600">View Count</span>
					<span className="font-semibold">
						{Number(viewCount).toLocaleString()}
					</span>
				</div>
				<div className="flex flex-col items-center">
					<span className="text-l text-gray-600">Next Milestone</span>
					<span className="font-semibold">
						{Number(nextMilestone).toLocaleString()}
					</span>
					<div className="flex justify-center items-center">
						<span className="text-sm text-gray-600 px-2">
							{nextMilestoneDays} days
						</span>
						<span className="text-sm text-gray-600 px-2">
							{nextMilestoneDate}
						</span>
					</div>
				</div>
			</CardContent>
		</Card>
	);
}
