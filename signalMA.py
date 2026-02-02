import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define a function to generate signals based on moving average crossover
def generate_signals(data, short_window=40, long_window=100):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0
    
    # Create short-term simple moving average
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    
    # Create long-term simple moving average
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
    
    # Generate signals
    signals.loc[signals.index[short_window:], 'signal'] = np.where(
        signals['short_mavg'].iloc[short_window:] > signals['long_mavg'].iloc[short_window:], 1.0, 0.0)
    
    # Generate trading orders
    signals['positions'] = signals['signal'].diff()
    
    return signals

# Load historical price data (replace this with your own data)
# For the sake of demonstration, let's use some random price data
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', end='2024-01-01')
prices = np.random.normal(loc=100, scale=5, size=len(dates))
data = pd.DataFrame({'Close': prices}, index=dates)

# Generate trading signals
signals = generate_signals(data)

# Plotting the closing price and moving averages
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price')
plt.plot(signals['short_mavg'], label='40-Day Moving Average')
plt.plot(signals['long_mavg'], label='100-Day Moving Average')

# Plot buy signals
plt.plot(signals.loc[signals.positions == 1.0].index, 
         signals.short_mavg[signals.positions == 1.0],
         '^', markersize=10, color='g', lw=0, label='Buy Signal')

# Plot sell signals
plt.plot(signals.loc[signals.positions == -1.0].index, 
         signals.short_mavg[signals.positions == -1.0],
         'v', markersize=10, color='r', lw=0, label='Sell Signal')

plt.title('Moving Average Crossover Strategy')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid()
plt.show()


