import React from "react";

interface AnnouncementProps {
    message: string;
    backgroundColor?: string;
    textColor?: string;
}

const Announcement: React.FC<AnnouncementProps> = ({
    message,
    backgroundColor = "#f8d7da",
    textColor = "#721c24",
}) => {
    return (
        <div
            className={`p-4 rounded-lg text-center font-bold`}
            style={{
                backgroundColor,
                color: textColor,
            }}
        >
            {message}
        </div>
    );
};

export default Announcement;
