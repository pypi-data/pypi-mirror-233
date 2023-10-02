# Top 100 Visited Sites Web Scraper

## Description
This Python script is a simple web scraper that fetches data from a Wikipedia's Top 100 Sites (https://en.wikipedia.org/wiki/List_of_most-visited_websites), specifically an HTML table, and converts it into a list of dictionaries. It also accesses each domain in the list and prints its response code.

I created this script to automate testing of Firewall, Content Filtering and NAT related services. It can be used to test if a domain is accessible or not. 
It can also be used to test if a domain is being redirected to another domain.

Using this script helps me debug whether a rule (code) is working as expected or not. For example, if I have a rule that blocks access to a domain, I can use this script to test if the domain is indeed blocked or not. At the same time, I can get useful Syslogs for each run. 

## Dependencies
- Python 3.6 or higher
- `requests` library
- `BeautifulSoup` from `bs4` library
- `urlparse` from `urllib.parse` library

## Functions
- `is_valid_url(url: str) -> bool`: Checks if the URL is valid.
- `html_table_to_list(url: str, num_columns: int) -> list`: Converts an HTML table into a list of dictionaries.
- `access_domains(top_100: list) -> None`: Accesses each domain in a list and prints its response code.

## Usage
1. Install the required dependencies.
2. Run the script with Python 3.6 or higher.
3. The script will fetch data from the specified URL, convert the HTML table into a list of dictionaries, and print the response code for each domain.

Please note that the URL of the webpage containing the table and the number of columns in the table are parameters for the `html_table_to_list` function. The default number of columns is set to 5.

The `access_domains` function takes in a list of dictionaries representing a table of domains and prints their response codes.

## Example
```python
# Use the function
top_100_reference = "https://en.wikipedia.org/wiki/List_of_most-visited_websites"  # Replace with your URL
top_100_list = html_table_to_list(top_100_reference)
access_domains(top_100_list)
```
In this example, the script fetches data from a Wikipedia page that lists the most visited websites, converts the HTML table into a list of dictionaries, and prints the response code for each domain.

## Disclaimer
Please use this script responsibly and ensure that you are allowed to scrape the websites you choose to scrape. Some websites may prohibit scraping in their terms of service. Always respect others' intellectual property rights.