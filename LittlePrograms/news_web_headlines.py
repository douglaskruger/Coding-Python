import requests
from bs4 import BeautifulSoup

def get_cnn_headlines():
    """Retrieves and prints headlines from CNN's homepage."""

    url = "https://www.theverge.com/tech"

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the relevant section containing the headlines
        headlines_section = soup.find('div', class_='zn-zone-only')

        if headlines_section:
            headlines = headlines_section.find_all('h3', class_='cd__headline')

            if headlines:
                print("Top Headlines from CNN:")
                for headline in headlines:
                    link = headline.find('a')
                    print('-', link.text.strip())
                    print(link.get('href'))  # Print the full URL of the news article
            else:
                print("Headlines not found within the expected structure.")

        else:
            print("Could not find the headlines section on CNN.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching news: {e}")

if __name__ == "__main__":
    get_cnn_headlines()