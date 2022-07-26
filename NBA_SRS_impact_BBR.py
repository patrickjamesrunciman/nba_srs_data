import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from re import sub
import string
from urllib.request import urlopen
import pandas as pd
import numpy as np
import requests

if __name__ == '__main__':
    data_E = pd.DataFrame()

    year = 2021

    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    table_E = soup.find(
        lambda tag: tag.name == "table"
                    and tag.has_attr("id")
                    and tag["id"] == "confs_standings_E"
    )

    table_E_head = table_E.find("thead").findAll("tr")
    table_E_body = table_E.find("tbody").findAll("tr")

    column_E_headers = []
    for th in table_E_head:
        i = 0
        column_E_headers[i] = th.getext(
            i=i + 1

        team_E_data = [
            [td.getText() for td in table_E_body[i].findAll("td")]
            for i in range(len(table_E_body))
        ]

        df_E = pd.DataFrame(team_E_data, columns=filtered_column_E_headers)
        data_E = pd.concat([data_E, df_E])

        column_E_headers