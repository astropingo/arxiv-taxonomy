import json
import requests
from bs4 import BeautifulSoup

# Extração de lista taxonômica das publicações no site arxiv.org
# Data: 24-06-2021

arxiv_taxonomy = {}

# Request da página do Arxiv
url = r"https://arxiv.org/category_taxonomy"
taxonomy_html = requests.get(url).text
soup = BeautifulSoup(taxonomy_html, 'html.parser')

# Extraíndo os grupos (h2) e a lista de categorias por grupo ([div class="accordion-body"])
group_names = soup.find_all("h2", {"class":"accordion-head"})
category_names = soup.find_all("div", {"class":"accordion-body"})
groups = zip(group_names, category_names)

# Adicionando cada dado no dicionário arxiv_taxonomy com o seguinte formato:
for group in groups:
    group_name = group[0].text
    for h4, p in zip(group[1].find_all("h4"), group[1].find_all("p")):
        cat_name = h4.find("span")
        cat_name.extract()
        cat_id = h4.text
        cat_description = p.text
        arxiv_taxonomy[cat_id] = {
                "group_name":group_name,
                "category_name":cat_name.text[1:-1],
                "description":cat_description
            }

# Salvasndo o arquivo em formato json
json_file = "../json/arxiv_taxonomy.json"
with open(json_file, "w") as outfile:
    json.dump(arxiv_taxonomy, outfile, indent=2)