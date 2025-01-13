# app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to scrape funding information
def scrape_funding_info(query, location, market, funding_round, min_amount):
    # Example Google search URL (replace with your API or scraping logic)
    search_url = f"https://www.google.com/search?q={query}+{location}+{market}+{funding_round}+funding+${min_amount}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Send HTTP request
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Parse search results
    results = []
    for result in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):  # Adjust based on Google's structure
        title = result.get_text()
        link = result.find_parent('a')['href']
        results.append({'title': title, 'link': link})
    
    return results

# Streamlit App Interface
st.title("Funding Info Search App")
st.sidebar.header("Search Criteria")

# Input fields for search criteria
query = st.sidebar.text_input("Query (e.g., Biotech Funding)")
location = st.sidebar.text_input("Location (Country)")
market = st.sidebar.text_input("Market")
funding_round = st.sidebar.selectbox("Funding Round", ["Seed", "Series A", "Series B", "Series C", "IPO"])
min_amount = st.sidebar.number_input("Minimum Amount ($)", min_value=0)

# Search button
if st.sidebar.button("Search"):
    with st.spinner("Searching..."):
        results = scrape_funding_info(query, location, market, funding_round, min_amount)
        if results:
            for result in results:
                st.write(f"**{result['title']}**")
                st.write(f"[Link]({result['link']})")
        else:
            st.write("No results found.")
