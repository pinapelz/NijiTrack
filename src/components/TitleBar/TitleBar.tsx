import React from 'react';
import '../TitleBar/TitleBarStyle.css'

interface TitleBarProps {
    title: string;
    redirectUrl?: string;
    showHomeButton?: boolean;
    backgroundColor?: string;
}

const TitleBar: React.FC<TitleBarProps> = ({ title, redirectUrl, showHomeButton, backgroundColor }) => {
    return (
        <>
            <div className="title-bar p-5 shadow-md" style={{ backgroundColor: backgroundColor || '#2D4B71' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <a href={redirectUrl}>
                        <span className="text-white text-4xl font-bold" style={{ fontFamily: 'Quantico, sans-serif' }}>{title}</span>
                    </a>
                    {showHomeButton && (
                        <a href="/">
                            <button className="bg-white text-black font-bold py-2 px-4 rounded-lg">Home</button>
                        </a>
                    )}
                </div>
            </div>
        </>
    );
};

export default TitleBar;