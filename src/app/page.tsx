import SubscriberTable, {SubscriberDataTableProp} from '../components/SubscriberTable/SubscriberTable';
import TitleBar from '../components/TitleBar/TitleBar';

async function Home(){
    const graphURL = process.env.NEXT_PUBLIC_GRAPH_URL
    const data: SubscriberDataTableProp = await getData();
    return(
        <>
            <TitleBar title="PhaseTracker" backgroundColor='black' />
            <div className="sm:block hidden mt-4" style={{ overflow: 'hidden', height: '105vh', position: 'relative' }}>
                <iframe src={graphURL} style={{ position: 'absolute', top: 0, left: 0 }} width="100%" height="100%"></iframe>
            </div>
            <SubscriberTable {...data} />
        </>
    );
}

async function getData(){
    const apiUrl = process.env.NEXT_PUBLIC_API_URL_TESTING
    const response = await fetch(apiUrl+'/api/subscribers', {
        headers: {
            'Cache-Control': 'no-cache'
        },
        cache: 'no-cache'
    });
    if(!response.ok){
        console.log(response.statusText);
    }
    return response.json();
}
export default Home;