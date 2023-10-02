import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def is_valid_url(url):
    """
    Check if the url is valid.

    Parameters:
    url (str): The url to be checked.

    Returns:
    bool: True if valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def html_table_to_list(url, num_columns=5):
    """
    Convert an HTML table to a list of dictionaries.

    Parameters:
    url (str): The url of the webpage containing the table.
    num_columns (int): The number of columns in the table.

    Returns:
    list: A list of dictionaries representing the table.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first table on the page
    table = soup.find_all('table')[0]

    # Get the headers of the table
    headers = [header.text.replace(' ', '').strip() for header in table.find_all('th')]

    # Get all the rows of the table
    rows = table.find_all('tr')

    # List to hold all data for JSON
    data_list = []

    # Go through each row
    for row in rows:
        data_dict = {}
        columns = row.find_all('td')
        # Only process rows with exactly num_columns columns
        if len(columns) == num_columns:
            # For each row, get each column
            for i, column in enumerate(columns):
                # Strip all whitespace, carriage return and line feed from each column
                column_text = "".join(column.text.split())
                # Prefix each value in the second column with "https://"
                if i == 1:
                    if column_text is None:
                        break
                    column_text = 'https://' + column_text
                    if not is_valid_url(column_text):
                        break
                data_dict[headers[i]] = column_text
            else:  # Only executed if the loop didn't break
                data_list.append(data_dict)

    return data_list


def access_domains(top_100):
    """
    Access each domain in a list and print its response code.

    Parameters:
    top_100 (list): A list of dictionaries representing a table of domains.

    Returns:
    None
    """

    for entry in top_100:
        try:
            url = entry.get('Domainname')
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            print(f"domain: {url} connection error")
        except requests.exceptions.MissingSchema:
            print(f"url schema error: {url}")
        else:
            print(f"domain: {url} response code: {response.status_code}")


# Use the function
top_100_reference = "https://en.wikipedia.org/wiki/List_of_most-visited_websites"  # Replace with your URL
top_100_list = html_table_to_list(top_100_reference)
access_domains(top_100_list)
