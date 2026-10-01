from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import time
from datetime import datetime

app = FastAPI(title='TechXplorer AI', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class ControlCommand(BaseModel):
    command: str

bot_state = {
    'running': False,
    'paused': False,
    'start_time': None,
    'last_update': datetime.now().isoformat(),
    'latest_price': 0.0,
    'position': None,
    'stats': {
        'total_trades': 0,
        'wins': 0,
        'losses': 0,
        'win_rate': 0.0,
        'total_profit': 0.0,
        'avg_profit': 0.0,
    },
    'trades': [],
    'connected_clients': set(),
}

@app.get('/api/health')
async def health():
    return {'status': 'ok', 'timestamp': datetime.now().isoformat()}

@app.get('/api/bot/status')
async def get_status():
    uptime = 0
    if bot_state['start_time']:
        uptime = time.time() - bot_state['start_time']
    return {
        'status': 'running' if bot_state['running'] else 'stopped',
        'paused': bot_state['paused'],
        'uptime_seconds': round(uptime, 2),
        'last_update': bot_state['last_update'],
        'connected_clients': len(bot_state['connected_clients'])
    }

@app.post('/api/bot/control')
async def control(command: ControlCommand):
    cmd = command.command.lower()
    if cmd == 'start':
        bot_state['running'] = True
        bot_state['paused'] = False
        if bot_state['start_time'] is None:
            bot_state['start_time'] = time.time()
        bot_state['last_update'] = datetime.now().isoformat()
        return {'message': 'Bot started', 'status': 'running'}
    if cmd == 'stop':
        bot_state['running'] = False
        bot_state['paused'] = False
        bot_state['last_update'] = datetime.now().isoformat()
        return {'message': 'Bot stopped', 'status': 'stopped'}
    if cmd == 'pause':
        bot_state['paused'] = True
        bot_state['last_update'] = datetime.now().isoformat()
        return {'message': 'Bot paused', 'status': 'paused'}
    if cmd == 'resume':
        bot_state['paused'] = False
        bot_state['running'] = True
        bot_state['last_update'] = datetime.now().isoformat()
        return {'message': 'Bot resumed', 'status': 'running'}
    raise HTTPException(status_code=400, detail='Invalid command')

@app.get('/api/bot/config')
async def get_config():
    return {
        'symbol': 'BTC/USDT',
        'timeframe': '1h',
        'risk_percent': 2.0,
        'start_balance': 100.0,
        'exchange': 'binance',
        'strategy': 'EMA + RSI + MACD'
    }

@app.get('/api/bot/current-price')
async def get_price():
    return {
        'price': bot_state['latest_price'],
        'timestamp': datetime.now().isoformat(),
        'position': bot_state['position']
    }

@app.get('/api/bot/statistics')
async def get_statistics():
    return bot_state['stats']

@app.get('/api/bot/trades')
async def get_trades(limit: int = 20):
    return {'total': len(bot_state['trades']), 'trades': bot_state['trades'][-limit:]}

@app.websocket('/ws/bot')
async def bot_ws(websocket: WebSocket):
    await websocket.accept()
    bot_state['connected_clients'].add(websocket)
    try:
        while True:
            payload = {
                'timestamp': datetime.now().isoformat(),
                'status': 'running' if bot_state['running'] else 'stopped',
                'price': bot_state['latest_price'],
                'position': bot_state['position'],
                'stats': bot_state['stats'],
            }
            await websocket.send_json(payload)
            await asyncio.sleep(1)
    except Exception:
        pass
    finally:
        bot_state['connected_clients'].discard(websocket)


def push_snapshot(latest_price: float = 0.0, position=None, stats=None, trades=None):
    bot_state['latest_price'] = latest_price
    if position is not None:
        bot_state['position'] = position
    if stats is not None:
        bot_state['stats'] = stats
    if trades is not None:
        bot_state['trades'] = trades
    bot_state['last_update'] = datetime.now().isoformat()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
