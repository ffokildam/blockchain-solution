import React, { useState } from 'react';
import { mintTokens } from '../api';

const Admin = ({ userAddress, setUserAddress }) => {
    const [newAddress, setNewAddress] = useState('');

    const handleChangeAddress = () => {
        if (newAddress) {
            setUserAddress(newAddress);  // Update the remembered address in the state
            alert('Address updated successfully!');
        } else {
            alert('Please enter a valid address');
        }
    };

    const handleMintTokens = async (recipientAddress, amount) => {
        try {
            const response = await mintTokens(recipientAddress, amount, userAddress);
            alert(response.message);
        } catch (error) {
            alert('Error minting tokens');
        }
    };

    return (
        <div>
            <h2>Admin Section</h2>

            <div>
                <h3>Change Address</h3>
                <input
                    type="text"
                    placeholder="Enter new address"
                    value={newAddress}
                    onChange={(e) => setNewAddress(e.target.value)}
                />
                <button onClick={handleChangeAddress}>Change Address</button>
            </div>

            <div>
                <h3>Mint Tokens</h3>
                <input type="text" placeholder="Recipient Address" id="mintAddress" />
                <input type="number" placeholder="Amount" id="mintAmount" />
                <button
                    onClick={() =>
                        handleMintTokens(
                            document.getElementById('mintAddress').value,
                            document.getElementById('mintAmount').value
                        )
                    }
                >
                    Mint Tokens
                </button>
            </div>
        </div>
    );
};

export default Admin;
