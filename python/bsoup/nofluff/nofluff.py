import requests
from bs4 import BeautifulSoup


class Scraper:
    base_url = 'https://nofluffjobs.com'
    experience = {
        'trainee', 'junior', 'mid', 'senior', 'expert'
    }

    department = {
        'backend',
        'frontend', 'fullstack', 'mobile', 'embedded',
        'testing', 'devops', 'architecture', 'security',
        'game-dev', 'artificial-intelligence', 'data',
        'sys-administrator', 'agile', 'product-management',
        'project-manager', 'business-intelligence', 'ux',
        'support', 'erp', 'other'
        # https://nofluffjobs.com/?page=1&criteria=category%3Dbackend,frontend%20seniority%3Dtrainee,junior,mid,senior,expert
    }

    def __init__(self, *args, **kwargs):

        self.experience_categories = self.get_input_categories('experience')
        self.department_categories = self.get_input_categories('department')

    def get_input_categories(self, category_type):
        available_categories = getattr(self, category_type, set())
        categories = set()
        print(f"Available {category_type} categories: {', '.join(sorted(available_categories))}")
        while True:
            category_input = input(f"Enter a {category_type} category: ").strip().lower()
            if category_input == 'done':
                break
            elif category_input == 'all':
                categories = available_categories.copy()
                break
            elif category_input == 'exclude':
                exclude_input = input(f"Enter categories to exclude (comma-separated): ").strip().lower().split(',')
                categories.update(available_categories - set(exclude_input))
            if category_input in available_categories:
                categories.add(category_input)
            else:
                print(f"Wrong category input, {category_type}.")
        print(categories)
        return categories

    def build_url(self, page=1):
        experience_part = ','.join(self.experience_categories)
        department_part = ','.join(self.department_categories)
        url = f'{self.base_url}/?criteria=category%3D{department_part}%20seniority%3D{experience_part}&page={page}'
        print(url)
        return url

    def scrape_links(self, soup, link_list):
        links = soup.select(
            'body > nfj-root > nfj-layout > nfj-main-content > div > nfj-postings-search > div > div > common-main-loader > nfj-search-results > nfj-postings-list > div.list-container.ng-star-inserted > a.posting-list-item')
        for link in links:
            href = link.get('href')
            full_link = f'{self.base_url}{href}'
            link_list.append(full_link)

    def scrape_all_pages(self, link_list):
        url = self.build_url()
        data = self.get_data(url)
        soup = BeautifulSoup(data, 'html.parser')
        self.scrape_links(soup, link_list)

        sites = soup.select('ul.pagination li')
        sites_length = len(sites)

        if sites_length >= 2:
            for page in range(2, sites_length):
                url = self.build_url(page)
                data = self.get_data(url)
                soup = BeautifulSoup(data, 'html.parser')
                self.scrape_links(soup, link_list)

        return link_list

    def get_data(self, url):
        req = requests.get(url)
        data = req.text
        return data


link_list = []
scraper = Scraper()
all_links = scraper.scrape_all_pages(link_list)

for link in all_links:
    print(link)
