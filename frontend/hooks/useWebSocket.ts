import { useEffect, useState, useCallback } from 'react';
import { NewsItem } from '@/types/types';

export const useWebSocket = (url: string) => {
    const [newsItems, setNewsItems] = useState<NewsItem[]>([]);
    const [socket, setSocket] = useState<WebSocket | null>(null);

    // Handle incoming WebSocket messages
    const handleMessage = useCallback((event: MessageEvent<any>) => {
        const data: NewsItem = JSON.parse(event.data);
        setNewsItems(prevItems => [data, ...prevItems]);
    }, []);

    // Setup WebSocket connection
    useEffect(() => {
        const ws = new WebSocket(url);
        setSocket(ws);
        ws.onmessage = handleMessage;

        return () => {
            ws.close();
        };
    }, [url, handleMessage]);

    return newsItems;
};
