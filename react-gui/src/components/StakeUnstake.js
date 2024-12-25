import React, { useState, useEffect } from 'react';
import { stake, unstake, getStakingPositions } from '../api';

const StakeUnstake = ({ userAddress }) => {
    const [amount, setAmount] = useState('');
    const [duration, setDuration] = useState('');
    const [positionId, setPositionId] = useState('');
    const [stakingPositions, setStakingPositions] = useState([]); // Store staking positions

    // Fetch staking positions when the component mounts or userAddress changes
    useEffect(() => {
        const fetchStakingPositions = async () => {
            try {
                const response = await getStakingPositions(userAddress);
                console.log('Fetched Staking Positions:', response); // Log the full response

                // Access staking_positions from the response object
                const positions = response.staking_positions || [];
                if (Array.isArray(positions)) {
                    setStakingPositions(positions); // Update state with the positions array
                } else {
                    console.error('Expected an array of staking positions but got:', positions);
                }
            } catch (error) {
                console.error('Error fetching staking positions:', error);
            }
        };

        if (userAddress) {
            fetchStakingPositions();
        }
    }, [userAddress]);

    // Handle staking
    const handleStake = async () => {
        try {
            await stake(amount, duration, userAddress);
            alert('Staked successfully');
            // Fetch staking positions after staking
            try {
                const response = await getStakingPositions(userAddress);
                console.log('Fetched Staking Positions after staking:', response);
                const positions = response.staking_positions || [];
                if (Array.isArray(positions)) {
                    setStakingPositions(positions);
                } else {
                    console.error('Expected an array of staking positions but got:', positions);
                }
            } catch (error) {
                console.error('Error fetching staking positions after staking:', error);
            }
        } catch (error) {
            alert('Error staking tokens');
            console.error(error);
        }
    };

    // Handle unstaking
    const handleUnstake = async () => {
        try {
            await unstake(positionId, userAddress);
            alert('Unstaked successfully');
            // Fetch staking positions after unstaking
            try {
                const response = await getStakingPositions(userAddress);
                console.log('Fetched Staking Positions after unstaking:', response);
                const positions = response.staking_positions || [];
                if (Array.isArray(positions)) {
                    setStakingPositions(positions);
                } else {
                    console.error('Expected an array of staking positions but got:', positions);
                }
            } catch (error) {
                console.error('Error fetching staking positions after unstaking:', error);
            }
        } catch (error) {
            alert('Error unstaking tokens');
            console.error(error);
        }
    };

    return (
        <div>
            <h2>Stake/Unstake</h2>

            {/* Staking Form */}
            <div>
                <input
                    type="number"
                    placeholder="Amount"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                />
                <input
                    type="number"
                    placeholder="Duration (days)"
                    value={duration}
                    onChange={(e) => setDuration(e.target.value)}
                />
                <button onClick={handleStake}>Stake</button>
            </div>

            {/* Unstaking Form */}
            <div>
                <input
                    type="number"
                    placeholder="Position ID"
                    value={positionId}
                    onChange={(e) => setPositionId(e.target.value)}
                />
                <button onClick={handleUnstake}>Unstake</button>
            </div>

            {/* Display staking positions */}
            <div>
                <h3>Current Staking Positions</h3>
                {stakingPositions.length > 0 ? (
                    <ul>
                        {stakingPositions.map((position) => (
                            <li key={position.positionId}>
                                Position ID: {position.positionId} - Amount: {position.amount} - Duration: {position.durationDays} days
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No staking positions available</p>
                )}
            </div>
        </div>
    );
};

export default StakeUnstake;
