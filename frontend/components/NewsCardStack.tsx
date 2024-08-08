import React, { useState, useEffect } from 'react';
import NewsCard from './NewsCard';
import { watchlistNews } from './mockData';
import { NewsItem } from '@/types/types';

interface NewsCardStackProps {
    onNewsSelect: (newsItem: NewsItem) => void;
    selectedNewsItem: NewsItem | null;
    watchlist: string;
}

// Define a more specific type for storing news items by watchlist
interface NewsItemsByWatchlist {
    [key: string]: NewsItem[];
}

const NewsCardStack: React.FC<NewsCardStackProps> = ({ onNewsSelect, selectedNewsItem, watchlist }) => {
    // Use the defined interface for better type checking
    const [newsItemsByWatchlist, setNewsItemsByWatchlist] = useState<NewsItemsByWatchlist>({});

    useEffect(() => {
        let active = true;

        const fetchNewsItems = async () => {
            const items = watchlistNews[watchlist] || [];
            let index = newsItemsByWatchlist[watchlist]?.length || 0;

            const addItem = () => {
                if (index < items.length && active) {
                    const currentItem = items[index];
                    if (currentItem) {  // Ensure currentItem is defined
                        setNewsItemsByWatchlist(prevItems => ({
                            ...prevItems,
                            [watchlist]: [...(prevItems[watchlist] || []), currentItem]
                        }));
                        index++;
                    }
                    setTimeout(addItem, randomInterval());  // Schedule the next newsItem or attempt, even if currentItem was undefined
                }
            };

            addItem();
        };

        fetchNewsItems();

        return () => {
            active = false;
        };
    }, [watchlist]);  // Note: Including newsItemsByWatchlist in dependency array can cause excessive re-renders

    const randomInterval = () => Math.floor(Math.random() * (8000 - 2000 + 1) + 2000);

    const displayedNewsItems = newsItemsByWatchlist[watchlist] || [];

    return (
        <div className="overflow-auto h-screen p-4">
            {displayedNewsItems.map((newsItem: NewsItem, index: number) => (
                <NewsCard
                    key={newsItem.id}
                    newsItem={newsItem}
                    onSelect={() => onNewsSelect(newsItem)}
                    isActive={!!selectedNewsItem && newsItem.id === selectedNewsItem?.id}  // Ensure this evaluates to boolean
                    shouldFlash={index === 0 && (newsItem.fundamentals_impact === 'critical' || newsItem.thesis_impact === 'critical')}
                />)
            )}
        </div>
    );
};

export default NewsCardStack;
