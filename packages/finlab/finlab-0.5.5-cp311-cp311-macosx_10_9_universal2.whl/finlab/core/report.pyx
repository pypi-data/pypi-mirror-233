from collections.abc import Iterable
from pkgutil import iter_modules
import pandas as pd
import numpy as np
import importlib
import datetime
import base64
import math
import json
import gzip
import re
import os
import finlab
from finlab import ffn_core
from finlab import get_token
from finlab.utils import logger, requests
from finlab import market_info


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        return super(CustomEncoder, self).default(obj)


def is_in_vscode():
    for k in os.environ.keys():
        if 'VSCODE' in k:
            return True
    return False

daily_return = lambda s: s.resample('1d').last().dropna().pct_change()

def safe_division(n, d):
    return n / d if d else 0

calc_cagr = (
    lambda s: (s.add(1).prod()) ** safe_division(365.25, (s.index[-1] - s.index[0]).days) - 1 
    if len(s) > 1 else 0)


class Report(object):

    def __init__(self, creturn, position, fee_ratio, tax_ratio, trade_at, next_trading_date, market_info):
        # cumulative return
        self.creturn = creturn
        self.daily_creturn = self.creturn.resample('1d').last().dropna().ffill().rebase()

        # benchmark return
        self.benchmark = market_info.get_benchmark()
        if isinstance(self.benchmark, pd.Series) and self.benchmark.index.tz is not None:
            self.benchmark.index = pd.Series(self.benchmark.index).dt.tz_convert(position.index.tz)
        if len(self.benchmark) == 0:
            self.benchmark = pd.Series(1, index=self.creturn.index)

        self.daily_benchmark = self.benchmark\
            .dropna().reindex(self.daily_creturn.index, method='ffill') \
            .ffill().rebase()
        
        # position 
        self.position = position
        self.fee_ratio = fee_ratio
        self.tax_ratio = tax_ratio
        self.trade_at = trade_at
        self.update_date = position.index[-1]
        self.asset_type = 'tw_stock' if (
                position.columns.str.find('USDT') == -1).all() else 'crypto'

        position_changed = position.diff().abs().sum(axis=1)
        self.last_trading_date = position_changed[position_changed != 0].index[-1] \
            if (position_changed != 0).sum() != 0 else position.index[0]
        self.next_trading_date = next_trading_date
        self.market_info = market_info


    def display(self, return_fig=False):

        if self.benchmark is not None:
            performance = pd.DataFrame({
                'strategy': self.creturn,
                'benchmark': self.benchmark.dropna()}).dropna().rebase()
        else:
            performance = pd.DataFrame({
                'strategy': self.creturn}).dropna().rebase()

        fig = self.create_performance_figure(
            performance, (self.position != 0).sum(axis=1))

        stats = self.get_stats()
        imp_stats = pd.Series({
         'annualized_rate_of_return':str(round(stats['daily_mean']*100,2))+'%',
         'sharpe':round(stats['daily_sharpe'],2),
         'max_drawdown':str(round(stats['max_drawdown']*100,2))+'%',
         'win_ratio':str(round(stats['win_ratio']*100,2))+'%',
        }).to_frame().T
        imp_stats.index = ['']

        yearly_return_fig = self.create_yearly_return_figure(stats['return_table'])
        monthly_return_fig = self.create_monthly_return_figure(stats['return_table'])

        if return_fig:
            return fig
        else:
            from IPython.display import display

            display(imp_stats)
            display(fig)
            display(yearly_return_fig)
            display(monthly_return_fig)

            if hasattr(self, 'current_trades'):
                display(self.current_trades)
            else:
                print('current position')
                p = self.position.iloc[-1]
                display(p[p != 0])

    @staticmethod
    def create_performance_figure(performance_detail, nstocks):

        from plotly.subplots import make_subplots
        import plotly.graph_objs as go
        # plot performance

        def diff(s, period):
            return (s / s.shift(period) - 1)

        drawdowns = performance_detail.to_drawdown_series()

        fig = go.Figure(make_subplots(
            rows=4, cols=1, shared_xaxes=True, row_heights=[2, 1, 1, 1]))
        fig.add_scatter(x=performance_detail.index, y=performance_detail.strategy / 100 - 1,
                        name='strategy', row=1, col=1, legendgroup='performance', fill='tozeroy')
        fig.add_scatter(x=drawdowns.index, y=drawdowns.strategy, name='strategy - drawdown',
                        row=2, col=1, legendgroup='drawdown', fill='tozeroy')
        fig.add_scatter(x=performance_detail.index, y=diff(performance_detail.strategy, 20),
                        fill='tozeroy', name='strategy - month rolling return',
                        row=3, col=1, legendgroup='rolling performance', )

        if 'benchmark' in performance_detail.columns:
            fig.add_scatter(x=performance_detail.index, y=performance_detail.benchmark / 100 - 1,
                            name='benchmark', row=1, col=1, legendgroup='performance', line={'color': 'gray'})
            fig.add_scatter(x=drawdowns.index, y=drawdowns.benchmark, name='benchmark - drawdown',
                            row=2, col=1, legendgroup='drawdown', line={'color': 'gray'})
            fig.add_scatter(x=performance_detail.index, y=diff(performance_detail.benchmark, 20),
                            fill='tozeroy', name='benchmark - month rolling return',
                            row=3, col=1, legendgroup='rolling performance', line={'color': 'rgba(0,0,0,0.2)'})

        fig.add_scatter(x=nstocks.index, y=nstocks, row=4,
                        col=1, name='nstocks', fill='tozeroy')
        fig.update_layout(legend={'bgcolor': 'rgba(0,0,0,0)'},
                          margin=dict(l=60, r=20, t=40, b=20),
                          height=600,
                          width=800,
                          xaxis4=dict(
                              rangeselector=dict(
                                  buttons=list([
                                      dict(count=1,
                                           label="1m",
                                           step="month",
                                           stepmode="backward"),
                                      dict(count=6,
                                           label="6m",
                                           step="month",
                                           stepmode="backward"),
                                      dict(count=1,
                                           label="YTD",
                                           step="year",
                                           stepmode="todate"),
                                      dict(count=1,
                                           label="1y",
                                           step="year",
                                           stepmode="backward"),
                                      dict(step="all")
                                  ]),
                                  x=0,
                                  y=1,
                              ),
                              rangeslider={'visible': True, 'thickness': 0.1},
                              type="date",
                          ),
                          yaxis={'tickformat': ',.0%', },
                          yaxis2={'tickformat': ',.0%', },
                          yaxis3={'tickformat': ',.0%', },
                          )
        return fig


    @staticmethod
    def create_yearly_return_figure(return_table):
        import plotly.express as px
        yearly_return = [round(v['YTD']*1000)/10 for v in return_table.values()]
        fig = px.imshow([yearly_return],
                        labels=dict(color="return(%)"),
                        x=list([str(k) for k in return_table.keys()]),
                        text_auto=True,
                        color_continuous_scale='RdBu_r',
                        )

        fig.update_traces(
            hovertemplate="<br>".join([
                "year: %{x}",
                "return: %{z}%",
            ])
        )

        fig.update_layout(
            height = 120,
            width= 800,
            margin=dict(l=20, r=270, t=40, b=40),
            yaxis={
                'visible': False,
            },
            title={
                'text': 'yearly return',
                'x': 0.025,
                'yanchor': 'top',
            },
            coloraxis_showscale=False,
            coloraxis={'cmid':0}
            )

        return fig

    @staticmethod
    def create_monthly_return_figure(return_table):
        import plotly.express as px
        monthly_table = pd.DataFrame(return_table).T
        monthly_table = round(monthly_table*100,1).drop(columns='YTD')

        fig = px.imshow(monthly_table.values,
                        labels=dict(x="month", y='year', color="return(%)"),
                        x=monthly_table.columns.astype(str),
                        y=monthly_table.index.astype(str),
                        text_auto=True,
                        color_continuous_scale='RdBu_r',

                        )

        fig.update_traces(
            hovertemplate="<br>".join([
                "year: %{y}",
                "month: %{x}",
                "return: %{z}%",
            ])
        )

        fig.update_layout(
            height = 550,
            width= 800,
            margin=dict(l=20, r=270, t=40, b=40),
            title={
                'text': 'monthly return',
                'x': 0.025,
                'yanchor': 'top',
            },
            yaxis={
                'side': "right",
            },
            coloraxis_showscale=False,
            coloraxis={'cmid':0}
        )

        return fig

    def to_json(self):

        # Convert DataFrame to JSON
        json_str = self.trades.to_json(orient='records')

        # Encode JSON string into bytes
        json_bytes = json_str.encode('utf-8')

        # Compress JSON bytes with gzip
        gzip_bytes = gzip.compress(json_bytes)

        # Convert gzip bytes to base64 encoded string for easier storage and transmission
        gzip_b64_str = base64.b64encode(gzip_bytes).decode('utf-8')

        ret = {
            'timestamps': self.daily_creturn.index.astype(str).to_list(),
            'strategy': self.daily_creturn.values.tolist(),
            'benchmark': self.daily_benchmark.values.tolist(),
            'metrics': self.get_metrics(),
            'trades': gzip_b64_str
        }

        return ret

    def _to_json046(self):

        # Convert DataFrame to JSON
        json_str = self.trades.tail(500).to_json(orient='records')

        # Encode JSON string into bytes
        json_bytes = json_str.encode('utf-8')

        # Compress JSON bytes with gzip
        gzip_bytes = gzip.compress(json_bytes)

        # Convert gzip bytes to base64 encoded string for easier storage and transmission
        gzip_b64_str = base64.b64encode(gzip_bytes).decode('utf-8')

        ret = {
            'metrics': self.get_metrics(),
            'trades': gzip_b64_str
        }

        return ret


    def upload(self, name=None, mae_mfe_charts=False, display=True):

        name = os.environ.get(
            'FINLAB_FORCED_STRATEGY_NAME', None) or name or '未命名'

        head_is_eng = len(re.findall(
            r'[\u0041-\u005a|\u0061-\u007a]', name[0])) > 0
        has_cn = len(re.findall('[\u4e00-\u9fa5]', name[1:])) > 0
        if head_is_eng and has_cn:
            raise Exception('Strategy Name Error: 名稱如包含中文，需以中文當開頭。')
        for c in '()[]+-|!@#$~%^={}&*':
            name = name.replace(c, '_')

        # stats
        stats = self.get_stats()

        # creturn
        creturn = {'time': self.daily_creturn.index.astype(str).to_list(),
                   'value': self.daily_creturn.values.tolist()}

        # ndays return
        ndays_return = {d: self.get_ndays_return(
            self.daily_creturn, d) for d in [1, 5, 10, 20, 60]}
        ndays_return_benchmark = {d: self.get_ndays_return(
            self.daily_benchmark, d) for d in [1, 5, 10, 20, 60]}

        d = {
            # backtest info
            'drawdown_details': stats['drawdown_details'],
            'stats': stats,
            'returns': creturn,
            'benchmark': self.daily_benchmark.values.tolist(),
            'ndays_return': ndays_return,
            'ndays_return_benchmark': ndays_return_benchmark,
            'return_table': stats['return_table'],
            'fee_ratio': self.fee_ratio,
            'tax_ratio': self.tax_ratio,
            'trade_at': self.trade_at if isinstance(self.trade_at, str) else 'open',
            'timestamp_name': self.market_info.get_name(),
            'freq': self.market_info.get_freq(),

            # dates
            'update_date': self.update_date.isoformat(),
            'next_trading_date': self.next_trading_date.isoformat(),

            # key data
            'position': self.position_info(),
            'position2': self.position_info2(),

            # live performance
            'live_performance_start': self.live_performance_start.isoformat() if self.live_performance_start else None,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            **self._to_json046()
        }

        # import numpy as np

        # def find_ndarray_keys(d, parent_keys=[]):
        #     ndarray_keys = []
        #     for key, value in d.items():
        #         new_keys = parent_keys + [key]
        #         if isinstance(value, np.ndarray):
        #             ndarray_keys.append('.'.join(new_keys))
        #         elif isinstance(value, dict):
        #             ndarray_keys.extend(find_ndarray_keys(value, new_keys))
        #     return ndarray_keys

        
        # ndarray_keys = find_ndarray_keys(d)
        # print('ndarray_keys')
        # print(ndarray_keys)

        payload = {'data': json.dumps(d, cls=CustomEncoder),
                   'api_token': get_token(),
                   'collection': 'strategies',
                   'document_id': name}

        result = requests.post(
            'https://asia-east2-fdata-299302.cloudfunctions.net/write_database', data=payload).text

        # python is in website backtest
        if 'FINLAB_FORCED_STRATEGY_NAME' in os.environ:
            return {'status': 'success'}

        # create iframe
        try:
            result = json.loads(result)
        except:
            return {'status': 'error', 'message': 'cannot parse json object'}

        if 'status' in result and result['status'] == 'error':
            print('Fail to upload result to server')
            print('error message', result['message'])
            return {'status': 'error', 'message': result['status']}

        if not display:
            return {'status': 'success'}

        try:
            if is_in_vscode():
                self.display()
            else:
                from IPython.display import IFrame, display
                url = 'https://ai.finlab.tw/strategy/?uid=' + \
                      result['uid'] + '&sid=' + result['strategy_id']

                iframe = IFrame(url, width='100%', height=600)
                display(iframe)

        except Exception as e:
            print(e)
            print('Install ipython to show the complete backtest results.')

        return {'status': 'success'}

        if 'status' in result and result['status'] == 'error':
            print('Fail to upload result to server')
            print('error message', result['message'])
            return {'status': 'error', 'message': res}

        try:
            from IPython.display import IFrame, display
            url = 'https://ai.finlab.tw/strategy/?uid=' + \
                  result['uid'] + '&sid=' + result['strategy_id']

            iframe = IFrame(url, width='100%', height=600)
            display(iframe)

        except Exception as e:
            print(e)
            print('Install ipython to show the complete backtest results.')

        return {'status': 'success'}

    
    def position_info2(self):
        actions = []

        for idx, row in self.current_trades.iterrows():
            is_entry = row['entry_sig_date'] == self.creturn.index[-1]
            is_future_entry = row['entry_sig_date'] > self.creturn.index[-1]

            # exit today or before today
            is_exit = row['exit_sig_date'] == self.creturn.index[-1]
            is_past_exit = row['exit_sig_date'] < self.creturn.index[-1]

            # exit in futures (hold)
            is_hold = (row['exit_sig_date'] > self.creturn.index[-1]) | (row['exit_sig_date'] != row['exit_sig_date'])

            type_ = 'hold'

            if is_entry:
                type_ = 'entry'
            elif is_future_entry:
                type_ = 'entry_f'
            elif is_exit:
                type_ = 'exit'
            elif is_past_exit:
                type_ = 'exit_p'
            elif is_hold:
                type_ = 'hold'
            else:
                print(f'There is a strange type for stock {idx} {row}')
            
            if type_ == 'exit' or type_ == 'exit_p':
                reason = self.actions.loc[idx] if idx in self.actions.index else '_'
            else:
                reason = '_'

            date = row['exit_sig_date']
            if date != date:
                date = row['entry_sig_date']
            profit = row['return']
            if profit != profit:
                profit = 0
            actions.append({
                'type': type_,
                'reason': reason,
                'date': date.isoformat(),
                'profit': profit
            })

        adj_close = self.market_info.get_price('close', adj=True)
        close = self.market_info.get_price('close', adj=False)
        cmin = adj_close.iloc[-20:].min()
        cmax = adj_close.iloc[-20:].max()
        rsv20 = (adj_close.iloc[-1] - cmin) / (cmax - cmin)

        to_date_string = lambda d: d.isoformat() if d == d else None

        trades = self.current_trades.copy()
        positions = pd.DataFrame({
            'assetName': trades.index.str.split(' ').str[1],
            'assetId':trades.index.str.split(' ').str[0],
            'entryDate':trades['entry_date'].apply(to_date_string),
            'entrySigDate':trades['entry_sig_date'].apply(to_date_string),
            'exitDate':trades['exit_date'].apply(to_date_string),
            'exitSigDate':trades['exit_sig_date'].apply(to_date_string),
            'entryPrice':trades['trade_price@entry_date'],
            'exitPrice':trades['trade_price@exit_date'],
            'currentPrice':trades.index.str.split(' ').str[0].map(close.iloc[-1]),
            'profit':trades['return'],
            'currentWeight':trades['weight'],
            'nextWeight':trades['next_weights'],
            'rsv20': trades.index.str.split(' ').str[0].map(rsv20),
            'action': actions,
        }).to_dict(orient='records')

        position_config = {
            # isDailyStrategy: False,
            "isDailyStrategy": 1 if ((self.position.index.hour == 0) & (self.position.index.minute == 0) & (self.position.index.second == 0)).all() else 0,
            "sl": self.stop_loss,
            "tp": self.take_profit,
            "resample": self.resample,
            "entryTradePrice": self.trade_at,
            "exitTradePrice": self.trade_at,
            "scheduled": self.next_trading_date.isoformat(),
            "dataFreq": self.market_info.get_freq(),
            "created": datetime.datetime.now().isoformat(),
            "lastTimestamp": self.creturn.index[-1].isoformat() if len(self.creturn) > 0 else None,
        }

        return {
            "positions": positions,
            "positionConfig": position_config,
        }

    def position_info(self):

        current_trades = self.current_trades

        default_status = pd.Series('hold', index=current_trades.index)
        default_status.loc[current_trades.exit_sig_date.notna()] = 'exit'
        if self.resample == None:
            default_status[current_trades.exit_sig_date.isnull()] = 'hold'
            default_status[current_trades.exit_sig_date.notna()] = 'exit'

        trade_at = self.trade_at if isinstance(self.trade_at, str) else 'close'

        trade_at_zh = {
                'close': '收盤',
                'open': '開盤',
                'open|close': '盤中',
                }

        status = self.actions.reindex(current_trades.index).fillna(default_status)

        ret = pd.DataFrame({
            'status': status,
            'weight': current_trades.weight,
            'next_weight': current_trades.next_weights,
            'entry_date': current_trades.entry_sig_date.apply(lambda d: d.isoformat() if d else ''),
            'exit_date': current_trades.exit_sig_date.apply(lambda d: d.isoformat() if d else ''),
            'return': current_trades['return'].fillna(0),
            'entry_price': current_trades['trade_price@entry_date'].fillna(0),
        }, index=current_trades.index)

        ret['latest_sig_date'] = pd.DataFrame({'entry': ret.entry_date, 'exit': ret.exit_date}).max(axis=1)
        ret = ret.sort_values('latest_sig_date').groupby(level=0).last()
        ret = ret.drop(columns='latest_sig_date')

        ret = ret.to_dict('index')

        ret['update_date'] = self.update_date.isoformat()
        ret['next_trading_date'] = self.next_trading_date.isoformat()
        ret['trade_at'] = trade_at
        ret['freq'] = self.market_info.get_freq()
        ret['market'] = self.market_info.get_name()
        ret['stop_loss'] = self.stop_loss
        ret['take_profit'] = self.take_profit

        return ret

    @staticmethod
    def get_ndays_return(creturn, n):
        last_date_eq = creturn.iloc[-1]
        ref_date_eq = creturn.iloc[max(-1 - n, -len(creturn))]
        return last_date_eq / ref_date_eq - 1

    def add_trade_info(self, name, df, date_col='entry_sig_date'):

        if isinstance(date_col, str):
            date_col = [date_col]

        combined_dates = set().union(*[set(self.trades[d]) for d in date_col])
        df_temp = df.reindex(df.index.union(combined_dates), method='ffill')

        for date_name in date_col:
            dates = self.trades[date_name]
            stocks = self.trades['stock_id'].str.split(' ').str[0]

            idx_d = df_temp.index.get_indexer_for(dates)
            idx_s = df_temp.columns.get_indexer_for(stocks)

            self.trades[f"{name}@{date_name}"] = [
                np.nan if s == -1 else df_temp.iloc[d, s]
                for s, d in zip(idx_s, idx_d)]


    def remove_trade_info(self, name):
        cs = [c for c in self.columns if c != name]
        self.trades = self.trades[cs]

    def get_mae_mfe(self):
        return self.mae_mfe

    def get_trades(self):
        return self.trades

    def get_stats(self, resample='1d', riskfree_rate=0.02):

        stats = self.creturn.resample(resample).last().dropna().calc_stats()
        stats.set_riskfree_rate(riskfree_rate)

        # calculate win ratio
        ret = stats.stats.to_dict()
        ret['start'] = ret['start'].strftime('%Y-%m-%d')
        ret['end'] = ret['end'].strftime('%Y-%m-%d')
        ret['version'] = finlab.__version__

        trades = self.trades.dropna()
        ret['win_ratio'] = sum(trades['return'] > 0) / len(trades) if len(trades) != 0 else 0
        ret['return_table'] = stats.return_table.transpose().to_dict()
        # ret['mae_mfe'] = self.run_analysis("MaeMfe", display=False)
        # ret['liquidity'] = self.run_analysis("Liquidity", display=False)
        # ret['period_stats'] = self.run_analysis("PeriodStats", display=False)
        # ret['alpha_beta'] = self.run_analysis("AlphaBeta", display=False)

        # todo old remove
        drawdown = self.run_analysis("Drawdown", display=False)
        ret['drawdown_details'] = drawdown['strategy']['largest_drawdown']
        return ret

    def get_metrics(self, stats_=None, riskfree_rate=0.02):

        if stats_ == None:
            simple_stats = self.creturn.resample('1d').last().dropna().calc_stats()
            simple_stats.set_riskfree_rate(0.02)
            stats_ = simple_stats.stats.to_dict()


        mv = self.market_info.get_market_value()
        if len(mv) != 0:
            self.add_trade_info('market_value', mv, ['entry_date'])

        strategy_daily_return = daily_return(self.creturn)
        benchmark_daily_return = daily_return(self.benchmark).reindex(strategy_daily_return.index).fillna(0)

        from finlab.analysis.alphaBetaAnalysis import AlphaBetaAnalysis
        alpha, beta = AlphaBetaAnalysis.calculate_alpha_beta(strategy_daily_return, benchmark_daily_return)
        position_nstocks = (self.position!=0).sum(axis=1)
        monthly_return = (strategy_daily_return+1).resample('M').prod().subtract(1)
        var = monthly_return.quantile(0.05)
        cvar = monthly_return[monthly_return < var].mean()
        
        tail_right = strategy_daily_return.quantile(0.95)
        tail_left = strategy_daily_return.quantile(0.05)
        tail_ratio = abs(tail_right / tail_left) if tail_left != 0 else 1

        safe_div = lambda a, b: a / b if b != 0 else 0
        calc_profit_factor = lambda s: abs(safe_div(s[s > 0].sum(), s[s < 0].sum()))
        liquidity = self.run_analysis('liquidity', display=False)


        def calc_capacity(trades, percentage_of_volume=0.05):

            if 'turnover@entry_date' not in trades.columns:
                return 0

            accepted_money_flow = (self.trades['turnover@entry_date'] * percentage_of_volume / self.trades.position + \
                    self.trades['turnover@exit_date'] * percentage_of_volume / self.trades.position) / 2

            return accepted_money_flow.quantile(0.1)


        return {

            "backtest": {
                "startDate": self.creturn.index[0].to_pydatetime().timestamp(),
                "endDate": self.creturn.index[-1].to_pydatetime().timestamp(),
                "version": finlab.__version__,
                'feeRatio': self.fee_ratio,
                'taxRatio': self.tax_ratio,
                'tradeAt': self.trade_at if isinstance(self.trade_at, str) else 'open',
                'market': self.market_info.get_name(),
                'freq': self.market_info.get_freq(),

                # dates
                'updateDate': self.update_date.timestamp(),
                'nextTradingDate': self.next_trading_date.timestamp(),

                # live performance
                'livePerformanceStart': self.live_performance_start.timestamp() if self.live_performance_start else None,
                'stopLoss': self.stop_loss,
                'takeProfit': self.take_profit,
                'trailStop': self.trail_stop,
            },

            "profitability": {
                "annualReturn": stats_["cagr"],
                "alpha": alpha,
                "beta": beta,
                "avgNStock": position_nstocks.mean(),
                "maxNStock": position_nstocks.mean().max(),
            },

            "risk": {
                "maxDrawdown": stats_["max_drawdown"],
                "avgDrawdown": stats_["avg_drawdown"],
                "avgDrawdownDays": stats_["avg_drawdown_days"],
                "valueAtRisk": var,
                "cvalueAtRisk": cvar
            },

            "ratio": {
                "sharpeRatio": stats_["daily_sharpe"],
                "sortinoRatio": stats_["daily_sortino"],
                "calmarRatio": stats_["calmar"],
                "volatility": stats_["daily_vol"],
                "profitFactor": calc_profit_factor(self.trades['return']),
                "tailRatio": tail_ratio,
            },

            "winrate": {
                "winRate": sum(self.trades['return'] > 0) / len(self.trades) if len(self.trades) != 0 else 0,
                "m12WinRate": stats_["twelve_month_win_perc"],
                "expectancy": self.trades['return'].mean(),
                "mae": self.trades['mae'].mean(),
                "mfe": self.trades['gmfe'].mean(),
            },

            "liquidity": {
                "capacity": calc_capacity(self.trades, percentage_of_volume=0.05),
                "disposalStockRatio": max(liquidity['處置股']['exit'], liquidity['處置股']['entry']) if '處置股' in liquidity else 0,
                "warningStockRatio": max(liquidity['警示股']['entry'],liquidity['警示股']['exit']) if '警示股' in liquidity else 0,
                "fullDeliveryStockRatio": max(liquidity['全額交割股']['entry'], liquidity['全額交割股']['exit']) if '全額交割股' in liquidity else 0,
                "buyHigh": max(liquidity['buy_high']['entry'],liquidity['buy_high']['exit'])  if 'buy_high' in liquidity else 0,
                "sellLow": max(liquidity['sell_low']['entry'],liquidity['sell_low']['exit']) if 'sell_low' in liquidity else 0,
            }
        }



    def run_analysis(self, analysis, display=True, **kwargs):

        # get the instance of analysis
        if isinstance(analysis, str):

            if analysis[-8:] != 'Analysis':
                analysis += 'Analysis'

            # get module
            module_name = 'finlab.analysis.' + analysis[0].lower() + analysis[1:]

            if importlib.util.find_spec(module_name) is None:
                import finlab.analysis as module
                submodules = []
                for submodule in iter_modules(module.__path__):
                    if '_' not in submodule.name:
                        submodules.append(submodule.name[:-8:])

                error = f"Cannot find {module_name}. Possible candidates are " + str(submodules)[1:-1]
                raise Exception(error)

            analysis_module = importlib.import_module(module_name)

            # create an instance from module
            analysis_class = analysis[0].upper() + analysis[1:]

            analysis = getattr(analysis_module, analysis_class)(**kwargs)

        # calculate additional trade info for analysis
        additional_trade_info = analysis.calculate_trade_info(self)
        for v in additional_trade_info:
            self.add_trade_info(*v)

        # analysis and return figure or data as result
        result = analysis.analyze(self)

        if display:
            return analysis.display()

        return result

    def display_mae_mfe_analysis(self, **kwargs):
        return self.run_analysis("MaeMfeAnalysis", **kwargs)
