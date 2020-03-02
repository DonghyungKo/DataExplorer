from setuptools import setup, find_packages

setup(
    name = 'TimeSeriesDataExplorer',
    version = '0.0.1',
    description = 'a library for time-series data analysis' ,
    author = 'Donghyung Ko',
    author_email = 'koko8624@gmail.com',
    license='MIT',
    url = 'https://github.com/DonghyungKo/TimeSeriesDataExplorer',
    download_url = 'https://github.com/DonghyungKo/TimeSeriesDataExplorer/archive/master.zip',
    install_requires = [],
    packages = find_packages(),
    keywords = ['time-series', 'time series', 'data analysis'],
    python_requires = '>=3.7',
    package_data = {},
    zip_safe = False,
    long_description=open('README.md').read(),
    
)
