import React, { useState, useEffect } from 'react';
import { getBalance } from '../api';

const Balance = ({ userAddress }) => {
    const [balance, setBalance] = useState(null);

    useEffect(() => {
        const fetchBalance = async () => {
            const data = await getBalance(userAddress);
            setBalance(data.balance);
        };
        if (userAddress) fetchBalance();
    }, [userAddress]);

    return (
        <div>
            <h2>Balance</h2>
            {balance !== null ? (
                <p>Balance: {balance}</p>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default Balance;
