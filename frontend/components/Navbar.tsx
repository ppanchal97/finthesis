// components/Navbar.tsx
import React, { useState } from 'react';
import Image from 'next/image';
import CreateWatchlist from './CreateWatchList';
import CatchUpModal from './CatchUpModal';  // Ensure this import

interface NavbarProps {
    onWatchlistChange: (watchlist: any) => void;
}

const Navbar: React.FC<NavbarProps> = ({ onWatchlistChange }) => {
    const [showCreateWatchlist, setShowCreateWatchlist] = useState(false);
    const [showCatchUpModal, setShowCatchUpModal] = useState(false);
    const [watchlists, setWatchlists] = useState(['Priority', 'Highlights', 'All', 'Consumer', 'iPhone']);

    const handleCreateWatchlist = () => {
        setShowCreateWatchlist(true);
    };

    const handleCatchUp = () => {
        setShowCatchUpModal(true);
    };

    const handleClose = (newWatchlistName = '') => {
        if (newWatchlistName && typeof newWatchlistName === 'string' && newWatchlistName.trim() !== "") {
            setWatchlists(currentWatchlists => [...currentWatchlists, newWatchlistName]);
        }
        setShowCreateWatchlist(false);
    };

    const handleCloseCatchUp = () => {
        setShowCatchUpModal(false);
    };

    return (
        <>
            <div className="bg-inactive-bg p-3 overflow-x-auto whitespace-nowrap">
                {watchlists.map((watchlist, index) => (
                    <button key={index} onClick={() => onWatchlistChange(watchlist)} className="inline-block text-center text-navbar-text mx-2">
                        <span className="text-lightblue font-bold">{watchlist}</span>
                    </button>
                ))}
                <button onClick={handleCreateWatchlist} className="inline-block mx-2">
                    <Image src="/plus.svg" alt="Add" width={20} height={20} />
                </button>
                <button onClick={handleCatchUp} className="inline-block mx-2 text-navbar-text bg-blue-500 p-2 rounded-lg">
                    Catch me up
                </button>
            </div>
            {showCreateWatchlist && <CreateWatchlist onClose={handleClose} />}
            {showCatchUpModal && <CatchUpModal onClose={handleCloseCatchUp} />}
        </>
    );
};

export default Navbar;
