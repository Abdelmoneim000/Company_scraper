#!./venv/bin/python3

import requests
from bs4 import BeautifulSoup
import csv
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def retry_request(url, max_retries=5, initial_wait=60):
    attempt = 0
    wait_time = initial_wait

    while attempt < max_retries:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response
        except requests.RequestException as e:
            print(
                f"Request failed: {e}. Attempt {attempt + 1} of {max_retries}. Waiting for {wait_time} seconds.")
            time.sleep(wait_time)
            attempt += 1
            wait_time *= 2  # Exponential backoff

    print(f"Failed to retrieve {url} after {max_retries} attempts.")
    return None


def get_total_pages():
    url = 'https://vc-mapping.gilion.com/explore'
    response = retry_request(url)
    if not response:
        return 0

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        page_count_text = soup.find(
            'div', class_='w-page-count page-count').text.strip()
        total_pages = int(page_count_text.split('/')[-1].replace(' ', ''))
        return total_pages
    except Exception as e:
        print(f"An error occurred while parsing total pages: {e}")
        return 0


def fetch_Vc_firms(page):
    url = f'https://vc-mapping.gilion.com/explore?5656daaa_page={page}'
    response = retry_request(url)
    response.encoding = 'utf-8'
    if not response:
        return []

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = []
        firms = soup.find_all('div', class_='info-card card-org')
        for firm in firms:
            try:
                firm_name = firm.find(
                    'div', class_='investor-name').text.strip()
                firm_details = firm.find(
                    'a', class_='card-button w-button').get('href')
                cards.append(
                    (firm_name, f'https://vc-mapping.gilion.com{firm_details}'))
            except AttributeError as e:
                print(f"Error extracting data from firm card: {e}")
        return cards
    except Exception as e:
        print(f"An error occurred while parsing data for page {page}: {e}")
        return []


def fetch_firm_details(firm_url):
    response = retry_request(firm_url)
    response.encoding = 'utf-8'
    if not response:
        return {}

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        numbers = [flexbox.find('div', class_='numbers-on-cards').get_text(strip=True)
                   for flexbox in soup.find('div', class_='tag-split no-pad').find_all('div', class_='flexbox-vertical')]
        about = soup.find(
            'div', class_='vc-info_container is--first extra-text').find_next('p').text.strip()
        portfolio_companies = soup.find(
            'div', class_='agency-info').find('div', class_='numbers-on-cards-left').text.strip()
        tags = [tag.find_all('div', class_='tag-text')
                for tag in soup.find_all('div', class_='w-dyn-list')]

        founded = numbers[0] if len(numbers) > 0 else ''
        investments = numbers[1] if len(numbers) > 1 else ''
        exits = numbers[2] if len(numbers) > 2 else ''
        fund_type = ', '.join(i.get_text(strip=True)
                              for i in tags[0]) if len(tags) > 0 else ''
        investment_stage = ', '.join(i.get_text(strip=True)
                                     for i in tags[1]) if len(tags) > 1 else ''
        investment_focus = ', '.join(i.get_text(strip=True)
                                     for i in tags[2]) if len(tags) > 2 else ''
        hq_country = ', '.join(i.get_text(strip=True)
                               for i in tags[3]) if len(tags) > 3 else ''
        city = ', '.join(i.get_text(strip=True)
                         for i in tags[4]) if len(tags) > 4 else ''

        details = {
            'Founded': founded,
            'Investments': investments,
            'Exits': exits,
            'About': about,
            'Portfolio Companies': portfolio_companies,
            'Fund Type': fund_type,
            'Investment Stage': investment_stage,
            'Investment Focus': investment_focus,
            'HQ Country': hq_country,
            'City': city
        }
        return details
    except Exception as e:
        print(
            f"An error occurred while parsing firm details from {firm_url}: {e}")
        return {}


def save_to_csv(firms_details, filename='vc_firms_details.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Firm Name', 'URL', 'Founded', 'Investments', 'Exits', 'About', 'Portfolio Companies',
                        'Fund Type', 'Investment Stage', 'Investment Focus', 'HQ Country', 'City'])

        for firm_name, firm_url, details in firms_details:
            writer.writerow([
                firm_name,
                firm_url,
                details.get('Founded', ''),
                details.get('Investments', ''),
                details.get('Exits', ''),
                details.get('About', ''),
                details.get('Portfolio Companies', ''),
                details.get('Fund Type', ''),
                details.get('Investment Stage', ''),
                details.get('Investment Focus', ''),
                details.get('HQ Country', ''),
                details.get('City', '')
            ])
    print(f"Data has been written to {filename}")


def main():
    total_pages = get_total_pages()
    if total_pages == 0:
        print("No pages to fetch. Exiting.")
        return

    all_firms_details = []

    for page in range(1, total_pages + 1):
        print(f"Fetching page {page} of {total_pages}")
        firms = fetch_Vc_firms(page)

        for firm_name, firm_url in firms:
            print(f"Fetching details for {firm_name}")
            details = fetch_firm_details(firm_url)
            all_firms_details.append((firm_name, firm_url, details))

        print("Waiting for 10 seconds...")
        time.sleep(10)

    save_to_csv(all_firms_details)


if __name__ == '__main__':
    main()
