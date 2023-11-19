import React from 'react';
import Image from 'next/image';

interface TitleBarProps {
    title: string;
}

const TitleBar: React.FC<TitleBarProps> = ({ title }) => {
    return (
        <div className="title-bar p-5 shadow-md" style={{ backgroundColor: '#2D4B71' }}>
            <div style={{ width: 'fit-content', whiteSpace: 'nowrap', overflow: 'hidden' }}>
                <span className="text-white text-4xl font-bold">{title}</span>
            </div>
        </div>
    );
};

export default TitleBar;