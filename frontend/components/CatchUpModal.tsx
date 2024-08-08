import React, { useState, useEffect } from 'react';
import Image from 'next/image';

interface CatchUpModalProps {
    onClose: () => void;
}

const CatchUpModal: React.FC<CatchUpModalProps> = ({ onClose }) => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setLoading(false);
        }, 4000);  // Wait for 4 seconds

        return () => clearTimeout(timer);  // Clean up the timer
    }, []);

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center p-4 z-50">
            <div className="relative bg-white p-4 rounded-lg" style={{ width: '800px' }}>
                <button onClick={onClose} className="absolute top-2 right-2">
                    <Image src="/close.svg" alt="Close" width={20} height={20} />
                </button>
                <h2 className="font-bold text-xl text-black">Important Events Impacting your Watchlists</h2>
                {loading ? (
                    <div className="flex justify-center items-center">
                    <div className="loader"></div>
                </div>
                ) : (
                    <div className="text-left mt-4">
                        <p><strong>US Economy Ahead Of Personal Consumption Expenditures Price Index Figures Release</strong><br/>
                        Economists and investors eagerly await the release of the latest Personal Consumption Expenditures (PCE) Price Index figures. The data is expected to provide insights into the current state and future direction of the US economy.</p>
                        <p><strong>Shaken Junk-Bond Investors Get Wise to Refinancing Risks, Northern Trust Says</strong><br/>
                        Northern Trust reports that junk-bond investors are becoming more cautious about refinancing risks. This newfound caution is altering strategies and influencing market dynamics.</p>
                        <p><strong>Traders On The Floor Of The New York Stock Exchange As Fed Chair Powell Holds News Conference</strong><br/>
                        Traders on the NYSE floor react to the latest news conference held by Fed Chair Jerome Powell. Powells comments are closely scrutinized for indications of future monetary policy moves.</p>
                        <p><strong>Private Credit Firms Find $1 Trillion Target in Rich Australians</strong><br/>
                        Private credit firms are eyeing wealthy Australians as a new $1 trillion market opportunity. The firms are positioning themselves to tap into this lucrative segment.</p>
                        <p><strong>Penthouse and Facilities at One Barangaroo Crown Residences</strong><br/>
                        The luxurious penthouse and facilities at One Barangaroo Crown Residences attract high-net-worth individuals. The residence offers a blend of opulence and world-class amenities.</p>
                        <p><strong>All About ZiG, Zimbabwe’s Latest Shot at a Stable Currency</strong><br/>
                        Zimbabwe introduces ZiG, a new currency aimed at stabilizing its economy. The government hopes ZiG will address inflation and restore financial confidence.</p>
                        <p><strong>Circulation of Zimbabwes New ZiG Currency</strong><br/>
                        ZiG currency begins circulation in Zimbabwe amidst cautious optimism. Analysts are watching closely to see if this initiative will succeed where previous efforts have failed.</p>
                        <p><strong>Bankrupt WOM’s Bond Bounce Thrusts Billionaire Carlos Slim Into Spotlight</strong><br/>
                        Billionaire Carlos Slim is thrust into the spotlight as WOMs bonds see a surprising rebound. Slims involvement is seen as a pivotal factor in the bonds recovery.</p>
                        <p><strong>Billionaire Carlos Slim Holds Press Conference</strong><br/>
                        Carlos Slim addresses the media in a press conference, discussing his recent financial moves. His insights and strategies are widely followed by the financial community.</p>
                        <p><strong>Argentina Soy-Crush Workers Extend Strike Over Pay to Third Day</strong><br/>
                        Soy-crush workers in Argentina continue their strike over pay, now extending into the third day. The strike is impacting the soybean processing industry and raising concerns about export disruptions.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CatchUpModal;
