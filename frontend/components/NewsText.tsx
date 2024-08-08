import React from 'react';

interface NewsTextProps {
    title: string;
    description: string;
    fundamentals_impact_text: string;
    thesis_impact_text: string;
}

const NewsText: React.FC<NewsTextProps> = ({ title, description, fundamentals_impact_text, thesis_impact_text }) => {
    return (
        <div>
            <h1 className="text-news-title font-bold text-titleorange" style={{margin: '2%'}}>{title}</h1>
            <p className="text-lg text-white" style={{margin: '2%'}}>{description}</p>
            <div className="text-white" style={{margin: '2%'}}>{fundamentals_impact_text}</div>
            <div className="text-white" style={{margin: '2%'}}>{thesis_impact_text}</div>
        </div>
    );
};

export default NewsText;
