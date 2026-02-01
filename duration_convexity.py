import numpy as np
import pandas as pd

# Given bond details
face_value = 1000  # Face value of the bond
coupon_rate = 0.05  # Annual coupon rate (5%)
years_to_maturity = 10  # Years until maturity
ytm = 0.06  # Yield to maturity (6% annually)
frequency = 2  # Semiannual payments

# Compute per-period values
coupon_payment = (coupon_rate / frequency) * face_value  # Coupon per period
periods = years_to_maturity * frequency  # Total number of periods
ytm_per_period = ytm / frequency  # YTM per period

# Compute cash flows and present values
time_periods = np.arange(1, periods + 1)  # Time periods (1 to periods)
cash_flows = np.full(periods, coupon_payment)  # Regular coupon payments
cash_flows[-1] += face_value  # Add face value at the last period

# Compute discount factors
discount_factors = 1 / (1 + ytm_per_period) ** time_periods

# Compute present value of each cash flow
pv_cash_flows = cash_flows * discount_factors

# Compute bond price
bond_price = pv_cash_flows.sum()

# Compute weights (PV of CFs / Bond Price)
weights = pv_cash_flows / bond_price

# Compute duration (sum of t * weight) and modified duration
duration = np.sum(time_periods * weights)
modified_duration = duration / (1 + ytm_per_period)

# Compute convexity (sum of t^2 * weight)
convexity = np.sum((time_periods**2) * weights) / (1 + ytm_per_period) ** 2

# Define yield change
delta_yield = 0.01  # 1% change in yield

# Compute percentage price change
percent_price_change = -modified_duration * delta_yield + 0.5 * convexity * (delta_yield**2)

# Compute new price
new_price = bond_price * (1 + percent_price_change)

# Create a DataFrame with detailed calculations
df_working = pd.DataFrame({
    "Time Periods (t)": time_periods,
    "Cash Flows": cash_flows,
    "Discount Factor": discount_factors,
    "Present Value of Cash Flows": pv_cash_flows,
    "Weight (PV / Price)": weights,
    "t * Weight (for Duration)": time_periods * weights,
    "t^2 * Weight (for Convexity)": (time_periods**2) * weights
})

# Add summary calculations
summary_data = pd.DataFrame({
    "Parameter": [
        "Bond Price",
        "Modified Duration",
        "Convexity",
        "Yield Change (Δy)",
        "Percentage Price Change",
        "New Price"
    ],
    "Value": [
        bond_price,
        modified_duration,
        convexity,
        delta_yield,
        percent_price_change,
        new_price
    ]
})

# Define file path
file_path_working = "C:/Users/skarb/Google Drive/Coding/py_masterdir/Bond_Duration_Convexity_Working.xlsx"

# Write to Excel with multiple sheets
with pd.ExcelWriter(file_path_working) as writer:
    df_working.to_excel(writer, sheet_name="Duration & Convexity", index=False)
    summary_data.to_excel(writer, sheet_name="Summary", index=False)

# Provide the file path for download
file_path_working
