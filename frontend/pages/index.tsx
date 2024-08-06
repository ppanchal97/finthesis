// pages/index.tsx
import React, { useState } from 'react';
import NewsCardStack from '../components/NewsCardStack';
import NewsDetail from '../components/NewsDetail';
import Navbar from '../components/Navbar';
import { NewsItem } from '@/types/types';

const Home: React.FC = () => {
    const [selectedNewsItem, setSelectedNewsItem] = useState<NewsItem | null>(null);
    const [currentWatchlist, setCurrentWatchlist] = useState('Priority');

    const handleNewsSelect = (newsItem: NewsItem) => {
        setSelectedNewsItem(newsItem);
    };

    return (
        <div className="flex min-h-screen">
            <div className="w-1/3 overflow-auto bg-darkgray">
                <Navbar onWatchlistChange={setCurrentWatchlist} />
                <NewsCardStack 
                    onNewsSelect={handleNewsSelect} 
                    selectedNewsItem={selectedNewsItem} 
                    watchlist={currentWatchlist} 
                />
            </div>
            <div className="w-2/3 p-4 bg-black text-white">
                {selectedNewsItem ? (
                    <NewsDetail newsItem={selectedNewsItem} />
                ) : (
                    <p>Please select a news item to view details.</p>
                )}
            </div>
        </div>
    );
};

export default Home;
