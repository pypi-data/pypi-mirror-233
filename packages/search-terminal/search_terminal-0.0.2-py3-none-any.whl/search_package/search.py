import argparse
import requests
import html2text

def main():
    parser = argparse.ArgumentParser(description="Search the web from the command line.")
    parser.add_argument("query", type=str, help="Search query")
    args = parser.parse_args()

    try:
        search_results = google_search(args.query)
        if search_results:
            print(search_results)
    except Exception as e:
        print(e)

def google_search(query):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    headers = {"User-Agent": user_agent}
    
    search_url = f"https://www.google.com/search?q={query}"
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        
        html_content = response.text
        plain_text = html2text.html2text(html_content)
        
        return plain_text
    except requests.exceptions.RequestException as e:
        raise Exception("Error: Unable to fetch search results.") from e

if __name__ == "__main__":
    main()
