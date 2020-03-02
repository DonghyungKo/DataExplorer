import datetime
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as sp
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from ._errors import IndexTypeError, ParameterTypeError

class SignleTimeSeriesExplorer(object):
    ''' a class for analyzing single time-series data '''

    def __init__(self):
        pass

    # main method
    def plot_all(self, arr, ma_period=5):
        '''
        show various plots of given arr
         - raw time-series
         - moving average
         - distribution plot
         - Q-Q plot
         - acf plot
         - pacf plot
         - violin plot (weekday group)
         - strip plot (day of month group)

        params
        ========================================
        x: array-like, list or pandas.Series
        ma_period: int, default = 5
            past periods for calculating moving average

        return
        =========================================
        fig: matplotlib.figure.Figure

        '''
        fig = plt.figure(figsize=(13, 40))
        axes = []

        axes.append(fig.add_subplot(10, 1, 1)) # 0: (1, ~)
        axes.append(fig.add_subplot(10, 2, 3)) # 1: (3, 1)
        axes.append(fig.add_subplot(10, 2, 4)) # 2: (3, 2)
        axes.append(fig.add_subplot(10, 2, 5)) # 3: (4, 1)
        axes.append(fig.add_subplot(10, 2, 6)) # 4: (4, 2)
        axes.append(fig.add_subplot(10, 2, 7)) # 5: (5, 1)
        axes.append(fig.add_subplot(10, 2, 8)) # 6: (5, 2)

        self.plot(arr, ax=axes[0], title="Time Series", label="Raw") # raw time-series
        self.plot_ma(arr, period=ma_period, ax=axes[0], title="", label='Moving Average') # moving average
        self.plot_dist(arr, ax=axes[1]) # Distplot
        self.plot_qq(arr, ax=axes[2]) # Q-Q
        self.plot_acf(arr, ax=axes[3]) # ACF
        self.plot_pacf(arr, ax=axes[4]) # PACF
        self.plot_violin_weekday(arr, ax=axes[5]) # Violin by weekday groups
        self.plot_strip_day_of_month(arr, ax=axes[6]) # strip plot by day of month groups

        plt.show()
        return fig


    ###########################
    ######### Plot ############
    ###########################


    def plot(self, arr, ax=None, title="Time Series", label=''):
        ''' draw a time-series plot of given arr

        params
        ===============================
        x: array-like, list or pandas.Series
        ax: matplotlib.axes._subplots.AxesSubplot, default=None
          if None; draw a plot on a new AxesSubplot
        title: str
        label: str

        return
        ===============================
        ax: AxesSubplot
        '''

        ax = self._check_ax(ax)

        ax.plot(arr, label=label)

        if title:
            ax.set_title(title, fontsize=15)

        if label:
            ax.legend(loc='best')

        return ax

    def plot_ma(self, arr, period, ax=None, title='Moving Average', label=""):
        ''' draw a moving average plot of given arr

        params
        ===============================
        x: array-like, list or pandas.Series
        period: int, past period used to calculate moving average
        ax: matplotlib.axes._subplots.AxesSubplot, default=None
          if None; draw a plot on a new AxesSubplot
        title: str
        label: str

        return
        ===============================
        ax: AxesSubplot
        '''

        ax = self._check_ax(ax)
        ma_arr = arr.rolling(period).mean()

        self.plot(ma_arr, ax, title, label)

        return ax

    def plot_dist(self, arr, ax=None):
        '''
        draw a distribution plot of given arr

        params
        =========================
        x: array-like, list or pandas.Series
        ax: matplotlib.axes._subplots.AxesSubplot, default=None
            if None; draw a plot on a new AxesSubplot

        return
        ===============================
        ax: AxesSubplot
        '''

        ax = self._check_ax(ax)

        sns.distplot(arr, ax=ax, fit=sp.norm)
        ax.set_title("Data Distribution", fontsize=15)
        ax.set_xlabel("")

        return ax

    def plot_acf(self, arr, ax=None):
        '''
        draw a acf(Auto-Correlation Function) plot of given arr

        params
        =========================
        x: array-like, list or pandas.Series
        ax: matplotlib.axes._subplots.AxesSubplot, default=None
            if None; draw a plot on a new AxesSubplot

        return
        ===============================
        ax: AxesSubplot
        '''

        ax = self._check_ax(ax)

        plot_acf(arr, ax=ax)
        ax.set_title('ACF Plot', fontsize=15)

        return ax

    def plot_pacf(self, arr, ax=None):
        '''
        draw a pacf(Partial Auto-Correlation Function) plot of given arr

        params
        =========================
        x: array-like, list or pandas.Series
        ax: matplotlib.axes._subplots.AxesSubplot, default=None
            if None; draw a plot on a new AxesSubplot

        return
        ===============================
        ax: AxesSubplot
        '''

        ax = self._check_ax(ax)

        plot_pacf(arr, ax=ax)
        ax.set_title('PACF Plot', fontsize=15)

        return ax

    def plot_qq(self, arr, ax=None):
        '''
        draw a Q-Q(Quantile-Quantile) plot of given arr

        params
        =========================
        x: array-like, list or pandas.Series
        ax: matplotlib.axes._subplots.AxesSubplot, default=None
            if None; draw a plot on a new AxesSubplot

        return
        ===============================
        ax: AxesSubplot
        '''

        ax = self._check_ax(ax)

        sp.probplot(arr, plot=ax)
        ax.set_title("Q-Q Plot", fontsize=15)
        ax.set_xlabel("")
        ax.set_ylabel("")

        return ax

    def plot_violin_weekday(self, arr, ax=None):
        '''
        draw a violin-plot of given arr after grouping by weekdays

        params
        =========================
        x: pandas.Series
            the type of given arr index must be Timestamp
        ax: matplotlib.axes._subplots.AxesSubplot
            default=None, if None: draw a plot on a new AxesSubplot

        return
        ===============================
        ax: AxesSubplot
        '''

        ax = self._check_ax(ax)
        self._check_arr_index_type(arr)

        dates = list(arr.index)
        values = list(arr)

        weekday_dict = {
            0 : "Monday",
            1 : "Tuesday",
            2 : 'Wednesday',
            3 : "Thursday",
            4 : 'Friday',
            5 : 'Satureday',
            6 : 'Sunday',
        }
        weekdays = [weekday_dict[t.weekday()] for t in dates]

        df = pd.DataFrame({
            'value' : values,
            'weekday' : weekdays
        })

        sns.violinplot(x='weekday', y='value', data=df, ax=ax, order=list(self.weekday_dict.values()))
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title("Weekday Violin Plot", fontsize=15)

        return ax

    def plot_strip_day_of_month(self, arr, ax=None):
        '''
        draw a strip-plot of given arr after grouping by day of month

        params
        =========================
        x: pandas.Series
            the type of given arr index must be Timestamp
        ax: matplotlib.axes._subplots.AxesSubplot
            default=None, if None: draw a plot on a new AxesSubplot

        return
        ===============================
        ax: AxesSubplot
        '''

        ax = self._check_ax(ax)
        self._check_arr_index_type(arr)

        dates = list(arr.index)
        values = list(arr)
        days = [t.day for t in dates]

        df = pd.DataFrame({
            'value' : values,
            'day' : days
        })

        sns.stripplot(x='day', y='value', data=df, ax=ax)
        ax.set_ylabel("")
        ax.set_title("Day of Month Stripplot Plot", fontsize=15)

        return ax

    # support methods
    def _check_ax(self, ax):
        ''' 지정된 AxesSubplot이 없으면, 새로운 figure를 생성하는 함수 '''

        if ax is None:
            _, ax = plt.subplots()

        return ax

    def _check_arr_index_type(self, arr):
        ''' 입력받은 pandas.Series 객체의 index가 Timestamp 자료형인지 확인하는 함수

        params
        ==========================================
        x: pandas.Series
        '''

        index = arr.index[0]

        if not (isinstance(index, pd._libs.tslibs.timestamps.Timestamp)
                or isinstance(index, datetime.datetime)):

            msg = "Array Index Type ERROR: Must be datetime or timestamp, but given {}".format(type(index))
            raise IndexTypeError(msg)

    '''
    def plot_weekly_sum(self, arr, ax=None):
        #주차별 합을 계산하여 barplot을 그리는 함수

        ax = self._check_ax(ax)
        self._check_arr_index_type(arr)

        weekly_sum_arr = arr.groupby([datetime.date.isocalendar(t)[1] for t in arr.index]).sum()

        ax.bar(list(weekly_sum_arr.index), weekly_sum_arr.values)
        ax.set_title("Weekly Sum", fontsize=15)

        return ax
    '''


