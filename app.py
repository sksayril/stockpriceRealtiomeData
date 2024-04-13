import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Set the page configuration
st.set_page_config(page_title="Real-time Stock Data", page_icon="📈")

# Title for your application
st.title('Stock Data Viewer')

# User input for the stock symbol
ticker_symbol = st.text_input("Enter Stock Ticker:", "ZOMATO.NS")

# Use yfinance to fetch data
def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    # Fetching 1-year historical data
    hist = stock.history(period="1y")
    return hist

# Display the stock data
if ticker_symbol:
    df = fetch_data(ticker_symbol)
    
    if not df.empty:
        # Display the last update time
        st.write(f"Last updated at: {pd.Timestamp.now()}")

        # Extract the most recent closing price
        last_close_price = df['Close'].iloc[-1]

        # Display the current price of the stock
        st.markdown(f"**Current Price:** ₹{last_close_price:,.2f} INR")

        # Create a candlestick chart using Plotly
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    increasing_line_color='green', decreasing_line_color='red')])

        fig.update_layout(title='1 Year Stock Movement',
                          xaxis_title='Date',
                          yaxis_title='Price (INR)',  # Ensure it's clear we're using INR
                          xaxis_rangeslider_visible=False)  # Hides the range slider

        # Update y-axis to reflect currency format (optional, for enhanced readability)
        fig.update_yaxes(tickprefix="₹", tickformat=',.2f')

        st.plotly_chart(fig)
        # st.experimental_rerun()

    else:
        st.error("No data found for the given ticker symbol. Please try another symbol.")
