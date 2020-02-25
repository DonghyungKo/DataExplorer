import datetime
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import pandas as pd
import scipy.stats as sp
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose

#from errors import IndexTypeError, ParameterTypeError

class Explorer(object):

    def __init__(self):

        self.weekday_dict = {
            0 : "Monday",
            1 : "Tuesday",
            2 : 'Wednesday',
            3 : "Thursday",
            4 : 'Friday',
            5 : 'Satureday',
            6 : 'Sunday',
        }

    # main method
    def show_all(self, arr, freq=7):

        fig = plt.figure(figsize=(13, 40))
        axes = []

        axes.append(fig.add_subplot(10, 1, 1)) # 0: (1, ~)
        axes.append(fig.add_subplot(10, 2, 3)) # 1: (2, 1)
        axes.append(fig.add_subplot(10, 2, 4)) # 2: (2, 2)
        axes.append(fig.add_subplot(10, 2, 5)) # 3: (3, 1)
        axes.append(fig.add_subplot(10, 2, 6)) # 4: (3, 2)
        axes.append(fig.add_subplot(10, 2, 7)) # 5: (4, 1)
        axes.append(fig.add_subplot(10, 2, 8)) # 6: (4, 2)

        self.plot(arr, ax=axes[0]) # 원시계열
        self.plot_dist(arr, ax=axes[1]) # Distplot
        self.plot_qq(arr, ax=axes[2]) # Q-Q 플롯
        self.plot_acf(arr, ax=axes[3]) # ACF
        self.plot_pacf(arr, ax=axes[4]) # PACF
        self.plot_weekday_violin(arr, ax=axes[5]) # Violin
        self.plot_day_of_month(arr, ax=axes[6]) # 월 중, 일별 분포

        # Daily Frequency 자료인 경우
        index = arr.index
        if isinstance(index[0], pd._libs.tslibs.timestamps.Timestamp):

            axes.append(fig.add_subplot(10, 1, 5)) # 7 (5,~)
            axes.append(fig.add_subplot(10, 1, 6)) # 8 (6, ~)
            axes.append(fig.add_subplot(10, 1, 7)) # 9 (7, ~)

            self.plot_stl_trend(arr, ax=axes[7], freq=freq) # Trend 시계열
            self.plot_stl_seasonality(arr, ax=axes[8], freq=freq) # Seasonality 시계열
            self.plot_stl_resid(arr, ax=axes[9], freq=freq) # Resid 시계열

        plt.show()

    #########################
    ######### Cal ###########
    #########################

    def cal_stl_trend(self, arr, freq):

        result = seasonal_decompose(arr, model='additive', freq=freq)
        return result.trend

    def cal_stl_seasonal(self, arr, freq):

        result = seasonal_decompose(arr, model='additive', freq=freq)
        return result.seasonal

    def cal_stl_resid(self, arr, freq):

        result = seasonal_decompose(arr, model='additive', freq=freq)
        return result.resid


    ###########################
    ######### Plot ############
    ###########################


    def plot(self, arr, ax=None, title='Raw Time Series'):
        ''' 시계열 그래프를 그리는 함수

        params
        ===============================
        arr: list or pandas.Series
        ax: matplotlib.axes._subplots.AxesSubplot, default=None
         -> 그래프를 그릴 axes, None인 경우, 새로운 figure를 생성하고 그래프를 그림
        '''
        ax = self._check_ax(ax)

        ax.plot(arr)
        ax.set_title(title, fontsize=15)

    def plot_ma(self, arr, period, ax=None):
        ''' 시계열 이동평균선을 그리는 함수

        params
        ===============================
        period: int, 이동평균선 계산 기간
        '''

        ax = self._check_ax(ax)

        ma_arr = arr.rolling(period).mean()
        title = "{} Days Moving Average".format(period)

        self.plot(ma_arr, ax, title)

    def plot_stl_trend(self, arr, freq, ax=None):
        '''STL 분해 후, Trend plot을 그리는 함수'''

        ax = self._check_ax(ax)

        trend = self.cal_stl_trend(arr, freq=freq)
        title = "STL - Trend"

        self.plot(arr=trend, ax=ax, title=title)

    def plot_stl_seasonality(self, arr, freq, ax=None):
        '''STL 분해 후, Seasonality plot을 그리는 함수'''

        ax = self._check_ax(ax)

        seasonal = self.cal_stl_seasonal(arr, freq=freq)
        title = "STL - Seasonality"

        self.plot(arr=seasonal, ax=ax, title=title)

    def plot_stl_resid(self, arr, freq, ax=None):
        '''STL 분해 후, Residual plot을 그리는 함수'''

        ax = self._check_ax(ax)

        resid = self.cal_stl_resid(arr, freq=freq)
        title = "STL - Residual"

        self.plot(arr=resid, ax=ax, title=title)

    def plot_dist(self, arr, ax=None):
        '''데이터의 분포도(Distribution Plot)를 그리는 함수'''

        ax = self._check_ax(ax)

        sns.distplot(arr, ax=ax, fit=sp.norm)
        ax.set_title("Data Distribution", fontsize=15)
        ax.set_xlabel("")

    def plot_acf(self, arr, ax=None):
        ''' ACF(AutoCorrelation Function) plot을 그리는 함수'''

        ax = self._check_ax(ax)

        plot_acf(arr, ax=ax)
        ax.set_title('ACF Plot', fontsize=15)

    def plot_pacf(self, arr, ax=None):
        ''' PACF(Partial AutoCorrelation Function) plot을 그리는 함수'''

        ax = self._check_ax(ax)

        plot_pacf(arr, ax=ax)
        ax.set_title('PACF Plot', fontsize=15)

    def plot_qq(self, arr, ax=None):
        ''' Q-Q plot을 그리는 함수 '''

        ax = self._check_ax(ax)

        sp.probplot(arr, plot=ax)
        ax.set_title("Q-Q Plot", fontsize=15)
        ax.set_xlabel("")
        ax.set_ylabel("")

    def plot_stl(self, arr):

        result = seasonal_decompose(arr, model='additive')

        fig = result.plot()
        fig.set_size_inches(10, 10)

    def plot_weekday_violin(self, arr, ax=None):
        ''' 요일별로 구분하여 Violin plot을 그리는 함수 '''

        ax = self._check_ax(ax)
        self._check_arr_index_type(arr)

        dates = list(arr.index)
        values = list(arr)
        weekdays = [self.weekday_dict[t.weekday()] for t in dates]

        df = pd.DataFrame({
            'value' : values,
            'weekday' : weekdays
        })

        sns.violinplot(x='weekday', y='value', data=df, ax=ax, order=list(self.weekday_dict.values()))
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title("Weekday Violin Plot", fontsize=15)

    '''
    def plot_weekly_sum(self, arr, ax=None):
        #주차별 합을 계산하여 barplot을 그리는 함수

        ax = self._check_ax(ax)
        self._check_arr_index_type(arr)

        weekly_sum_arr = arr.groupby([datetime.date.isocalendar(t)[1] for t in arr.index]).sum()

        ax.bar(list(weekly_sum_arr.index), weekly_sum_arr.values)
        ax.set_title("Weekly Sum", fontsize=15)
    '''

    def plot_day_of_month(self, arr, ax=None):
        ''' 월 중, 일별 분포(stripplot)를 그리는 함수 '''

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

    # support methods
    def _check_ax(self, ax):

        if ax is None:
            _, ax = plt.subplots()

        return ax

    def _check_arr_index_type(self, arr):

        index = arr.index[0]

        if not isinstance(index, pd._libs.tslibs.timestamps.Timestamp):

            msg = "Array Index Type ERROR: Must be pandas._libs.tslibs.timestamps.Timestamp, but given {}".format(type(index))
            raise IndexTypeError(msg)
