// components/Navbar.tsx
import React, { useState } from 'react';
import Image from 'next/image';
import CreateWatchlist from './CreateWatchList';

const Navbar = ({ onWatchlistChange }) => {
    const [showCreateWatchlist, setShowCreateWatchlist] = useState(false);
    const [watchlists, setWatchlists] = useState(['Priority', 'Highlights', 'All', 'Consumer', 'iPhone']);

    const handleCreateWatchlist = () => {
        setShowCreateWatchlist(true);
    };

    const handleClose = (newWatchlistName = '') => {
        if (newWatchlistName && typeof newWatchlistName === 'string' && newWatchlistName.trim() !== "") {
            setWatchlists(currentWatchlists => [...currentWatchlists, newWatchlistName]);
        }
        setShowCreateWatchlist(false);
    };

    return (
        <>
            <div className="bg-inactive-bg p-3 overflow-x-auto whitespace-nowrap">
                {watchlists.map((watchlist, index) => (
                    <button key={index} onClick={() => onWatchlistChange(watchlist)} className="inline-block text-center text-navbar-text mx-2">
                        <span className="text-lightblue font-bold">{watchlist}</span>
                    </button>
                ))}
                <button onClick={handleCreateWatchlist} className="inline-block">
                    <Image src="/plus.svg" alt="Add" width={20} height={20} />
                </button>
            </div>
            {showCreateWatchlist && <CreateWatchlist onClose={handleClose} />}
        </>
    );
};

export default Navbar;
