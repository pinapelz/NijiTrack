import React from 'react';

interface TitleBarProps {
    title: string;
    redirectUrl?: string;
    showHomeButton?: boolean;
}

const TitleBar: React.FC<TitleBarProps> = ({ title, redirectUrl, showHomeButton }) => {
    return (
        <div className="title-bar p-5 shadow-md" style={{ backgroundColor: '#2D4B71' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <a href={redirectUrl}>
                    <span className="text-white text-4xl font-bold">{title}</span>
                </a>
                {showHomeButton && (
                    <a href="/">
                        <button className="bg-white text-blue-500 hover:bg-blue-500 hover:text-white font-bold py-2 px-4 rounded-full">Home</button>
                    </a>
                )}
            </div>
        </div>
    );
};

export default TitleBar;