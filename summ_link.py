'''import streamlit as st
from transformers import pipeline
from newspaper import Article
import validators

# Initialize summarization pipeline
summarizer = pipeline("summarization")

# Set up Streamlit app
st.set_page_config(page_title="URL Summarization")
st.title("URL Summarization Tool")

# User input for URL
url = st.text_input("Enter the URL of the article you want to summarize:")

# Check if URL is valid and process it
if url:
    if validators.url(url):
        with st.spinner("Fetching and summarizing the article..."):
            # Download and parse the article
            article = Article(url)
            article.download()
            article.parse()
            article_text = article.text

            # Summarize the article text
            summary = summarizer(article_text, max_length=1500, min_length=150, do_sample=False)[0]["summary_text"]

            # Display results
            st.subheader("Article Summary:")
            st.write(summary)
    else:
        st.error("Please enter a valid URL.")

# Instructions
st.sidebar.markdown("### Instructions")
st.sidebar.markdown("1. Enter the URL of an article or webpage.")
st.sidebar.markdown("2. Wait for the tool to fetch, analyze, and summarize the content.")
'''


import streamlit as st
from transformers import pipeline
from newspaper import Article
import validators

# Initialize summarization pipeline
summarizer = pipeline("summarization")

def main():
    # Set up Streamlit app
    #st.set_page_config(page_title="URL Summarization")
    st.title("URL Summarization Tool")

    # User input for URL
    url = st.text_input("Enter the URL of the article you want to summarize:")

    # Check if URL is valid and process it
    if url:
        if validators.url(url):
            with st.spinner("Fetching and summarizing the article..."):
                # Download and parse the article
                article = Article(url)
                article.download()
                article.parse()
                article_text = article.text

                # Summarize the article text
                summary = summarizer(article_text, max_length=1500, min_length=150, do_sample=False)[0]["summary_text"]

                # Display results
                st.subheader("Article Summary:")
                st.write(summary)
        else:
            st.error("Please enter a valid URL.")

    # Instructions
    st.sidebar.markdown("### Instructions")
    st.sidebar.markdown("1. Enter the URL of an article or webpage.")
    st.sidebar.markdown("2. Wait for the tool to fetch, analyze, and summarize the content.")

if __name__ == "__main__":
    main()





'''

import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Initialize summarization pipeline
summarizer = pipeline("summarization")

# Set up Streamlit app
st.set_page_config(page_title="Structured URL Summarization Tool")
st.title("Structured URL Summarization Tool")

# User input for URL
url = st.text_input("Enter the URL of the page you want to summarize:")

def fetch_and_summarize(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    summaries = []
    st.write("### Raw Content Extracted (for troubleshooting):")
    for section in soup.find_all(["h2", "h3", "p"]):
        # Display raw content for troubleshooting
        st.write(section.get_text())
        
        # Summarize content in paragraphs under headings
        content = section.get_text().strip()
        
        if content:
            # Generate summary only for long enough content
            if len(content) > 50:
                summary = summarizer(content, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
                summaries.append(f"#### {section.get_text()}\n{summary}")
    
    # Return compiled summary
    return "\n\n".join(summaries)

# Process and display summary
if url:
    try:
        with st.spinner("Fetching and summarizing the page..."):
            summary_text = fetch_and_summarize(url)
            st.subheader("Page Summary:")
            st.write(summary_text)
    except Exception as e:
        st.error(f"Error processing the URL: {e}")

# Instructions
st.sidebar.markdown("### Instructions")
st.sidebar.markdown("1. Enter the URL of a structured page with multiple sections.")
st.sidebar.markdown("2. The tool will extract, summarize, and organize information based on each section.")

'''