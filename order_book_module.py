import requests
from datetime import datetime


class OrderBook:

    def __init__(self, limit=1000, symbol='BTCUSDT'):
        self.url = f'https://fapi.binance.com/fapi/v1/depth?symbol={symbol}&limit{limit}'

    def get_current_volume(self):
        order_book = requests.get(self.url).json()

        vol_bids = 0.0
        vol_asks = 0.0

        for bid in order_book['bids']:
            vol_bids += float(bid[1])
        for ask in order_book['asks']:
            vol_asks += float(ask[1])

        trn_time = datetime.fromtimestamp(order_book['T'] // 1000)

        return {'date_time': trn_time, 'bids': vol_bids, 'asks': vol_asks}
