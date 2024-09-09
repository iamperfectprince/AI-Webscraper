import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
import validators  # To validate URLs

# Streamlit UI
st.title("AI Web Scraper")
url = st.text_input("Enter Website URL")

# Validate URL
if url and not validators.url(url):
    st.error("Please enter a valid URL.")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url and validators.url(url):
        with st.spinner("Scraping the website..."):
            # Scrape the website
            dom_content = scrape_website(url)
            if dom_content:
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content

                # Display the DOM content in an expandable text box
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
                st.success("Website content scraped successfully!")
            else:
                st.error("Failed to scrape the website. Please check the URL and try again.")
    else:
        st.error("Please enter a valid URL.")

# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            with st.spinner("Parsing the content..."):
                # Parse the content with Ollama
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_ollama(dom_chunks, parse_description)
                st.write(parsed_result)
            st.success("Content parsed successfully!")
        else:
            st.warning("Please provide a description of what you want to parse.")
