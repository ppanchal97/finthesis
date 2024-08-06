// components/RelevantHoldings.tsx
import React from 'react';

interface RelevantHoldingsProps {
    holdingsData: {
        ticker: string;
        position: string;
        total_value: string;
        loss_gain: string;
    };
}

const RelevantHoldings: React.FC<RelevantHoldingsProps> = ({ holdingsData }) => {
    return (
        <div>
            <div className="bg-[#0F0F0F] rounded-lg p-4 grid grid-cols-4 gap-4 text-lightblue m-5"
                style={{
                    height: '91px',
                    flexShrink: 0,
                    borderRadius: '10px',
                    margin: '2%',
                }}>
                {/* Ticker */}
                <div className="flex flex-col items-center justify-center">
                    <div className="text-sm font-semibold">Ticker</div>
                    <div>{holdingsData.ticker}</div>
                </div>

                {/* Position */}
                <div className="flex flex-col items-center justify-center">
                    <div className="text-sm font-semibold">Position</div>
                    <div>{holdingsData.position}</div>
                </div>

                {/* Total Value */}
                <div className="flex flex-col items-center justify-center">
                    <div className="text-sm font-semibold">Total Value</div>
                    <div>{holdingsData.total_value}</div>
                </div>

                {/* Loss / Gain */}
                <div className="flex flex-col items-center justify-center">
                    <div className="text-sm font-semibold">Loss / Gain</div>
                    <div>{holdingsData.loss_gain}</div>
                </div>
            </div>
        </div>
    );
};

export default RelevantHoldings;
