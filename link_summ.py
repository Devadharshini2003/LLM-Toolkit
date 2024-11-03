import streamlit as st
from transformers import pipeline
from newspaper import Article
import validators


summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

def main():
    st.title("URL Summarization Tool")

    # User input for URL
    url = st.text_input("Enter the URL of the article you want to summarize:")

    # Check if URL is valid and process it
    if url:
        if validators.url(url):
            with st.spinner("Fetching and summarizing the article..."):
                try:
                    # Download and parse the article
                    article = Article(url)
                    article.download()
                    article.parse()
                    article_text = article.text

                    # Summarize the article text
                    summary = summarizer(article_text, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]

                    # Display results
                    st.subheader("Article Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a valid URL.")

    # Instructions in the sidebar
    st.sidebar.markdown("### Instructions")
    st.sidebar.markdown("1. Enter the URL of an article.")
    st.sidebar.markdown("2. The tool will fetch, analyze, and summarize the content.")

if __name__ == "__main__":
    main()
