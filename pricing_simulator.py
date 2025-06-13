import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pricing Simulator", layout="centered")
st.title("💰 Pricing Simulator")

st.markdown("""
This tool helps you simulate and benchmark pricing models:
- **Cost-Plus**: Add a margin to your total cost to ensure profitability
- **Tiered Pricing**: Set different price levels based on quantity purchased
- **Value-Based Pricing**: Price based on what the customer is willing to pay

It also supports competitive analysis and helps you assess profit margins to inform smart pricing strategies.
""")

# Upload cost components
st.header("📦 Input Your Cost Structure")
st.markdown("""
Input the core components of your unit economics. These are critical to build a sound pricing model:
- **Fixed Cost**: Infrastructure, licensing, or base costs not tied to volume
- **Variable Cost**: Raw material, labor, etc. per unit
- **Service Overhead**: Support, training, or delivery cost per unit
""")
fixed_cost = st.number_input("Fixed Cost ($)", min_value=0.0, step=1.0)
variable_cost = st.number_input("Variable Cost per Unit ($)", min_value=0.0, step=0.1)
service_cost = st.number_input("Service Overhead per Unit ($)", min_value=0.0, step=0.1)

# Upload competitor pricing
st.header("📊 Competitor Pricing (Optional)")
st.markdown("""
Upload a CSV with competitor pricing to benchmark your proposed price. Columns should include:
- `Competitor`
- `Price`
This enables you to position your offering relative to market trends.
""")
comp_file = st.file_uploader("Upload CSV with Competitor Prices", type=["csv"])

if comp_file:
    comp_df = pd.read_csv(comp_file)
    st.write("### Competitor Pricing Data")
    st.dataframe(comp_df)

# Select pricing strategy
st.header("🧮 Choose Pricing Strategy")
st.markdown("""
Select a strategy to simulate pricing outcomes:
- **Cost-Plus**: Calculates price using a markup over total cost
- **Tiered**: Uses quantity-based breakpoints to simulate average pricing
- **Value-Based**: Directly uses perceived customer value
""")
strategy = st.selectbox("Pricing Strategy", ["Cost-Plus", "Tiered", "Value-Based"])

# Units for value-based pricing
estimated_value = 0
if strategy == "Value-Based":
    estimated_value = st.number_input("Customer Perceived Value ($)", min_value=0.0, step=0.1)

# Set margin / tiers
if strategy == "Cost-Plus":
    margin_pct = st.slider("Target Margin %", 0, 100, 30)
    price = (fixed_cost + variable_cost + service_cost) * (1 + margin_pct / 100)

elif strategy == "Tiered":
    st.markdown("""Define price tiers by quantity range:
    Example: 1-100 units = $25, 101-500 units = $22, etc.
    """)
    tiers = st.text_area("Enter tiers (format: min,max,price)", "1,100,25\n101,500,22\n501,1000,20")
    tier_lines = [line.split(',') for line in tiers.strip().split('\n') if line]
    tier_df = pd.DataFrame(tier_lines, columns=["Min Units", "Max Units", "Price"])
    tier_df = tier_df.astype({"Min Units": int, "Max Units": int, "Price": float})
    st.write("### Tier Table")
    st.dataframe(tier_df)
    price = tier_df['Price'].mean()  # Avg for estimate

elif strategy == "Value-Based":
    price = estimated_value

# Output result
st.header("📈 Suggested Price & Profit")
total_cost = fixed_cost + variable_cost + service_cost
profit = price - total_cost
margin = (profit / price) * 100 if price else 0

st.metric("Recommended Price", f"${price:,.2f}")
st.metric("Estimated Profit per Unit", f"${profit:,.2f}")
st.metric("Estimated Margin %", f"{margin:.2f}%")

# Compare to competitors
if comp_file and "Price" in comp_df.columns:
    comp_df["Delta vs. Recommended"] = comp_df["Price"] - price
    st.write("### Price Benchmark vs Competitors")
    st.dataframe(comp_df[["Competitor", "Price", "Delta vs. Recommended"]])
    st.markdown("""
    This comparison helps evaluate whether your pricing is aggressive, competitive, or premium in the market. 
    Aim for a value proposition that aligns with your business goals (volume, margin, or positioning).
    """)
