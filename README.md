# Stock Prediction App

This Streamlit app allows users to predict stock prices for selected stocks (AAPL, GOOG, MSFT, GME) using the Prophet time series forecasting model. The app fetches historical stock data using the Yahoo Finance API, performs predictions, and visualizes the results.

## Author

Hassan Anwar

## Requirements

To run this app, you need to have the following Python packages installed. You can install them using the provided requirements file.

### Install Requirements

```bash
pip install -r requirements.txt
```

## How to Use

1. Run the Streamlit app using the following command:

```bash
streamlit run app.py
```

2. The app will open in your default web browser.

3. Select the stock for prediction using the dropdown menu.

4. Choose the number of years for the prediction using the slider.

5. The app will display the raw data, forecast data, and visualizations.

## App Code Explanation

The app is developed using Python and Streamlit, with the following key libraries:

- `streamlit`: For creating the web app interface.
- `datetime`: For handling date and time.
- `pandas`: For data manipulation.
- `yfinance`: For fetching stock data from Yahoo Finance.
- `prophet`: For time series forecasting.
- `plotly`: For interactive plotting.

The code is organized as follows:

1. Data Loading: Fetches historical stock data using the selected stock symbol.

2. Raw Data Visualization: Plots the raw stock data, including Open and Close prices over time.

3. Time Series Forecasting: Uses the Prophet model to predict future stock prices.

4. Forecast Data Visualization: Displays the forecasted stock prices and related visualizations.

5. Forecast Components: Shows the individual components of the forecast, including trend and seasonality.

## Notes

- The app uses the `yfinance` library to fetch historical stock data.
- The `Prophet` model is trained on the closing prices of the selected stock.
- The app provides interactive plots using the `plotly` library.
