import streamlit as st
import matplotlib.pyplot as plt
from stock_data import fetch_stock_data
from valuation import calculate_intrinsic_value
from financial_news import summarize_news
from rag_pipeline import build_rag
from crew import finance_crew
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="AI Investment Research Assistant")

st.title("AI Investment Research Assistant")


ticker = st.text_input("Enter Stock Ticker", "AAPL")


if st.button("Analyze Stock"):

    hist, financials = fetch_stock_data(ticker)

    st.subheader("Company Information")
    st.write(financials)

    eps = financials.get("eps", 0)

    intrinsic_value = calculate_intrinsic_value(eps)

    st.subheader("Intrinsic Value")
    st.write(intrinsic_value)

    st.subheader("Stock Price Chart")

    fig, ax = plt.subplots()
    hist["Close"].plot(ax=ax)

    st.pyplot(fig)

    sample_news = "The company reported strong quarterly earnings and revenue growth."

    news_summary = summarize_news(sample_news)

    st.subheader("AI News Analysis")
    st.write(news_summary)

    st.subheader("Running AI Finance Agents")

    result = finance_crew.kickoff(
    inputs={
        "ticker": ticker,
        "eps": financials.get("eps"),
        "pe_ratio": financials.get("peRatio"),
        "current_price": financials.get("currentPrice")
    }
    )
    

    st.write(result)


uploaded_file = st.file_uploader(
    "Upload Annual Report PDF",
    type=["pdf"]
)


if uploaded_file:

    with open(f"data/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.read())

    qa_chain = build_rag(f"data/{uploaded_file.name}")

    question = st.text_input("Ask Questions About the Report")

    if question:

        answer = qa_chain.run(question)

        st.subheader("AI Answer")
        st.write(answer)