import requests
from bs4 import BeautifulSoup
import json

url = "https://www.technologyreview.com/lists/companies/2017/"
response = requests.get(url)
text = response.text
soup = BeautifulSoup(text, "html.parser")
data = soup.select(".company")

companies = {}

for company in data:
    company_dict = {}
    # Get Ranking, but not adding it to the temprary dictionary
    ranking = company.find("span", class_="company__rank").text
    # Get Name
    pre_name = company.find("h2", class_="company__name").text
    name = pre_name.strip("\n")
    company_dict["Name"] = name
    # Get Link
    pre_link = company.find("a", class_="company-data__details_link")
    pre_link_2 = pre_link["href"]
    link = pre_link_2.replace("/lists/companies/2017/", "")
    # Go to company details
    details_url = url + link
    details_response = requests.get(details_url)
    details_text = details_response.text
    detail_soup = BeautifulSoup(details_text, "html.parser")
    company_stats = detail_soup.select(".company__stats__item")
    # Get Headquarters
    pre_hq = company_stats[5 * (int(ranking) - 1)].text  # hq index = 5 * (ranking - 1)
    pre_hq_2 = pre_hq.replace("\n", "")
    pre_hq_3 = pre_hq_2.replace("Headquarters\t\t\t\t\t\t", "")
    hq = pre_hq_3.replace("\t\t", "")
    company_dict["Headquarters"] = hq
    # Get Industry
    pre_industry = company_stats[5 * (int(ranking) - 1) + 1].text.title() # industry index = hq index + 1
    industry = pre_industry.replace("Industry ", "")
    company_dict["Industry"] = industry
    # Get Valuation
    pre_valuation = company_stats[5 * (int(ranking) - 1) + 4].text.title() # valuation index = hq index + 4
    valuation = pre_valuation.replace("Valuation ", "")
    company_dict["Valuation"] = valuation
    companies[ranking] = company_dict

formatted_companies = json.dumps(companies, indent=2)
print(formatted_companies)
    
    
