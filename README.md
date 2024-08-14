# Company Scraper

This is a Python script designed to scrape information about venture capital firms from the VC Mapping website and save the details to a CSV file.

## Features

- **Retry Mechanism**: The script includes a retry mechanism to handle network errors gracefully.
- **BeautifulSoup for Web Scraping**: The script uses BeautifulSoup to parse HTML and extract relevant data.
- **CSV Export**: Extracted data is saved in a CSV file for further analysis or processing.

## Requirements

- Python 3.x
- Virtual Environment (optional, but recommended)

## Setup and Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Abdelmoneim000/Company_scraper.git
cd company-scraper
```

## Step 2: Set Up the Virtual Environment
It's recommended to use a virtual environment to manage dependencies.


```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Step 3: Install Dependencies
Install the required Python packages:

```bash
pip install requests beautifulsoup4
```

> [!NOTE]
> On replit, you will need to pass the flag `--no-user` to install dependencies.

## Running the Script
Once the setup is complete, you can run the script:

```bash
./scrapping.py
```
Or you can run it directly with Python:

```bash
python3 scrapping.py
```

### Output
The script will scrape data from the website and save the details in a CSV file named `vc_firms_details.csv` in the current directory.

## Understanding the Code

### Key Functions

  1. `retry_request(url, max_retries=5, initial_wait=60)`:
     - Handles network requests with a retry mechanism.
     - Waits for a specified time before retrying failed requests.
  2. `get_total_pages()`:
     - Determines the total number of pages to scrape by parsing the HTML content.
  3. `fetch_Vc_firms(page)`:
     - Scrapes venture capital firm data from a specific page.
  4. `fetch_firm_details(firm_url)`:
     - Scrapes detailed information about a specific firm using the firm's URL.
  5. `save_to_csv(firms_details, filename='vc_firms_details.csv')`:
     - Saves the scraped data into a CSV file.

### Flow of Execution

1. *Total Pages*: The script starts by determining the total number of pages to scrape.
2. *Scraping Firms*: It then iterates through each page, scraping the list of firms.
3. *Fetching Details*: For each firm, the script fetches detailed information.
4. *Saving Data*: Finally, all the collected data is saved in a CSV file.

## Customization

- *Change the Target URL*: Modify the URL in the `get_total_pages()` and `fetch_Vc_firms(page)` functions to scrape data from a different source.
- *Adjust Retry Mechanism*: You can customize the max_retries and initial_wait parameters in the retry_request() function.

