"use client";
import type React from "react";
import "../TitleBar/TitleBarStyle.css";
import {
    faHouse,
    faBars,
    faTimes,
    faChevronDown,
    faChevronUp,
    faSpinner,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState, useEffect } from "react";
import Link from "next/link";

interface TitleBarProps {
    title: string;
    redirectUrl?: string;
    showHomeButton?: boolean;
    backgroundColor?: string;
}

const TitleBar: React.FC<TitleBarProps> = ({
    title,
    redirectUrl,
    showHomeButton,
    backgroundColor,
}) => {
    const hideFromSidebar = ["Fuura Yuri"]; // List of names to hide (e.g., due to graduation)
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [isMounted, setIsMounted] = useState(false);
    const [groupingData, setPhaseData] = useState<{
        [key: string]: string[];
    } | null>(null);
    const [collapsedSections, setCollapsedSections] = useState<{
        [key: string]: boolean;
    }>({});
    const [loadingMember, setLoadingMember] = useState<string | null>(null);

    useEffect(() => {
        setIsMounted(true);
        const fetchPhaseData = async () => {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL_TESTING;
            try {
                const response = await fetch(apiUrl + "/api/groups");
                const data = await response.json();
                setPhaseData(data);
                const initialCollapsedState = Object.keys(data).reduce(
                    (acc, phase) => {
                        acc[phase] = true;
                        return acc;
                    },
                    {} as { [key: string]: boolean },
                );
                setCollapsedSections(initialCollapsedState);
            } catch (error) {
                console.error("Error fetching phase data:", error);
            }
        };

        fetchPhaseData();
    }, []);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    const toggleSection = (phase: string) => {
        setCollapsedSections((prevState) => ({
            ...prevState,
            [phase]: !prevState[phase],
        }));
    };

    const handleMemberClick = (member: string) => {
        setLoadingMember(member);
    };

    if (!isMounted) {
        return null;
    }

    return (
        <>
            <div
                className="title-bar p-5 shadow-md"
                style={{ backgroundColor: backgroundColor || "#2D4B71" }}
            >
                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                    }}
                >
                    <button
                        onClick={toggleSidebar}
                        className="text-white text-3xl mr-4 focus:outline-none"
                    >
                        <FontAwesomeIcon
                            icon={isSidebarOpen ? faTimes : faBars}
                        />
                    </button>
                    <a href={redirectUrl}>
                        <span
                            className="text-white text-4xl font-bold"
                            style={{ fontFamily: "Quantico, sans-serif" }}
                        >
                            {title}
                        </span>
                    </a>
                    {showHomeButton && (
                        <a href="/" className="ml-2 text-white text-3xl">
                            <FontAwesomeIcon icon={faHouse} />
                        </a>
                    )}
                </div>
            </div>

            {/* Sidebar */}
            <div
                className={`fixed top-0 left-0 h-screen bg-black text-white shadow-lg transition-transform transform ${
                    isSidebarOpen ? "translate-x-0" : "-translate-x-full"
                } duration-500 ease-in-out z-50`}
                style={{
                    width: "16rem",
                    fontFamily: "Quantico, sans-serif",
                    overflowY: "auto",
                }}
            >
                <div className="p-4 text-3xl font-bold border-b border-gray-700">
                    PhaseTracker
                </div>
                <ul className="text-xl border-b border-gray-700">
                    <Link href="/">
                        <li className="p-4 hover:bg-gray-700 transition-colors duration-300">
                            Home
                        </li>
                    </Link>
                    <Link href="/about">
                        <li className="p-4 hover:bg-gray-700 transition-colors duration-300">
                            About
                        </li>
                    </Link>
                </ul>

                <ul className="mt-4 text-xl">
                    {groupingData ? (
                        Object.entries(groupingData).map(([group, members]) => (
                            <li key={group} className="p-4">
                                <div
                                    className="flex justify-between items-center cursor-pointer select-none"
                                    onClick={() => toggleSection(group)}
                                >
                                    <span className="font-bold text-lg">
                                        {group}
                                    </span>
                                    <FontAwesomeIcon
                                        icon={
                                            collapsedSections[group]
                                                ? faChevronDown
                                                : faChevronUp
                                        }
                                    />
                                </div>
                                {!collapsedSections[group] && (
                                    <ul className="ml-4 mt-2">
                                        {members
                                            .filter(
                                                (member) =>
                                                    !hideFromSidebar.includes(
                                                        member,
                                                    ),
                                            )
                                            .map((member) => (
                                                <a
                                                    href={`/stats/${member}`}
                                                    key={member}
                                                >
                                                    <li
                                                        className="p-1 hover:bg-gray-700 transition-colors duration-300 flex items-center"
                                                        onClick={() =>
                                                            handleMemberClick(
                                                                member,
                                                            )
                                                        }
                                                    >
                                                        {member}
                                                        {loadingMember ===
                                                            member && (
                                                            <FontAwesomeIcon
                                                                icon={faSpinner}
                                                                spin
                                                                className="ml-2"
                                                            />
                                                        )}
                                                    </li>
                                                </a>
                                            ))}
                                    </ul>
                                )}
                            </li>
                        ))
                    ) : (
                        <li className="p-4">Loading...</li>
                    )}
                </ul>
            </div>
            {isSidebarOpen && (
                <div
                    className="fixed top-0 left-0 w-full h-full bg-black opacity-50 transition-opacity duration-500"
                    style={{ zIndex: 40 }}
                    onClick={toggleSidebar}
                ></div>
            )}
        </>
    );
};

export default TitleBar;
