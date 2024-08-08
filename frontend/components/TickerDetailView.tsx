// components/TickerDetailView.tsx
import React from 'react';
import Image from 'next/image';

interface TickerDetailViewProps {
    ticker: string;
    onClose: () => void;
}

const TickerDetailView: React.FC<TickerDetailViewProps> = ({ ticker, onClose }) => {
    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center p-4 z-50">
            <div className="relative bg-white p-4 rounded-lg" style={{ width: '800px' }}>
                <button onClick={onClose} className="absolute top-2 right-2">
                    <Image src="/close.svg" alt="Close" width={20} height={20} />
                </button>
                <h2 className="font-bold text-xl text-black">Ticker Details: {ticker}</h2>
                {/* Placeholder for more detailed content */}
                <p>Details about {ticker} would go here...</p>
            </div>
        </div>
    );
};

export default TickerDetailView;
