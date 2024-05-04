import requests
from bs4 import BeautifulSoup

def read_website_html(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Print the HTML content
        print(soup.prettify())
    else:
        print(f"Failed to retrieve HTML. Status code: {response.status_code}")

# Replace 'https://www.example.com' with the URL of the website you want to read
read_website_html('https://www.example.com')