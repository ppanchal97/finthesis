import React, { useState } from 'react';
import NewsText from './NewsText';
import QAComponent from './QAComponent';
import NewsDetailHeader from './NewsDetailHeader';
import DraftInvestmentNote from './DraftInvestmentNote';
import TickerDetailView from './TickerDetailView';
import { NewsItem } from '@/types/types';

interface NewsDetailProps {
    newsItem: NewsItem;
}

const NewsDetail: React.FC<NewsDetailProps> = ({ newsItem }) => {
    const [showNoteModal, setShowNoteModal] = useState(false);
    const [showTickerModal, setShowTickerModal] = useState(false);
    const [selectedTicker, setSelectedTicker] = useState('');

    const handleCreateNote = () => setShowNoteModal(true);
    const handleCloseNote = () => setShowNoteModal(false);
    const handleTickerClick = (ticker: string) => {
        setSelectedTicker(ticker);
        setShowTickerModal(true);
    };
    const handleCloseTickerDetail = () => setShowTickerModal(false);

    return (
        <div className="p-4 text-white">
            <NewsDetailHeader
                tickersImpacted={newsItem.tickers_impacted}
                holdingImpact={newsItem.thesis_impact}
                portfolioImpact={newsItem.fundamentals_impact}
                onCreateNote={handleCreateNote}
                onTickerClick={handleTickerClick}
            />
            {showNoteModal && <DraftInvestmentNote onClose={handleCloseNote} />}
            {showTickerModal && <TickerDetailView ticker={selectedTicker} onClose={handleCloseTickerDetail} />}
            <NewsText title={newsItem.title} description={newsItem.description} fundamentals_impact_text={newsItem.fundamentals_impact} thesis_impact_text={newsItem.thesis_impact_text} />
            <QAComponent/>
        </div>
    );
};

export default NewsDetail;