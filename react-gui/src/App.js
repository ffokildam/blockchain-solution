import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Login from './components/Login';
import Register from './components/Register';
import StakeUnstake from './components/StakeUnstake';
import Balance from './components/Balance';
import ExchangeTokens from './components/ExchangeTokens';
import Admin from './components/Admin';  // Import the Admin component

const App = () => {
    const [userAddress, setUserAddress] = useState(null);

    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/login" element={<Login setUserAddress={setUserAddress} />} />
                <Route path="/register" element={<Register />} />
                <Route path="/stake-unstake" element={<StakeUnstake userAddress={userAddress} />} />
                <Route path="/balance" element={<Balance userAddress={userAddress} />} />
                <Route path="/exchange-tokens" element={<ExchangeTokens userAddress={userAddress} />} />
                <Route path="/admin" element={<Admin userAddress={userAddress} setUserAddress={setUserAddress} />} /> {/* Admin route */}
            </Routes>
        </Router>
    );
};

export default App;
