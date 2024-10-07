import SubscriberTable, {
  type SubscriberDataTableProp,
} from "../components/SubscriberTable/SubscriberTable";
import TitleBar from "../components/TitleBar/TitleBar";

async function Home() {
  const graphURL = process.env.NEXT_PUBLIC_GRAPH_URL;
  const data: SubscriberDataTableProp = await getData();
  return (
    <>
      <TitleBar title="PhaseTracker" backgroundColor="black" />
      <div
        className="sm:block hidden mt-4"
        style={{ overflow: "hidden", height: "105vh", position: "relative" }}
      >
        <iframe
          title="Phase Connect Subscriber Count Graph"
          src={graphURL}
          style={{ position: "absolute", top: 0, left: 0 }}
          width="100%"
          height="100%"
        />
      </div>
      <SubscriberTable {...data} />
    </>
  );
}

async function getData() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL_TESTING;
  const endpoint = "/api/subscribers";
  const headers = {
    "Cache-Control": "no-cache",
  };
  const cacheOption = "no-cache";

  const response = await fetch(`${apiUrl}${endpoint}`, {
    headers: headers,
    cache: cacheOption,
  });
  if (!response.ok) {
    console.log(response.statusText);
  }
  return response.json();
}
export default Home;
