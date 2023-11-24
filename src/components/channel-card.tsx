import { AvatarImage, AvatarFallback, Avatar } from "@/components/ui/avatar"
import { CardTitle, CardHeader, CardContent, Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface ChannelCardProps {
  name: string
  avatarUrl: string
  subscriberCount: number
  videoCount: number
  suborg: string
  nextMilestone: string
  nextMilestoneDays: string
  nextMilestoneDate: string
}

export function ChannelCard(props: ChannelCardProps) {
  const { name, avatarUrl, subscriberCount, videoCount, suborg, nextMilestone, nextMilestoneDays, nextMilestoneDate } = props
  return (
    <Card className="w-[500px] shadow-lg rounded-lg overflow-hidden mt-4 py-4">
      <CardHeader>
        <div className="flex items-center space-x-4 p-4">
          <Avatar>
            <AvatarImage src={avatarUrl}/>
            <AvatarFallback>PR</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle>{name}</CardTitle>
            <Badge variant="secondary">{suborg}</Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent className="px-4 py-2 space-y-4">
        <div className="flex flex-col items-center">
          <span className="text-l text-gray-600">Subscribers</span>
            <span className="font-semibold">{subscriberCount.toLocaleString()}</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-l text-gray-600">Videos</span>
          <span className="font-semibold">{videoCount}</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-l text-gray-600">Next Milestone</span>
          <span className="font-semibold">{nextMilestone.toLocaleString()}</span>
          <div className="flex justify-center items-center">
            <span className="text-sm text-gray-600 px-2">{nextMilestoneDays} days</span>
            <span className="text-sm text-gray-600 px-2">{nextMilestoneDate}</span>
          </div>

        </div>
      </CardContent>
    </Card>
  )
}
