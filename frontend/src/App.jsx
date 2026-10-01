import React, { useEffect, useState } from 'react';
import './App.css';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const API_URL = 'http://localhost:8000';

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
  const [price, setPrice] = useState(0);
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
      const [statusRes, configRes, statsRes, tradesRes, priceRes] = await Promise.all([
        fetch(`${API_URL}/api/bot/status`),
        fetch(`${API_URL}/api/bot/config`),
        fetch(`${API_URL}/api/bot/statistics`),
        fetch(`${API_URL}/api/bot/trades?limit=5`),
        fetch(`${API_URL}/api/bot/current-price`),
      ]);

      const statusData = await statusRes.json();
      const configData = await configRes.json();
      const statsData = await statsRes.json();
      const tradesData = await tradesRes.json();
      const priceData = await priceRes.json();

      setStatus(statusData.status);
      setConfig(configData);
      setStats(statsData);
      setTrades(tradesData.trades || []);
      setPrice(priceData.price || 0);
      setPosition(priceData.position || null);
    } catch (error) {
      console.log('API not ready yet:', error);
    }
  };

  useEffect(() => {
    loadData();
    const timer = setInterval(loadData, 5000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/bot');
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.price) setPrice(payload.price);
        if (payload.position) setPosition(payload.position);
        if (payload.stats) setStats(payload.stats);
      } catch (error) {
        console.error('WS parse error:', error);
      }
    };
    return () => ws.close();
  }, []);

  const handleControl = async (command) => {
    try {
      const response = await fetch(`${API_URL}/api/bot/control`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
      });
      const data = await response.json();
      if (data.status) {
        setStatus(data.status);
      }
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
            <p className="eyebrow">TRADING SYSTEM</p>
            <h1>TechXplorer AI</h1>
          </div>
        </div>

        <nav className="nav-menu">
          <button className="nav-item active">Overview</button>
          <button className="nav-item">Portfolio</button>
          <button className="nav-item">Signals</button>
          <button className="nav-item">Strategies</button>
          <button className="nav-item">Analytics</button>
        </nav>

        <div className="mini-panel">
          <p className="label">Market</p>
          <h3>{config?.symbol || 'BTC/USDT'}</h3>
          <p className="value">${Number(price || 0).toLocaleString()}</p>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <p className="eyebrow muted">LIVE BOT STATUS</p>
            <h2>{status.toUpperCase()}</h2>
          </div>

          <div className="topbar-actions">
            <span className={`connection ${connected ? 'online' : 'offline'}`}>
              {connected ? 'Live feed online' : 'Offline'}
            </span>
            {status === 'running' ? (
              <button className="danger-btn" onClick={() => handleControl('stop')}>Stop Bot</button>
            ) : (
              <button className="primary-btn" onClick={() => handleControl('start')}>Start Bot</button>
            )}
          </div>
        </header>

        <section className="metrics-grid">
          <MetricCard title="Balance" value="$10,000" tone="blue" />
          <MetricCard title="PnL" value={`$${stats.total_profit.toFixed(2)}`} tone="green" />
          <MetricCard title="Win Rate" value={`${stats.win_rate.toFixed(1)}%`} tone="purple" />
          <MetricCard title="Total Trades" value={String(stats.total_trades)} tone="orange" />
        </section>

        <section className="content-grid">
          <div className="card chart-card">
            <div className="card-header">
              <div>
                <p className="eyebrow muted">PRICE</p>
                <h3>BTC / USDT</h3>
              </div>
              <div className="price-badge">${Number(price || 0).toLocaleString()}</div>
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
                <p className="eyebrow muted">POSITION</p>
                <h3>Current Trade</h3>
              </div>
            </div>

            {position ? (
              <div className="position-box">
                <div className="row"><span>Entry</span><strong>${position.entry_price?.toFixed(2) || '0.00'}</strong></div>
                <div className="row"><span>Stop</span><strong>${position.stop_loss?.toFixed(2) || '0.00'}</strong></div>
                <div className="row"><span>Target</span><strong>${position.take_profit?.toFixed(2) || '0.00'}</strong></div>
                <div className="row"><span>Trend</span><strong>{position.trend || 'Neutral'}</strong></div>
              </div>
            ) : (
              <div className="empty-state">No active position yet.</div>
            )}
          </div>
        </section>

        <section className="bottom-grid">
          <div className="card">
            <div className="card-header">
              <div>
                <p className="eyebrow muted">SETTINGS</p>
                <h3>Bot Config</h3>
              </div>
            </div>
            <div className="settings-box">
              <div className="row"><span>Exchange</span><strong>{config?.exchange || 'binance'}</strong></div>
              <div className="row"><span>Timeframe</span><strong>{config?.timeframe || '1h'}</strong></div>
              <div className="row"><span>Risk</span><strong>{config?.risk_percent || '2'}%</strong></div>
              <div className="row"><span>Strategy</span><strong>{config?.strategy || 'EMA + RSI + MACD'}</strong></div>
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <div>
                <p className="eyebrow muted">RECENT</p>
                <h3>Trades</h3>
              </div>
            </div>
            <div className="trade-list">
              {trades.length ? (
                trades.map((trade, idx) => (
                  <div key={idx} className="trade-item">
                    <span>{trade.side || 'BUY'}</span>
                    <span>{trade.symbol || 'BTC/USDT'}</span>
                    <span>${Number(trade.price || 0).toFixed(2)}</span>
                  </div>
                ))
              ) : (
                <div className="empty-state small">No trades yet.</div>
              )}
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
