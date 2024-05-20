import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import time

data = pd.DataFrame()

max_requests_per_minute = 20

time_interval = timedelta(minutes=1) /(max_requests_per_minute - 1)

start_time = datetime.now()

for year in range(1977, datetime.today().year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + ".html"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find(
        lambda tag: tag.name == "table"
        and tag.has_attr("id")
        and tag["id"] == "advanced-team"
    )

    table_head = table.find("thead").findAll("tr")[1]
    table_body = table.find("tbody").findAll("tr")

    column_headers = [th.getText() for th in table_head]
    filtered_column_headers = list(filter(lambda t: t != " ", column_headers))[1:]

  # actual data from the table
    team_data = [
        [td.getText() for td in table_body[i].findAll("td")]
        for i in range(len(table_body))
    ]

  # integration with the master dataframe
    df = pd.DataFrame(team_data, columns=filtered_column_headers)
    df["Year"] = year
    data = pd.concat([data, df])
    print(year)

    elapsed_time = datetime.now() - start_time
    time_to_wait = time_interval - elapsed_time

    if time_to_wait.total_seconds() > 0:
        time.sleep(time_to_wait.total_seconds())

    start_time = datetime.now()

data.to_csv('/Users/patrickrunciman/Desktop/pythonProjects/Data/teams.csv')

