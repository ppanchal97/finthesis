import React, { useState } from 'react';
import NewsText from './NewsText';
import QAComponent from './QAComponent';
import NewsDetailHeader from './NewsDetailHeader';
import DraftInvestmentNote from './DraftInvestmentNote';
import { NewsItem } from '@/types/types';

interface NewsDetailProps {
    newsItem: NewsItem;
}

const NewsDetail: React.FC<NewsDetailProps> = ({ newsItem }) => {
    const [showNoteModal, setShowNoteModal] = useState(false);

    const handleCreateNote = () => {
        setShowNoteModal(true);
    };

    const handleCloseNote = () => {
        setShowNoteModal(false);
    };

    return (
        <div className="p-4 text-white">
            <NewsDetailHeader
                tickersImpacted={newsItem.tickers_impacted}
                holdingImpact={newsItem.thesis_impact}
                portfolioImpact={newsItem.fundamentals_impact}
                onCreateNote={handleCreateNote}  // Pass the function here
            />
            {showNoteModal && <DraftInvestmentNote onClose={handleCloseNote} />}
            <NewsText title={newsItem.title} description={newsItem.description} fundamentals_impact_text={newsItem.fundamentals_impact_text} thesis_impact_text={newsItem.thesis_impact_text} />
            <QAComponent title={newsItem.title} description={newsItem.description} />
        </div>
    );
};

export default NewsDetail;