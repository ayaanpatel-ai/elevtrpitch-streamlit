import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Custom CSS
st.markdown("""
<style>
/* Pale Turquoise color */
:root {
    --accent-color: #AFEEEE;
}

/* Style sliders track and handles */
input[type="range"] {
    accent-color: var(--accent-color);
}

/* Style buttons */
.stButton > button {
    background-color: var(--accent-color);
    color: black;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    padding: 0.4em 1em;
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #90e0d0;
}

/* Style text inputs and textareas */
input[type="text"], textarea {
    background-color: white;
    color: black;
    border: 2px solid var(--accent-color);
    border-radius: 5px;
    padding: 0.4em;
    font-weight: bold;
}

input[type="text"]:focus, textarea:focus {
    outline: none;
    border-color: #66cdaa;
    box-shadow: 0 0 5px var(--accent-color);
}
</style>
""", unsafe_allow_html=True)

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# App Title and Description
st.title("elevtrpitch.ai")
st.caption("Created by Ayaan Patel")

st.markdown("""
 **elevtrpitch.ai** is an AI-powered elevator pitch analyzer. It analyzes a pitch based on business metrics and an elevator pitch that
    the user will input, which will be evaluated by the VADER sentiment analysis library.
""")

st.caption("version 3.3.7")

# Company name input
company_name = st.text_input("Company Name:", "")

st.markdown("""
Below, you'll see sliders with metrics such as market size, product uniqueness, and more.  
Drag the sliders to rate each metric on a scale from 0 to 10, with 0 being the lowest and 10 the highest.  
Use the investment amount slider to choose how much funding you're requesting.
""")

# Sliders for metrics
market_size = st.slider("**Market Size**:", 0.0, 10.0, 5.0, 0.1)
product_uniqueness = st.slider("**Product Uniqueness**:", 0.0, 10.0, 5.0, 0.1)
team_experience = st.slider("**Team Experience**:", 0.0, 10.0, 5.0, 0.1)
revenue_model = st.slider("**Revenue Model Success Potential**:", 0.0, 10.0, 5.0, 0.1)
sales_till_date = st.slider("**Sales Till Date**:", 0.0, 10.0, 5.0, 0.1)
investment_asked = st.slider("**Amount of Investment Asked**:", 0, 1000000, 500000, 10000)

# Pitch input
pitch = st.text_area("**Your Pitch**:", height=150, placeholder="Type your startup pitch here...\n(Tap outside or scroll down to analyze)")

# Sentiment Analysis
st.markdown("### Sentiment Analysis")
if pitch.strip():
    vs = analyzer.polarity_scores(pitch)
    compound = vs['compound']
    if compound >= 0.05:
        sentiment_label = "POSITIVE"
    elif compound <= -0.05:
        sentiment_label = "NEGATIVE"
    else:
        sentiment_label = "NEUTRAL"
    st.write(f"Sentiment: **{sentiment_label}** (compound score: {compound:.3f})")
else:
    st.write("Enter a pitch above to see sentiment analysis.")

# Polarity scoring logic
def polarity_score():
    if not pitch.strip():
        return 0
    comp = analyzer.polarity_scores(pitch)['compound']
    if comp >= 0.6:
        return 10
    elif comp >= 0.3:
        return 5
    else:
        return 0

# Investment score logic based on context
def invest_score_contextual():
    ask = investment_asked
    core_avg = (market_size + product_uniqueness + team_experience + revenue_model + sales_till_date) / 5
    if ask > 750000 and core_avg < 6:
        return 2
    elif ask > 600000 and core_avg < 5:
        return 1
    elif 300000 <= ask <= 600000:
        return 10
    elif ask < 200000 and core_avg > 7:
        return 4
    else:
        return 6

# Score button
if st.button("Show Scores"):
    core_avg = (market_size + product_uniqueness + team_experience + revenue_model + sales_till_date) / 5
    pol_score = polarity_score()
    invest_score = invest_score_contextual()

    st.write("### Your Scores:")
    st.write(f"- Company Name: {company_name}")
    st.write(f"- Market Size: {market_size}")
    st.write(f"- Product Uniqueness: {product_uniqueness}")
    st.write(f"- Team Experience: {team_experience}")
    st.write(f"- Revenue Model: {revenue_model}")
    st.write(f"- Sales Till Date: {sales_till_date}")
    st.write(f"- Amount of Investment Asked: ${investment_asked:,}")
    st.write(f"- Core Metrics Average: {core_avg:.2f}")
    st.write(f"- Polarity Score (from VADER): {pol_score}")
    st.write(f"- Contextual Investment Score: {invest_score}")

    total_score = (
        1.5 * market_size +
        1.2 * product_uniqueness +
        1.3 * team_experience +
        revenue_model +
        1.4 * sales_till_date +
        invest_score +
        2 * pol_score
    )

    st.write(f"### Final Weighted Score: {total_score:.2f}")

    if total_score <= 20:
        st.error("Extremely weak. I'm out!")
    elif total_score <= 30:
        st.warning("Pretty weak. Needs improvement in most areas. I'm out!")
    elif total_score <= 40:
        st.info("Some strengths, but lacks polish. I'm out!")
    elif total_score <= 60:
        st.info("Decent. Some promise, but room to improve. I'm on the fence.")
    elif total_score <= 70:
        st.success("Strong potential. I'm in!")
    else:
        st.success("Well done! This is a compelling pitch. I'm in!")


