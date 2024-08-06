import React, { useState } from 'react';
import CreatableSelect from 'react-select/creatable';
import { GroupBase, OptionsOrGroups, } from "react-select";
import Image from 'next/image';

interface CreateWatchListProps {
    onClose: (watchlistName?: string) => void;  // Update to accept an optional string
}

interface OptionType {
    label: string;
    value: string;
}

const CreateWatchList: React.FC<CreateWatchListProps> = ({ onClose }) => {
    const [selectedTickers, setSelectedTickers] = useState([]);
    const [watchlistName, setWatchlistName] = useState('');
    const [selectedWebsites, setSelectedWebsites] = useState([]);
    const [selectedTwitterAccounts, setSelectedTwitterAccounts] = useState([]);
    const [investmentThesis, setInvestmentThesis] = useState('');

    const tickerOptions: OptionsOrGroups<OptionType, GroupBase<OptionType>> = [
        { value: 'Ticker 1', label: 'Ticker 1' },
    ];

    const websiteOptions: OptionsOrGroups<OptionType, GroupBase<OptionType>> = [
        { value: 'website1.com', label: 'website1.com' },
        { value: 'website2.com', label: 'website2.com' },
        // More predefined website options can be listed here
    ];

    const twitterOptions: OptionsOrGroups<OptionType, GroupBase<OptionType>> = [
        { value: 'twitter1', label: '@twitter1' },
        { value: 'twitter2', label: '@twitter2' },
        // More predefined Twitter options can be listed here
    ];

    const handleTickersChange = (selectedOptions: any) => {
        setSelectedTickers(selectedOptions || []);
    };

    const handleWebsiteChange = (selectedOptions: any) => {
        setSelectedWebsites(selectedOptions || []);
    };

    const handleTwitterAccountChange = (selectedOptions: any) => {
        setSelectedTwitterAccounts(selectedOptions || []);
    };

    const handleSave = () => {
        console.log("Saving Watchlist:", watchlistName);
        if (watchlistName.trim()) {
            onClose(watchlistName);  // Pass the watchlist name back to Navbar if not empty
        } else {
            onClose();  // Close without parameters if no name was provided
        }
    };

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="relative bg-white p-4 rounded-lg" style={{ width: '800px' }}>
                <button onClick={() => onClose()} className="absolute top-2 right-2">
                    <Image src="/close.svg" alt="Close" width={20} height={20} />
                </button>
                <h2 className="font-bold text-xl">Create New Watchlist</h2>
                <input
                    type="text"
                    value={watchlistName}
                    onChange={(e) => setWatchlistName(e.target.value)}
                    className="border p-2 w-full mb-4"
                    placeholder="Watchlist Name"
                />
                <section className="mb-4">
                    <h3 className="font-bold text-xl">Tickers to Monitor</h3>
                    <CreatableSelect
                        isMulti
                        options={tickerOptions}
                        value={selectedTickers}
                        onChange={handleTickersChange}
                        placeholder="Add or select US stock Tickers..."
                    />
                </section>
                <section className="mb-4">
                    <h3 className="font-bold text-xl">Streaming Data Sources</h3>
                    <div className="flex flex-col">
                        <label><input type="checkbox" name="bloomberg" /> Bloomberg News & Events Stream</label>
                        <label><input type="checkbox" name="dowJones" /> Dow Jones News Wire</label>
                        <label><input type="checkbox" name="cnn" /> CNN News Wire</label>
                        <label><input type="checkbox" name="ap" /> AP News Wire</label>
                    </div>
                </section>
                <section className="mb-4">
                    <h3 className="font-bold text-xl">Web Pages</h3>
                    <CreatableSelect
                        isMulti
                        options={websiteOptions}
                        value={selectedWebsites}
                        onChange={handleWebsiteChange}
                        placeholder="Add or select websites..."
                    />
                </section>
                <section className="mb-4">
                    <h3 className="font-bold text-xl">Twitter Accounts</h3>
                    <CreatableSelect
                        isMulti
                        options={twitterOptions}
                        value={selectedTwitterAccounts}
                        onChange={handleTwitterAccountChange}
                        placeholder="Add or select Twitter accounts..."
                    />
                </section>
                <section className="mb-4">
                    <h3 className="font-bold text-xl">Investment Thesis</h3>
                    <textarea
                        value={investmentThesis}
                        onChange={(e) => setInvestmentThesis(e.target.value)}
                        className="border p-2 w-full h-40"  // Set height to 40 to make it a large text box
                        placeholder="Enter your investment thesis here..."
                    />
                </section>
                <section className="mb-4">
                    <h3 className="font-bold text-xl">Fundamental Data Point Sources</h3>
                    <div className="flex flex-col">
                        <label><input type="checkbox" name="sec" /> SEC Filings</label>
                        <label><input type="checkbox" name="bills_of_lading" /> Bills of Lading</label>
                        <label><input type="checkbox" name="cash_flow_statements" /> Cash Flow Statements</label>
                        <label><input type="checkbox" name="income_statements" /> Income Statements</label>
                        <label><input type="checkbox" name="balance_sheets" /> Balance Sheets</label>
                        <label><input type="checkbox" name="quarterly_reports" /> Quarterly Reports</label>
                        <label><input type="checkbox" name="earnings_reports" /> Earnings Reports</label>
                        <label><input type="checkbox" name="earnings_transcripts" /> Earnings Transcripts</label>
                        <label><input type="checkbox" name="credit_reports" /> Credit Reports</label>
                        <label><input type="checkbox" name="audit_reports" /> Audit Reports</label>
                        <label><input type="checkbox" name="sustainability_reports" /> Sustainability Reports</label>
                        <label><input type="checkbox" name="risk_assessments" /> Risk Assessments</label>
                        <label><input type="checkbox" name="industry_analyses" /> Industry Analyses</label>
                    </div>
                </section>

                <button onClick={handleSave} className="mt-2 p-2 bg-blue-500 text-white rounded">
                    Save
                </button>
            </div>
        </div>
    );
};

export default CreateWatchList;
