
class STL(object):

    def __init__(self):
        pass

    def stl(self, arr, model='addtive', filt=None,
            freq=None, two_sided=True, extrapolate_trend=0):

        '''
        see https://www.statsmodels.org/stable/generated/statsmodels.tsa.seasonal.seasonal_decompose.html
        for parameter details

        returns
        ===============================
        DecomposeResult
          => A object with seasonal, trend, and resid attributes.
        '''

        result = seasonal_decompose(arr, model='additive', filt=filt, freq=freq,
                                    two_sided=two_sided, extrapolate_trend=extrapolate_trend)
        return result

    def plot_stl_trend(self, arr, ax=None, model='addtive', filt=None,
            freq=None, two_sided=True, extrapolate_trend=0):
        '''
        draw a trend plot from STL(Seasonal and Trend decomposition using Loess)
        see Cleveland, Cleveland, McRae, & Terpenning (1990) for details

        params
        ===============================
        x: array-like, list or pandas.Series
        ax: matplotlib.axes._subplots.AxesSubplot, default=None
          => if None; draw a plot on a new AxesSubplot

        See also
            data_explorer.tsa.TimeSeriesDataExplorer.stl

        return
        ===============================
        ax: AxesSubplot
        '''
        ax = self._check_ax(ax)

        stl = self.stl(arr, model='additive', filt=filt, freq=freq,
                        two_sided=two_sided, extrapolate_trend=extrapolate_trend)
        trend = stl.trend
        title = "STL - Trend"

        self.plot(arr=trend, ax=ax, title=title)

        return ax
        
    def plot_stl_seasonal(self, arr, ax=None):
        '''
        draw a seasonal plot from STL(Seasonal and Trend decomposition using Loess)
        see Cleveland, Cleveland, McRae, & Terpenning (1990) for details

        params
        ===============================
        x: array-like, list or pandas.Series
        ax: matplotlib.axes._subplots.AxesSubplot, default=None
          => if None; draw a plot on a new AxesSubplot

        See also
            data_explorer.tsa.TimeSeriesDataExplorer.stl

        return
        ===============================
        ax: AxesSubplot
        '''

        ax = self._check_ax(ax)

        stl = self.stl(arr, model='additive', filt=filt, freq=freq,
                            two_sided=two_sided, extrapolate_trend=extrapolate_trend)
        seasonal = stl.seasonal
        title = "STL - Seasonality"

        self.plot(arr=seasonal, ax=ax, title=title)

        return ax

    def plot_stl_reminder(self, arr, ax=None):
        '''
        draw a reminder plot from STL(Seasonal and Trend decomposition using Loess)
        see Cleveland, Cleveland, McRae, & Terpenning (1990) for details

        params
        ===============================
        x: array-like, list or pandas.Series
        ax: matplotlib.axes._subplots.AxesSubplot, default=None
            if None; draw a plot on a new AxesSubplot

        See also
            data_explorer.tsa.TimeSeriesDataExplorer.stl

        return
        ===============================
        ax: AxesSubplot
        '''


        ax = self._check_ax(ax)

        stl = self.stl(arr, model='additive', filt=filt, freq=freq,
                         two_sided=two_sided, extrapolate_trend=extrapolate_trend)
        resid = stl.resid
        title = "STL - Reminder"

        self.plot(arr=resid, ax=ax, title=title)

        return ax
