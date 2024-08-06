import React, { useState, useEffect } from 'react';
import Image from 'next/image';

interface DraftInvestmentNoteProps {
    onClose: () => void;
}

const DraftInvestmentNote: React.FC<DraftInvestmentNoteProps> = ({ onClose }) => {
    const initialNoteText = `- Boeing's quarterly earnings report for the period ending July 31, 2024, has highlighted significant challenges for the aerospace giant. \n- The company reported a wider-than-expected loss, surpassing analyst forecasts and underscoring ongoing financial struggles.\n- Revenue also fell short of expectations, with both the commercial airplane and defense divisions contributing to the underperformance.\n- The report reveals that Boeing continues to grapple with safety and manufacturing issues, which are affecting the timely delivery of new aircraft.\n- These issues are a continuation of problems that have plagued the company for several years. Compounding these difficulties`;

    const [noteText, setNoteText] = useState(initialNoteText);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setLoading(false);
        }, 4000);  // Wait for 4 seconds

        return () => clearTimeout(timer);  // Clean up the timer
    }, []);

    const handleSave = () => {
        console.log("Saving Investment Note:", noteText);
        onClose(); // Close modal after saving
    };

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="relative bg-white p-4 rounded-lg" style={{ width: '800px' }}>
                <button onClick={onClose} className="absolute top-2 right-2">
                    <Image src="/close.svg" alt="Close" width={20} height={20} />
                </button>
                <h2 className="font-bold text-xl text-black">Draft Investment Note</h2>
                {loading ? (
                    <div className="flex justify-center items-center">
                        <div className="loader"></div>
                    </div>
                ) : (
                    <>
                        <textarea
                            value={noteText}
                            onChange={(e) => setNoteText(e.target.value)}
                            className="border p-2 w-full h-40 text-black"
                            placeholder="Write your investment note here..."
                        />
                        <button onClick={handleSave} className="mt-2 p-2 bg-blue-500 text-white rounded">
                            Save Note
                        </button>
                    </>
                )}
            </div>
        </div>
    );
};

export default DraftInvestmentNote;
