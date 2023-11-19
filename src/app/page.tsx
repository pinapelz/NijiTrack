import SubscriberTable, {SubscriberDataTableProp} from './_componenets/SubscriberTable/SubscriberTable';
import TitleBar from './_componenets/TitleBar/TitleBar';

async function Home(){
    const apiUrl = process.env.NEXT_PUBLIC_API_URL
    const data: SubscriberDataTableProp = await getData();
    return(
        <>
            <TitleBar title="Nijitracker" />
            <div className="sm:block hidden mt-4" style={{ overflow: 'hidden', height: '105vh', position: 'relative' }}>
                <iframe src={apiUrl} style={{ position: 'absolute', top: 0, left: 0 }} width="100%" height="100%"></iframe>
            </div>
            <SubscriberTable {...data} />
        </>
    );
}

async function getData(){
    const apiUrl = process.env.NEXT_PUBLIC_API_URL
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