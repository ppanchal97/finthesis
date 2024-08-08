import React, { useState, useEffect, useRef } from 'react';
import NewsCard from './NewsCard';
import { watchlistNews } from './mockData';
import { NewsItem } from '@/types/types';

interface NewsCardStackProps {
    onNewsSelect: (newsItem: NewsItem) => void;
    selectedNewsItem: NewsItem | null;
    watchlist: string;
}

interface NewsItemsByWatchlist {
    [key: string]: NewsItem[];
}

const NewsCardStack: React.FC<NewsCardStackProps> = ({ onNewsSelect, selectedNewsItem, watchlist }) => {
    const [newsItemsByWatchlist, setNewsItemsByWatchlist] = useState<NewsItemsByWatchlist>({});
    const newsItemsByWatchlistRef = useRef<NewsItemsByWatchlist>(newsItemsByWatchlist);
    newsItemsByWatchlistRef.current = newsItemsByWatchlist; // Update ref on state changes

    useEffect(() => {
        let active = true;

        const fetchNewsItems = async () => {
            const items = watchlistNews[watchlist] || [];
            let index = newsItemsByWatchlistRef.current[watchlist]?.length || 0;

            const addItem = () => {
                if (index < items.length && active) {
                    const currentItem = items[index];
                    if (currentItem) {
                        setNewsItemsByWatchlist(prevItems => {
                            const updatedItems = {
                                ...prevItems,
                                [watchlist]: [currentItem, ...(prevItems[watchlist] || [])]  // Prepend new items
                            };
                            newsItemsByWatchlistRef.current = updatedItems; // Keep ref up-to-date
                            return updatedItems;
                        });
                        index++;
                    }
                    setTimeout(addItem, randomInterval());
                }
            };

            addItem();
        };

        fetchNewsItems();

        return () => {
            active = false;
        };
    }, [watchlist]); // Only re-run the effect if watchlist changes

    const randomInterval = () => Math.floor(Math.random() * (8000 - 2000 + 1) + 2000);

    const displayedNewsItems = newsItemsByWatchlist[watchlist] || [];

    return (
        <div className="overflow-auto h-screen p-4">
            {displayedNewsItems.map((newsItem: NewsItem, index: number) => (
                <NewsCard
                    key={newsItem.id}
                    newsItem={newsItem}
                    onSelect={() => onNewsSelect(newsItem)}
                    isActive={!!selectedNewsItem && newsItem.id === selectedNewsItem?.id}
                    shouldFlash={index === 0 && (newsItem.fundamentals_impact === 'critical' || newsItem.thesis_impact === 'critical')}
                />)
            )}
        </div>
    );
};

export default NewsCardStack;
