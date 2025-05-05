import React from "react";
import "../../app/globals.css";
import TitleBar from "@/components/TitleBar/TitleBar";
import Footer from "@/components/Footer/Footer";
import Head from "next/head";

const About: React.FC = () => {
    return (
        <>
            <Head>
                <title>PhaseTracker - About</title>
                <meta
                    name="description"
                    content="Information and Frequently Asked Questions about PhaseTracker"
                />
            </Head>
            <TitleBar title="About" backgroundColor="black" showHomeButton />
            <div className="max-w-4xl mx-auto p-6">
                <h1 className="text-4xl font-bold text-center mb-8">
                    Information and Frequently Asked Questions
                </h1>
                <div className="space-y-6">
                    <div className="border-b pb-4">
                        <h2 className="text-2xl font-semibold mb-2">
                            What is this?
                        </h2>
                        <p className="text-gray-700">
                            This is PhaseTracker. It tracks the YouTube
                            subscriber count for members of the VTuber group
                            Phase Connect. It is also the primary demo of my
                            boilerplate project,{" "}
                            <a
                                className="text-blue-600 hover:underline"
                                href="https://github.com/pinapelz/NijiTrack&gt;"
                            >
                                NijiTrack
                            </a>{" "}
                            which allows you to setup a subscriber tracker for
                            any subset of YouTube channels (or VTuber
                            organization).
                        </p>
                    </div>
                    <div className="border-b pb-4">
                        <h2 className="text-2xl font-semibold mb-2">
                            Affiliation
                        </h2>
                        <p className="text-gray-700">
                            This project is <strong>not</strong> affiliated with
                            Phase Connect or any of its members. It is also not
                            affiliated with any other VTuber related subscriber
                            tracker (although partially inspired by them).
                        </p>
                    </div>
                    <div className="border-b pb-4">
                        <h2 className="text-2xl font-semibold mb-2">
                            What&apos;s Collected?
                        </h2>
                        <p className="text-gray-700">
                            Some statitics such as video count or channel view
                            count are provided for your convenience. These are
                            generated hourly and are not saved historically{" "}
                            <br />
                            <br />
                            Only subscriber count, channel name, profile picture
                            is saved historically.
                        </p>
                    </div>
                    <div className="border-b pb-4">
                        <h2 className="text-2xl font-semibold mb-2">
                            How often?
                        </h2>
                        <p className="text-gray-700">
                            The data in the tables will update every hour.
                            Historical data is recorded once a day at 12:00 AM
                            PST. This number will then become the next point in
                            the graph.
                        </p>
                    </div>
                    <div className="border-b pb-4">
                        <h2 className="text-2xl font-semibold mb-2">
                            Graduation
                        </h2>
                        <p className="text-gray-700">
                            If someone graduates (no longer active in Phase
                            Connect), their data will be kept in the database
                            but will no longer be updated. The main table will
                            also no longer show a row for them. You&apos;ll
                            still be able to view their data on the main graph
                            on the homepage.
                        </p>
                    </div>
                    <div className="border-b pb-4">
                        <h2 className="text-2xl font-semibold mb-2">
                            Why are there so few datapoints before April 1st
                            2022?
                        </h2>
                        <p className="text-gray-700">
                            This project only started collecting data on April
                            1st, 2022. Any data before that was manually
                            recovered by me through Wayback Machine and various
                            other sources.
                            <br />
                            <br />
                            I&apos;ve done this mostly for appearence sake, so
                            that the graphs can start from the roughly the
                            beginning of the channel&apos;s creation.
                        </p>
                    </div>
                    <div className="border-b pb-4">
                        <h2 className="text-2xl font-semibold mb-2">
                            This new channel&apos;s data point doesn&apos;t
                            start at 0
                        </h2>
                        <p className="text-gray-700">
                            Data is collected hourly. Only
                            &quot;verifiable&quot; datapoints are recorded,
                            it&apos;s hard to catch a channel at exactly 0
                            subsribers. When a new channel debuts, it&apos;ll
                            also take some time for the system to notice that
                            they are a part of Phase Connect.
                        </p>
                        <h3 className="text-xl mt-2 font-semibold mb-2">Note on Phase Invaders</h3>
                        <p className="text-gray-700">
                            Members of Phase Invaders join with already established communities/channels. I initially did backtrack
                            and add some data for original members of Invaders, however going forwardm, there will only be data
                            from the time they join Phase.
                        </p>
                    </div>
                    <div className="border-b pb-4">
                        <h2 className="text-2xl font-semibold mb-2">
                            Tech Stack?
                        </h2>
                        <p className="text-gray-700">
                            Next, Python, and PostgreSQL. The big graph on the
                            homepage is pre-rendered with Plotly, other graphs
                            are made using CanvasJS
                        </p>
                    </div>
                    <div className="border-b pb-4">
                        <h2 className="text-2xl font-semibold mb-2">
                            Can I get the data somehow?
                        </h2>
                        <p className="text-gray-700">
                            An archive of the data is available on{" "}
                            <a
                                className="text-blue-600 hover:underline"
                                href="https://github.com/pinapelz/Phase-Tracker-Data"
                            >
                                GitHub
                            </a>
                            , this is updated on a best-effort basis. A CSV for
                            each channel as well as a full unsorted SQL DML is
                            provided.
                            <br />
                            <br />
                            Please also read the next section
                        </p>
                    </div>
                    <div className="border-b pb-4">
                        <h2 className="text-2xl font-semibold mb-2">
                            A Personal Request
                        </h2>
                        <p className="text-gray-700">
                            I ask that you refrain from using this data to
                            harass or negatively compare the members of Phase
                            Connect or any members in the VTubing community.
                            There is no race, please just enjoy the content.
                            That said, you are free to use this data for any
                            purpose.
                            <br />
                            <br />
                            Phase
                            Connectのメンバーや他のVTuberを嫌がらせたり、否定的に比較したりするために、このデータを使用することはお控えください。これは競争ではありませんので、動画や配信をお楽しみください。このデータはあらゆる目的でご自由にご利用いただけます。
                        </p>
                    </div>
                </div>
            </div>
            <Footer />
        </>
    );
};

export default About;
