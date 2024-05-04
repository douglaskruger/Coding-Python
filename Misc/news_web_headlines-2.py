import requests
from bs4 import BeautifulSoup

def get_cnn_headlines():
    """Retrieves and prints headlines from CNN's homepage."""

    url = "https://www.cnn.com"

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        # CNN frequently updates their layout - Find elements reliably
        headlines = soup.find_all(class_="cd__headline")

        if headlines:
            for headline in headlines:
                link_container = headline.find('a')
                if link_container:
                    print(link_container.text.strip())
        else:
            print("Headlines not found. The website's structure might have changed.")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching news: {e}")

if __name__ == "__main__":
    get_cnn_headlines()