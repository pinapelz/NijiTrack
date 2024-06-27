import type React from "react";
import "../TitleBar/TitleBarStyle.css";
import { faHouse } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

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
					<a href={redirectUrl}>
						<span
							className="text-white text-4xl font-bold"
							style={{ fontFamily: "Quantico, sans-serif" }}
						>
							{title}
						</span>
					</a>
					{showHomeButton && (
						<a href="/" className="text-white text-3xl">
							<FontAwesomeIcon icon={faHouse} />
						</a>
					)}
				</div>
			</div>
		</>
	);
};

export default TitleBar;
