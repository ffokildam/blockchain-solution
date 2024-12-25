import axios from 'axios';

const API_URL = "http://localhost:8000";  // Replace with your backend URL

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Function to register a user
export const registerUser = async (username, password) => {
    const requestBody = { username, password };
    console.log('Request to /register:', requestBody);  // Log the request body
    const response = await api.post('/register', requestBody);
    console.log('Response from /register:', response.data);  // Log the response
    return response.data;
};

// Function to log in a user
export const loginUser = async (username, password) => {
    const requestBody = { username, password };
    console.log('Request to /login:', requestBody);  // Log the request body
    const response = await api.post('/login', requestBody);
    console.log('Response from /login:', response.data);  // Log the response
    return response.data;
};

// Function to get the balance of an address
export const getBalance = async (address) => {
    const requestBody = { address };
    console.log('Request to /balance:', requestBody);  // Log the request body
    const response = await api.get(`/balance/${address}`);
    console.log('Response from /balance:', response.data);  // Log the response
    return response.data;
};

// Function to stake tokens
export const stake = async (amount, durationDays, addressFrom) => {
    const requestBody = { amount, duration_days: durationDays, address_from: addressFrom };
    console.log('Request to /stake:', requestBody);  // Log the request body
    const response = await api.post('/stake', requestBody);
    console.log('Response from /stake:', response.data);  // Log the response
    return response.data;
};

// Function to unstake tokens
export const unstake = async (positionId, addressFrom) => {
    const requestBody = { position_id: positionId, address_from: addressFrom };
    console.log('Request to /unstake:', requestBody);  // Log the request body
    const response = await api.post('/unstake', requestBody);
    console.log('Response from /unstake:', response.data);  // Log the response
    return response.data;
};

// Function to mint tokens (admin function)
export const mintTokens = async (recipientAddress, amount, addressFrom) => {
    const requestBody = { recipient_address: recipientAddress, amount, address_from: addressFrom };
    console.log('Request to /mint_tokens:', requestBody);  // Log the request body
    const response = await api.post('/mint_tokens', requestBody);
    console.log('Response from /mint_tokens:', response.data);  // Log the response
    return response.data;
};

// Function to exchange tokens
export const exchangeTokens = async (to, amount, addressFrom) => {
    const requestBody = { to, amount, address_from: addressFrom };
    console.log('Request to /exchange_tokens:', requestBody);  // Log the request body
    const response = await api.post('/exchange_tokens', requestBody);
    console.log('Response from /exchange_tokens:', response.data);  // Log the response
    return response.data;
};

// Function to get staking positions for a given address
export const getStakingPositions = async (address) => {
    const requestBody = { address };
    console.log('Request to /get_staking_positions:', requestBody);  // Log the request body
    const response = await api.get(`/get_staking_positions/${address}`);
    console.log('Response from /get_staking_positions:', response.data);  // Log the response
    return response.data;
};