class MultiTimeSeriesExplorer(object):
    ''' a class for analyzing multiple time-series data '''

    def __init__(self):
        pass


    def plot_corr_heatmap(self, x, ax=None, method='pearson', min_periods=1, cmap='Blues'):
        '''
        draw a pearson correlation heatmap for given arrays

        params
        ========================================
        x: pandas.DataFrame or 2D array-like

        method: str, default='pearson'
          'pearson', 'kendall' or 'spearman'

        min_periods: int, optional
          Minimum number of observations required per pair of columns to have a valid result.
          Currently only available for Pearson and Spearman correlation.

        cmap: matplotlib colormap name or object, or list of colors, optional

        return
        ===============================
        ax: AxesSubplot
        '''
        ax = self._check_ax(ax)

        if not isinstance(x, pd.DataFrame):
            x = pd.DataFrame(x)

        corr_df = x.corr(method=method)

        sns.heatmap(corr_df, ax=ax, annot=True, fmt='.2f', cmap=cmap)
        ax.set_ylim(len(corr_df)+0.5, -0.5)

    # support methods
    def _check_ax(self, ax):
        ''' 지정된 AxesSubplot이 없으면, 새로운 figure를 생성하는 함수 '''

        if ax is None:
            _, ax = plt.subplots()

        return ax
