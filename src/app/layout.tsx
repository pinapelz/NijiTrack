import { Analytics } from "@vercel/analytics/react";
import type { Metadata } from "next";
import Footer from "../components/Footer/Footer";
import "./globals.css";


export const metadata: Metadata = {
	title: "PhaseTracker - Phase Connect Subscriber Tracker",
	description:
		"PhaseTracker, historical subscriber data for members of Phase Connect",
};

export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<html lang="en">
			<body>
				{children}
				<Footer />
				<Analytics />
			</body>
		</html>
	);
}
