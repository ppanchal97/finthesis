import React from 'react';
import ImpactBox from './ImpactBox';
import { NewsItem } from '@/types/types';

interface NewsCardProps {
    newsItem: NewsItem;
    onSelect: () => void;
    isActive: boolean;
    shouldFlash: boolean;
}

const NewsCard: React.FC<NewsCardProps> = ({ newsItem, onSelect, isActive, shouldFlash }) => {
    const cardClasses = `rounded-lg p-4 mb-4 cursor-pointer shadow-lg 
                         ${isActive ? 'bg-active-bg text-white' : 'bg-inactive-bg text-gray-500'} 
                         ${shouldFlash ? 'flash-animation' : ''}`;

    return (
        <div className={cardClasses} onClick={onSelect} style={shouldFlash ? { animation: 'flashAnimation 0.5s' } : {}}>
            <div className="flex justify-between">
                <div className="text-xs font-medium opacity-75">{newsItem.timestamp}</div>
            </div>
            <h2 className="text-lg font-bold mt-1">{newsItem.title}</h2>
            <p className="mt-1">{newsItem.description}</p>
            <ImpactDetails newsItem={newsItem} />
        </div>
    );
};

interface ImpactDetailsProps {
    newsItem: NewsItem;
}

const ImpactDetails: React.FC<ImpactDetailsProps> = ({ newsItem }) => {
    return (
        <div className="mt-2">
            <div className="grid grid-cols-4 gap-2 text-xs font-medium uppercase text-gray-400 text-center">
                <div>Fundamentals Impact</div>
                <div>Thesis Impact</div>
                <div>Tickers Impacted</div>
                <div>Source</div>
            </div>
            <div className="grid grid-cols-4 gap-2 mt-1 text-sm text-center">
                <ImpactBox impact={newsItem.holding_impact} />
                <ImpactBox impact={newsItem.portfolio_impact} />
                <div>{newsItem.holdings_impacted.join(", ")}</div>
                <div>{newsItem.source}</div>
            </div>
        </div>
    );
};

export default NewsCard;