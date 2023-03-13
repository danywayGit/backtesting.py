# backtesting.py

## Based on https://kernc.github.io/backtesting.py/

### Get Binance data

Currently only PowerShell version, I'll work to do the same in Python

https://github.com/danywayGit/DownloadBinanceHistorycalData
### Installation

1. Create a virtual environment `python3 -m venv venv-backtesting`
1. Activate the virtual environement `venv-backtesting\Scripts\activate`
1. Install requirements `pip3 install -r requirements.txt`

### Know issues

1. If bt.plot does not display any chart, and if you see the message `console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing")` by checking the source code of the html file try to downgrade the bokek 3.0.3
1. `pip uninstall -y bokeh && pip install bokeh==2.4.3`
