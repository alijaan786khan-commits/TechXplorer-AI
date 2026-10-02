import React, { useEffect, useState } from 'react';
import './index.css';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

const API_URL = 'http://127.0.0.1:8000';

function App() {
  const [status, setStatus] = useState('running');
  const [connected, setConnected] = useState(true);
  const [price, setPrice] = useState(63520.45);

  const history = [
    { time: '09:00', price: 62000 },
    { time: '09:15', price: 62300 },
    { time: '09:30', price: 62800 },
    { time: '09:45', price: 63100 },
    { time: '10:00', price: 63520 }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setPrice((prev) => Number((prev + (Math.random() - 0.5) * 100).toFixed(2)));
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  const handleControl = (command) => {
    const nextStatus = command === 'start' ? 'running' : 'stopped';
    setStatus(nextStatus);
    setConnected(command === 'start');
  };

  return (
    <div className="app-shell">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-icon">XT</div>
          <div>
            <p className="eyebrow">AI Trading Terminal</p>
            <h1>Xplorer Trade</h1>
          </div>
        </div>

        <nav className="nav-menu">
          <button className="nav-item active">Overview</button>
          <button className="nav-item">Portfolio</button>
          <button className="nav-item">Signals</button>
          <button className="nav-item">Analytics</button>
        </nav>

        <div className="mini-panel">
          <p className="label">Market</p>
          <h3>BTC/USDT</h3>
          <p className="value">${price.toLocaleString(undefined, { maximumFractionDigits: 2 })}</p>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-panel">
        {/* TOP BAR */}
        <div className="topbar">
          <div>
            <p className="eyebrow">Live Bot Status</p>
            <h2>{status.toUpperCase()}</h2>
          </div>
          <div className="topbar-actions">
            <span className={`connection ${connected ? 'online' : 'offline'}`}>
              {connected ? '● Connected' : '● Offline'}
            </span>
            {status === 'running' ? (
              <button className="danger-btn" onClick={() => handleControl('stop')}>Stop Bot</button>
            ) : (
              <button className="primary-btn" onClick={() => handleControl('start')}>Start Bot</button>
            )}
          </div>
        </div>

        {/* METRICS GRID */}
        <div className="metrics-grid">
          <div className="metric-card cyan">
            <p>Balance</p>
            <h3>$10,000</h3>
          </div>
          <div className="metric-card green">
            <p>PnL</p>
            <h3>+$245.50</h3>
          </div>
          <div className="metric-card purple">
            <p>Win Rate</p>
            <h3>68%</h3>
          </div>
          <div className="metric-card gold">
            <p>Total Trades</p>
            <h3>25</h3>
          </div>
        </div>

        {/* CONTENT GRID */}
        <div className="content-grid">
          {/* CHART CARD */}
          <div className="card chart-card">
            <div className="card-header">
              <div>
                <p className="eyebrow">Price Chart</p>
                <h3>BTC / USDT</h3>
              </div>
              <div className="price-badge">${price.toLocaleString(undefined, { maximumFractionDigits: 2 })}</div>
            </div>
            <div className="chart-box">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={history}>
                  <defs>
                    <linearGradient id="fillPrice" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#59d9ff" stopOpacity={0.8} />
                      <stop offset="95%" stopColor="#59d9ff" stopOpacity={0.1} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="#2c3a5b" strokeDasharray="3 3" />
                  <XAxis dataKey="time" stroke="#89a4d7" style={{ fontSize: '12px' }} />
                  <YAxis stroke="#89a4d7" style={{ fontSize: '12px' }} />
                  <Tooltip />
                  <Area type="monotone" dataKey="price" stroke="#59d9ff" fill="url(#fillPrice)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* POSITION CARD */}
          <div className="card position-card">
            <div className="card-header">
              <div>
                <p className="eyebrow">Position</p>
                <h3>Current Trade</h3>
              </div>
            </div>
            <div className="position-box">
              <div className="row">
                <span>Signal</span>
                <strong className="positive">BUY</strong>
              </div>
              <div className="row">
                <span>Entry Price</span>
                <strong>$62,450.00</strong>
              </div>
              <div className="row">
                <span>Stop Loss</span>
                <strong>$61,950.00</strong>
              </div>
              <div className="row">
                <span>Take Profit</span>
                <strong>$63,450.00</strong>
              </div>
              <div className="row">
                <span>Current P&L</span>
                <strong className="positive">+$125.50</strong>
              </div>
            </div>
          </div>
        </div>

        {/* BOTTOM GRID */}
        <div className="bottom-grid">
          {/* BOT CONFIG */}
          <div className="card">
            <div className="card-header">
              <div>
                <p className="eyebrow">Configuration</p>
                <h3>Bot Config</h3>
              </div>
            </div>
            <div className="settings-box">
              <div className="row">
                <span>Exchange</span>
                <strong>Binance</strong>
              </div>
              <div className="row">
                <span>Timeframe</span>
                <strong>1H</strong>
              </div>
              <div className="row">
                <span>Risk per Trade</span>
                <strong>2%</strong>
              </div>
              <div className="row">
                <span>Strategy</span>
                <strong>EMA + RSI</strong>
              </div>
            </div>
          </div>

          {/* RECENT TRADES */}
          <div className="card">
            <div className="card-header">
              <div>
                <p className="eyebrow">Recent</p>
                <h3>Trades</h3>
              </div>
            </div>
            <div className="trade-list">
              <div className="trade-item">
                <span>BUY</span>
                <span>BTC/USDT</span>
                <span className="positive">+2.1%</span>
              </div>
              <div className="trade-item">
                <span>SELL</span>
                <span>BTC/USDT</span>
                <span className="positive">+1.8%</span>
              </div>
              <div className="trade-item">
                <span>BUY</span>
                <span>BTC/USDT</span>
                <span className="negative">-0.5%</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
