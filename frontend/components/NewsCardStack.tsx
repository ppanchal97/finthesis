import React, { useState, useEffect } from 'react';
import NewsCard from './NewsCard';
import { watchlistNews } from './mockData';

const NewsCardStack = ({ onNewsSelect, selectedNewsItem, watchlist }) => {
    const [newsItemsByWatchlist, setNewsItemsByWatchlist] = useState({});

    useEffect(() => {
        let active = true;

        const fetchNewsItems = async () => {
            const items = watchlistNews[watchlist] || [];
            let index = newsItemsByWatchlist[watchlist]?.length || 0;  // Start from the last fetched index

            const addItem = () => {
                if (index < items.length && active) {
                    setNewsItemsByWatchlist(prevItems => ({
                        ...prevItems,
                        [watchlist]: [...(prevItems[watchlist] || []), items[index]]
                    }));
                    index++;
                    setTimeout(addItem, randomInterval());  // Schedule the next item
                }
            };

            addItem();  // Start adding items
        };

        fetchNewsItems();

        return () => {
            active = false;  // Clean up to avoid setting state after unmount
        };
    }, [watchlist]);  // Effect runs when watchlist changes

    const randomInterval = () => Math.floor(Math.random() * (8000 - 2000 + 1) + 2000);

    const displayedNewsItems = newsItemsByWatchlist[watchlist] || [];

    return (
        <div className="overflow-auto h-screen p-4">
            {displayedNewsItems.map((item, index) => (
                <NewsCard
                    key={item.id}
                    newsItem={item}
                    onSelect={() => onNewsSelect(item)}
                    isActive={selectedNewsItem && item.id === selectedNewsItem.id}
                    shouldFlash={index === 0 && (item.portfolio_impact === 'critical' || item.holding_impact === 'critical')}
                />)
            )}
        </div>
    );
};

export default NewsCardStack;
