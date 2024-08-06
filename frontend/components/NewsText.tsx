import React from 'react';

interface NewsTextProps {
    title: string;
    description: string;
    fullText: string;
}

const NewsText: React.FC<NewsTextProps> = ({ title, description, fullText }) => {
    return (
        <div>
            <h1 className="text-news-title font-bold text-titleorange" style={{margin: '2%'}}>{title}</h1>
            <p className="text-lg text-white" style={{margin: '2%'}}>{description}</p>
            <div className="text-white" style={{margin: '2%'}}>{fullText}</div>
        </div>
    );
};

export default NewsText;
