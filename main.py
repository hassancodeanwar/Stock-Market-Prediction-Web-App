import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objects as go

START = "2015-01-01"  # Updated to start from 2015
END = "2024-12-31"  # Explicitly setting end date to 2024

st.title("Stock Prediction App")

stocks = ('AAPL', 'GOOG', 'MSFT', 'GME')
select_stock = st.selectbox('Select a dataset for prediction', stocks)

n_years = st.select_slider('Years of prediction', options=range(1, 5))
period = n_years * 365

@st.cache_data
def load_data(ticker):
    try:
        st.text(f"Fetching data for {ticker}...")
        data = yf.download(ticker, START, END)
        
        if data.empty:
            st.warning(f"No data available for {ticker} in the selected date range. Try selecting a different stock or adjusting the date range.")
            return pd.DataFrame()
        
        data.reset_index(inplace=True)  # Ensure 'Date' is a column
        return data
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return pd.DataFrame()

data_load_state = st.text('Loading data...')
data = load_data(select_stock)
data_load_state.text('Loading data... Done!')

if data.empty:
    st.stop()

st.subheader('Raw data')
st.write(data.tail())

st.write("Columns in data:", data.columns)

def plot_raw_data():
    required_columns = {'Date', 'Open', 'Close'}
    if not required_columns.issubset(data.columns):
        st.error(f"Missing required columns: {required_columns - set(data.columns)}")
        return
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Stock Open', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock Close', line=dict(color='red')))
    fig.layout.update(title_text='Time Series Data', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

df_train = data[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail(10))

st.write('Forecast plot')
fig1 = plot_plotly(m, forecast)
fig1['data'][0]['line']['color'] = 'blue'
fig1['data'][1]['line']['color'] = 'orange'
st.plotly_chart(fig1)

st.write('Forecast components')
fig2 = m.plot_components(forecast)
st.write(fig2)
