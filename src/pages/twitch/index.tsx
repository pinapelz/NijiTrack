import { useEffect, useState } from "react";
import TwitchDataTable, {
  type TwitchDataTableProp,
} from "../../components/SubscriberTable/TwitchDataTable";
import TitleBar from "../../components/TitleBar/TitleBar";
import Announcement from "../../components/Announcement";
import "../../app/globals.css";

function TwitchPage() {
  const [twitchData, setTwitchData] = useState<TwitchDataTableProp | null>(null);
  const [error, setError] = useState<string | null>(null);

  const announcementText = process.env.NEXT_PUBLIC_ANNOUNCEMENT;

  useEffect(() => {
    async function fetchTwitchData() {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL_TESTING;
        const endpoint = "/api/twitch";
        const headers = {
          "Cache-Control": "no-cache",
        };
        const cacheOption = "no-cache";

        const response = await fetch(`${apiUrl}${endpoint}`, {
          headers: headers,
          cache: cacheOption,
        });

        if (!response.ok) {
          throw new Error(response.statusText);
        }

        const data = await response.json();
        setTwitchData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      }
    }

    fetchTwitchData();
  }, []);

  return (
    <>
      <TitleBar title="PhaseTracker" backgroundColor="black" />
      {announcementText && (
        <Announcement
          message={announcementText}
          backgroundColor="#e0f7fa"
          textColor="#006064"
        />
      )}
      {error ? (
        <div>Error: {error}</div>
      ) : twitchData ? (
        <TwitchDataTable {...twitchData} />
      ) : (
        <div>Loading...</div>
      )}
    </>
  );
}

export default TwitchPage;
