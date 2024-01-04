import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objects as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

stocks = ('AAPL', 'GOOG', 'MSFT', 'GME')
select_stock = st.selectbox('Selected dataset for prediction', stocks)

n_years = st.select_slider('Years of prediction', options=range(1, 5))
period = n_years * 365

@st.cache_data
def load_data(ticker):
    try:
        print("Fetching data for", ticker)
        data = yf.download(ticker, START, TODAY)
        if data.empty:
            return pd.DataFrame()  # Return an empty DataFrame in case of no data
        else:
            print("Fetched data shape:", data.shape)
            data.reset_index(inplace=True)
            print("Fetched data columns:", data.columns)
        return data
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

data_load_state = st.text('Load data...')
data = load_data(select_stock)
data_load_state.text('Loading data... Done!')

if data.empty:
    st.warning(f"No data available for {select_stock} in the selected date range.")
else:
    print("Data loaded:", data.head())
    st.subheader('Raw data')
    st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()

    # Specify colors for each trace
    colors = ['green', 'red']

    # Add trace for 'Stock_Open'
    fig.add_trace(go.Scatter(x=data['Date'],
                             y=data['Open'],
                             name='Stock_Open',
                             line=dict(color=colors[0])))

    # Add trace for 'Stock_Close'
    fig.add_trace(go.Scatter(x=data['Date'],
                             y=data['Close'],
                             name='Stock_Close',
                             line=dict(color=colors[1])))

    fig.layout.update(title_text='Time Series Data',
                      xaxis_rangeslider_visible=True)

    st.plotly_chart(fig)

plot_raw_data()

df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={'Date': 'ds', 'Close': 'y'})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail(10))

st.write('Forecast plot')
fig1 = plot_plotly(m, forecast)

# Modify the line colors in the figure
fig1['data'][0]['line']['color'] = 'blue'
fig1['data'][1]['line']['color'] = 'orange'

st.plotly_chart(fig1)

st.write('Forecast components')
fig2 = m.plot_components(forecast)
st.write(fig2)
