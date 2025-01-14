import re
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

# Documentation Links
external_links = {
    "Segment": "https://segment.com/docs/?ref=nav",
    "mParticle": "https://docs.mparticle.com/",
    "Lytics": "https://docs.lytics.com/",
    "Zeotap": "https://docs.zeotap.com/home/en-us/"
}

# Helper Functions
def fetch_documentation_content(url: str) -> str:
    """
    Fetch and extract content from a given documentation URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)  # Improved text extraction
    except requests.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as e:
        return f"Could not retrieve documentation from {url}. Error: {str(e)}"

def search_documentation(platform: str, query: str) -> str:
    """
    Search the provided documentation for a given query.
    """
    documentation_url = external_links.get(platform, None)
    if not documentation_url:
        return f"No documentation link available for {platform}."

    content = fetch_documentation_content(documentation_url)
    if re.search(re.escape(query.lower()), content.lower()):  # Improved search with regex
        return f"The documentation for {platform} contains relevant information. Visit: {documentation_url}"
    return f"No specific instructions found in the documentation for {platform}. Please visit: {documentation_url}"

def chatbot_response(query: str) -> str:
    """
    Generate a chatbot response based on user query.
    """
    platforms = ["Segment", "mParticle", "Lytics", "Zeotap"]
    query = query.lower()  # Normalize query to lowercase
    response = ""

    for platform in platforms:
        if platform.lower() in query:
            # Check for specific "how-to" keywords
            if any(phrase in query for phrase in ["how to", "how do", "how can"]):
                if "setup" in query and "source" in query:
                    response = search_documentation(platform, "setup source")
                elif "integrate" in query:
                    response = search_documentation(platform, "integrate")
                elif "build" in query and "audience" in query:
                    response = search_documentation(platform, "build audience")
                elif "create" in query and "profile" in query:
                    response = search_documentation(platform, "create profile")
                else:
                    response = f"Could you please specify the task you need help with regarding {platform}?"
                break

    if not response:
        response = ("I'm sorry, I couldn't identify a specific how-to task or platform in your query. "
                    "Please specify the platform (Segment, mParticle, Lytics, or Zeotap) and the task you need help with. "
                    "For more information, you can visit the respective documentation links:")
        response += "\n" + "\n".join([f"- {platform}: {link}" for platform, link in external_links.items()])

    return response

# Example Usage
if __name__ == "__main__":
    print("Welcome to the CDP Support Chatbot!")
    while True:
        user_query = input("Ask your question: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Thank you for using the CDP Support Chatbot. Goodbye!")
            break
        reply = chatbot_response(user_query)
        print(f"Chatbot: {reply}")