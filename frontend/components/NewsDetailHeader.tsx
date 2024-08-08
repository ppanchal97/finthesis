import React from 'react';

interface NewsDetailHeaderProps {
    tickersImpacted: string[];
    holdingImpact: string;
    portfolioImpact: string;
    onCreateNote: () => void;
}

const NewsDetailHeader: React.FC<NewsDetailHeaderProps> = ({
    tickersImpacted,
    holdingImpact,
    portfolioImpact,
    onCreateNote
}) => {
    return (
        <div className="grid grid-cols-3 items-center text-lightblue" style={{ fontFamily: 'Roboto' }}>
            {/* Horizontally aligned tickers */}
            <div className="col-span-1 flex items-center justify-start space-x-2">
                <p className="font-bold text-sm">Impacted Tickers:</p>
                <div className="flex flex-wrap items-center">
                    {tickersImpacted.map((ticker, index) => (
                        <span key={index} className="text-sm mr-2">{ticker}</span>  // Use span for inline display
                    ))}
                </div>
            </div>

            {/* Button to create a note */}
            <div className="col-span-2 flex justify-end">
                <button onClick={onCreateNote} style={{
                    width: '20%',
                    height: '20%',
                    backgroundColor: '#2156E7',
                    color: '#FFFFFF',
                    border: 'none',
                    borderRadius: '10px',
                    cursor: 'pointer'
                }}>
                    Draft Investment Note
                </button>
            </div>
        </div>
    );
};

export default NewsDetailHeader;
