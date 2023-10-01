from ccxtools.base.Exchange import Exchange


class CcxtExchange(Exchange):

    def __init__(self):
        self.ccxt_inst = None

    def get_balance(self, ticker):
        """
        :param ticker: <String> Ticker name. ex) 'USDT', 'BTC'
        :return: <Int> Balance amount
        """
        return self.ccxt_inst.fetch_balance()[ticker]['total']

    def get_balances(self, tickers):
        """
        :param tickers: <List> Ticker names. ex) ['USDT', 'BTC']
        :return: <Dict> { ticker: balance }
        """
        all_balances = self.ccxt_inst.fetch_balance()['total']
        return {
            ticker: all_balances[ticker] for ticker in tickers
        }
