import TwitchDataTable, {
  type TwitchDataTableProp,
} from "../../components/SubscriberTable/TwitchDataTable";
import TitleBar from "../../components/TitleBar/TitleBar";
import Announcement from "../../components/Announcement";
import "../../app/globals.css";

type Props = {
  data: TwitchDataTableProp;
  graphURL: string | undefined;
  announcementText: string | undefined;
};

function TwitchPage({ data, graphURL, announcementText }: Props) {
  return (
    <>
      <TitleBar title="PhaseTracker" backgroundColor="black" />
      <TwitchDataTable {...data} />
    </>
  );
}

export async function getServerSideProps() {
  const graphURL = process.env.NEXT_PUBLIC_TWITCH_GRAPH_URL;
  const announcementText = process.env.NEXT_PUBLIC_ANNOUNCEMENT;
  const apiUrl = process.env.NEXT_PUBLIC_API_URL_TESTING;
  const endpoint = "/twitch.json";
  const headers = {
    "Cache-Control": "no-cache",
  };
  const cacheOption = "no-cache";

  const response = await fetch(`${apiUrl}${endpoint}`, {
    headers: headers,
    cache: cacheOption,
  });
  let data = {};
  if (response.ok) {
    data = await response.json();
  } else {
    console.log(response.statusText);
  }

  return {
    props: {
      data,
      graphURL: graphURL ?? null,
      announcementText: announcementText ?? null,
    },
  };
}

export default TwitchPage;