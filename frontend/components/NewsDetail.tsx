// components/NewsDetail.tsx
import React, { useState } from 'react';
import NewsText from './NewsText';
import QAComponent from './QAComponent';
import NewsDetailHeader from './NewsDetailHeader';
import DraftInvestmentNote from './DraftInvestmentNote';

const NewsDetail = ({ newsItem }) => {
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
                holdingImpact={newsItem.holding_impact} 
                portfolioImpact={newsItem.portfolio_impact} 
                onCreateNote={handleCreateNote}  // Pass the function here
            />
            {showNoteModal && <DraftInvestmentNote onClose={handleCloseNote} />}
            <NewsText title={newsItem.title} description={newsItem.description} fullText={newsItem.full_text} />
            <QAComponent title={newsItem.title} description={newsItem.description} fullText={newsItem.full_text} />
        </div>
    );
};

export default NewsDetail;
