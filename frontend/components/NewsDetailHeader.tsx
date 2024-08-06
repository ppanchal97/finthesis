import React from 'react';
import ImpactBox from './ImpactBox';

interface NewsDetailHeaderProps {
    holdingImpact: string;
    portfolioImpact: string;
    onCreateNote: () => void;
}

const NewsDetailHeader: React.FC<NewsDetailHeaderProps> = ({ holdingImpact, portfolioImpact, onCreateNote }) => {
    return (
        <div className="grid grid-cols-2 items-center text-lightblue" style={{ fontFamily: 'Roboto' }}>
            <div className="text-lightblue text-2xl font-bold" style={{ fontSize: '26px', lineHeight: '32px' }}>
                Relevant Holdings
            </div>
            <button onClick={onCreateNote} style={{
                width: '50%',
                height: '33px',
                backgroundColor: '#2156E7',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '10px',
                cursor: 'pointer'
            }}>
                Draft Investment Note
            </button>
        </div>
    );
};

export default NewsDetailHeader;
