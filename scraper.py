import requests
from bs4 import BeautifulSoup
import json

response = requests.get("https://www.technologyreview.com/lists/companies/2017/intro/")
text = response.text
soup = BeautifulSoup(text, "html.parser")
data = soup.select(".company")

companies = {}

for company in data:
    company_dict = {}
    # Get Ranking
    pre_ranking = company.find("p", class_="company__rank").text
    if pre_ranking == "1":
        ranking = "1st"
    elif pre_ranking == "2":
        ranking = "2nd"
    elif pre_ranking == "3":
        ranking = "3rd"
    else:
        ranking = pre_ranking + "th"
    # Get Name
    name = company.find("h1", class_="company__title").text
    # Get Stats
    stats = company.select(".company__stats__item")
    # Get Headquarters
    pre_hq = stats[0].text.title()
    pre_hq_2 = pre_hq.replace("\n", "")
    pre_hq_3 = pre_hq_2.replace("Headquarters", "")
    hq = pre_hq_3.replace("\t", "")
    # Get Industry
    pre_industry = stats[1].text.title()
    industry = pre_industry.replace("Industry ", "")
    #Get Status
    pre_status = stats[2].text.title()
    status = pre_status.replace("Status ", "")
    # Get Years On the List
    pre_years = stats[3].find_all("a")
    years = [int(pre_year.text) for pre_year in pre_years]
    # Get Valuation (In Billions)
    pre_valuation = stats[4].text.title()
    pre_valuation_2 = pre_valuation.replace("Valuation $", "")
    try:
        valuation = float(pre_valuation_2.replace(" Billion", ""))
    except ValueError:
        valuation = None
    # Store Company Data
    company_dict["Name"] = name
    company_dict["Headquarters"] = hq
    company_dict["Industry"] = industry
    company_dict["Status"] = status
    company_dict["Years On The List"] = years
    company_dict["Valuation (In Billions)"] = valuation
    # Store Company Data in "Companies" Dictionary
    companies[ranking] = company_dict

formatted_companies = json.dumps(companies, indent=4)
print(formatted_companies)
    
    
