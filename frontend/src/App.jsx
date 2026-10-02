import React, { useEffect, useState } from 'react';
import './index.css';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const API_URL = 'http://127.0.0.1:8000';

function App() {
  const [status, setStatus] = useState('stopped');
  const [connected, setConnected] = useState(false);
  const [config, setConfig] = useState(null);
  const [stats, setStats] = useState({
    total_trades: 0,
    wins: 0,
    losses: 0,
    win_rate: 0,
    total_profit: 0,
    avg_profit: 0
  });
  const [trades, setTrades] = useState([]);
  const [price, setPrice] = useState(62500);
  const [position, setPosition] = useState(null);
  const [history, setHistory] = useState([
    { time: '09:00', price: 62000 },
    { time: '09:10', price: 62500 },
    { time: '09:20', price: 62360 },
    { time: '09:30', price: 62800 },
    { time: '09:40', price: 63200 },
    { time: '09:50', price: 63150 },
    { time: '10:00', price: 63500 }
  ]);

  const loadData = async () => {
    try {
      const response = await fetch(`${API_URL}/chat?prompt=status`);
      const data = await response.json();
      console.log('API response:', data);
    } catch (error) {
      console.log('API connection info:', error.message);
    }
  };

  useEffect(() => {
    loadData();
    const timer = setInterval(loadData, 5000);
    return () => clearInterval(timer);
  }, []);

  const handleControl = async (command) => {
    try {
      const newStatus = command === 'start' ? 'running' : 'stopped';
      setStatus(newStatus);
      console.log(`Bot ${newStatus}`);
    } catch (error) {
      console.error('control failed', error);
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-icon">TX</div>
          <div>
            <p className="eyebrow">Trading System</p>
            <h1>TechXplorer AI</h1>
          </div>
        </div>

        <nav className="nav-menu">
          <button className="nav-item active">Overview</button>
          <button className="nav-item">Portfolio</button>
          <button className="nav-item">Signals</button>
          <button className="nav-item">Analytics</button>
          <button className="nav-item">Settings</button>
        </nav>

        <div className="mini-panel">
          <p className="label">Market</p>
          <h3>BTC/USDT</h3>
          <p className="value">${price.toLocaleString()}</p>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <p className="eyebrow muted">Live Bot Status</p>
            <h2>{status.toUpperCase()}</h2>
          </div>

          <div className="topbar-actions">
            <span className={`connection ${connected ? 'online' : 'offline'}`}>
              {connected ? '🟢 Connected' : '🔴 Offline'}
            </span>
            {status === 'running' ? (
              <button className="danger-btn" onClick={() => handleControl('stop')}>⏹ Stop Bot</button>
            ) : (
              <button className="primary-btn" onClick={() => handleControl('start')}>▶ Start Bot</button>
            )}
          </div>
        </header>

        <section className="metrics-grid">
          <MetricCard title="Balance" value="$10,000" tone="blue" />
          <MetricCard title="PnL" value="$245.50" tone="green" />
          <MetricCard title="Win Rate" value="68%" tone="purple" />
          <MetricCard title="Total Trades" value="25" tone="orange" />
        </section>

        <section className="content-grid">
          <div className="card chart-card">
            <div className="card-header">
              <div>
                <p className="eyebrow muted">Price Chart</p>
                <h3>BTC / USDT</h3>
              </div>
              <div className="price-badge">${price.toLocaleString()}</div>
            </div>

            <div className="chart-box">
              <ResponsiveContainer width="100%" height={260}>
                <AreaChart data={history}>
                  <defs>
                    <linearGradient id="fillPrice" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#5ae4ff" stopOpacity={0.8} />
                      <stop offset="95%" stopColor="#5ae4ff" stopOpacity={0.1} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="#2c3356" strokeDasharray="4 4" />
                  <XAxis dataKey="time" stroke="#7f88b1" />
                  <YAxis stroke="#7f88b1" />
                  <Tooltip />
                  <Area type="monotone" dataKey="price" stroke="#5ae4ff" fill="url(#fillPrice)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card status-card">
            <div className="card-header">
              <div>
                <p className="eyebrow muted">Position</p>
                <h3>Current Trade</h3>
              </div>
            </div>

            <div className="position-box">
              <div className="row"><span>Entry Price</span><strong>$62,450.00</strong></div>
              <div className="row"><span>Stop Loss</span><strong>$61,950.00</strong></div>
              <div className="row"><span>Take Profit</span><strong>$63,450.00</strong></div>
              <div className="row"><span>Current P&L</span><strong style={{color: '#34d399'}}>+$125.50</strong></div>
            </div>
          </div>
        </section>

        <section className="bottom-grid">
          <div className="card">
            <div className="card-header">
              <div>
                <p className="eyebrow muted">Settings</p>
                <h3>Bot Config</h3>
              </div>
            </div>
            <div className="settings-box">
              <div className="row"><span>Exchange</span><strong>Binance</strong></div>
              <div className="row"><span>Timeframe</span><strong>1H</strong></div>
              <div className="row"><span>Risk per Trade</span><strong>2%</strong></div>
              <div className="row"><span>Strategy</span><strong>EMA + RSI + MACD</strong></div>
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <div>
                <p className="eyebrow muted">Recent</p>
                <h3>Trades</h3>
              </div>
            </div>
            <div className="trade-list">
              <div className="trade-item">
                <span>BUY</span>
                <span>BTC/USDT</span>
                <span style={{color: '#34d399'}}>+2.1%</span>
              </div>
              <div className="trade-item">
                <span>SELL</span>
                <span>BTC/USDT</span>
                <span style={{color: '#34d399'}}>+1.8%</span>
              </div>
              <div className="trade-item">
                <span>BUY</span>
                <span>BTC/USDT</span>
                <span style={{color: '#ff6b6b'}}>-0.5%</span>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

function MetricCard({ title, value, tone }) {
  return (
    <div className={`metric-card ${tone}`}>
      <p>{title}</p>
      <h3>{value}</h3>
    </div>
  );
}

export default App;
