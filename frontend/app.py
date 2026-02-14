import streamlit as st
import requests

# Setup the Page
st.set_page_config(page_title="Stock Price Predictor", page_icon="📈")
st.title("📈 Stock Price Prediction App")
st.markdown("Enter the stock details below to get a next-day price prediction.")

# User Inputs
col1, col2 = st.columns(2)


# columns for input fields
with col1:
    close_price = st.number_input(
        "Current Price ($)", 
        value=100.0,
        help="The price the stock closed at yesterday."
    )
    sma_10 = st.number_input(
        "Short-Term Trend (10 Days)", 
        value=100.0,
        help="The average price over the last 10 days. (Technical: SMA_10)"
    )

with col2:
    sma_50 = st.number_input(
        "Long-Term Trend (50 Days)", 
        value=100.0,
        help="The average price over the last 50 days. (Technical: SMA_50)"
    )
    volatility = st.number_input(
        "Market Risk / Volatility", 
        value=2.5,
        help="How much the price is jumping up and down. Higher numbers mean more risk."
    )


# The Centered "Predict" Button
# create 3 columns: [Empty space] [Button] [Empty space]
# The middle column is where the button sits.
c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    # use_container_width=True makes the button fill the middle column
    predict_btn = st.button("Analyze & Predict Price", use_container_width=True)
    
# The "Predict" Button
if predict_btn:
    # Prepare the data payload 
    payload = {
        "Close": close_price,
        "SMA_10": sma_10,
        "SMA_50": sma_50,
        "Volatility": volatility
    }

    # Define API URL
    API_URL = "https://stockpredictionmlops-production.up.railway.app/predict"  

    try:
        # Send the request
        with st.spinner("Calculating..."):
            response = requests.post(API_URL, json=payload)
            
        # Handle the response
        if response.status_code == 200:
            data = response.json()
            prediction = data["predicted_price"]
            st.success(f"💰 Predicted Price: ${prediction:.2f}")
        else:
            st.error(f"Error: {response.text}")
            
    except Exception as e:
        st.error(f"Connection Failed: {e}")

st.markdown("<br><br><br><br>", unsafe_allow_html=True)
# Footer

st.markdown(
    """
    <div style="text-align: center;">
        <p>Built with 🖤 by <a href="https://www.linkedin.com/in/hanseeka-dhingana/" target="_blank">Hanseeka Dhingana</a></p>
        <p style="font-size: 0.8em;">Powered by FastAPI & Railway 🚅</p>
    </div>
    """,
    unsafe_allow_html=True
)