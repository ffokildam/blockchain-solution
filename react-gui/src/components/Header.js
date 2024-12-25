import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
    return (
        <header>
            <h1>DeFi Platform</h1>
            <nav>
                <ul>
                    <li><Link to="/login">Login</Link></li>
                    <li><Link to="/register">Register</Link></li>
                    <li><Link to="/stake-unstake">Stake/Unstake</Link></li>
                    <li><Link to="/balance">Balance</Link></li>
                    <li><Link to="/exchange-tokens">Exchange Tokens</Link></li>
                    <li><Link to="/admin">Admin</Link></li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
