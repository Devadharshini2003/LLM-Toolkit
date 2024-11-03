import streamlit as st
from transformers import pipeline
from newspaper import Article
import validators
from bs4 import BeautifulSoup
import requests

# Initialize summarization pipeline
try:
    summarizer = pipeline("summarization")
except Exception as e:
    st.error("Failed to load the summarization model. Please check the environment.")
    st.stop()

def summarize_article(url):
    """Summarizes a single article using `newspaper3k`."""
    if validators.url(url):
        with st.spinner("Fetching and summarizing the article..."):
            article = Article(url)
            article.download()
            article.parse()
            article_text = article.text

            # Summarize the article text
            summary = summarizer(article_text, max_length=500, min_length=50, do_sample=False)[0]["summary_text"]

            # Display results
            st.subheader("Article Summary:")
            st.write(summary)
    else:
        st.error("Please enter a valid URL.")

def fetch_and_summarize_structured(url):
    """Fetches and summarizes structured content using BeautifulSoup."""
    if validators.url(url):
        with st.spinner("Fetching and summarizing the page..."):
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")

                summaries = []
                for section in soup.find_all(["h2", "h3", "p"]):
                    content = section.get_text().strip()
                    if content and len(content) > 50:  # Generate summary only for meaningful content
                        summary = summarizer(content, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
                        summaries.append(f"#### {section.get_text()}\n\n{summary}\n\n")

                # Display compiled summary
                st.subheader("Page Summary:")
                st.write("\n".join(summaries))

            except Exception as e:
                st.error(f"Error processing the URL: {e}")
    else:
        st.error("Please enter a valid URL.")

def main():
    # Set up Streamlit app configuration
    st.title("Multi-Function URL Summarization Tool")
    st.sidebar.markdown("### Choose a Summarization Mode")
    mode = st.sidebar.selectbox("Select Mode", ("Single Article Summarizer", "Structured Page Summarizer"))

    url = st.text_input("Enter the URL of the page you want to summarize:")

    if url:
        if mode == "Single Article Summarizer":
            summarize_article(url)
        elif mode == "Structured Page Summarizer":
            fetch_and_summarize_structured(url)

    # Instructions
    st.sidebar.markdown("### Instructions")
    st.sidebar.markdown("1. Enter the URL of an article or webpage.")
    st.sidebar.markdown("2. Select the summarization mode.")
    st.sidebar.markdown("3. Wait for the tool to fetch and summarize the content.")

if __name__ == "__main__":
    main()
