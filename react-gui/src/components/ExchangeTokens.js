import React, { useState } from 'react';
import { exchangeTokens } from '../api';

const ExchangeTokens = ({ userAddress }) => {
    const [amount, setAmount] = useState('');
    const [to, setTo] = useState('');

    const handleExchange = async () => {
        await exchangeTokens(to, amount, userAddress);
        alert('Tokens exchanged successfully');
    };

    return (
        <div>
            <h2>Exchange Tokens</h2>
            <input
                type="text"
                placeholder="To (Address)"
                value={to}
                onChange={(e) => setTo(e.target.value)}
            />
            <input
                type="number"
                placeholder="Amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
            />
            <button onClick={handleExchange}>Exchange</button>
        </div>
    );
};

export default ExchangeTokens;
