import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from re import sub
import string
from urllib.request import urlopen
import pandas as pd
import numpy as np
import requests

if __name__ == '__main__':

    url = 'https://www.basketball-reference.com/awards/mvp.html'

    table_html = str((BeautifulSoup(urlopen(url), 'html.parser').findAll('table', id = 'mvp_NBA')[0]))

    df_MVP = pd.read_html(table_html)[0]

    df_MVP.columns = df_MVP.columns.droplevel(0)
    df1_MVP = df_MVP[['Player', 'Age']]
    df2_MVP = df_MVP[['Player', 'PTS', 'TRB', 'AST']]

    MVP_age = (df1_MVP['Age'].sum())/66
    print('Average MVP age:', round(MVP_age, 2))

    MVP_ppg = (df2_MVP['PTS'].sum())/66
    print('Average MVP PPG:', round(MVP_ppg, 2))

    MVP_ast = (df2_MVP['AST'].sum())/66
    print('Average MVP APG:', round(MVP_ast, 2))

    MVP_RPG = (df2_MVP['TRB'].sum())/66
    print('Average MVP RPG:', round(MVP_RPG, 2))

    oldest = df1_MVP['Age'].describe()
    print('Oldest MVP age:', oldest)

    url = 'https://www.basketball-reference.com/contracts/LAC.html'

    table_html = str((BeautifulSoup(urlopen(url), 'html.parser').findAll('table', id = 'contracts')[0]))

    df_salary = pd.read_html(table_html)[0]
    df_salary.columns = df_salary.columns.droplevel(0)

    df1_salary = df_salary[['Player', 'Age', '2022-23', 'Guaranteed']]
    print(df1_salary)

    df1_salary['2022-23'] = df1_salary['2022-23'].apply(lambda x: x.replace('$', '').replace(',', '')
                                    if isinstance(x, str) else x).astype(float)

    df1_salary['Guaranteed'] = df1_salary['Guaranteed'].apply(lambda x: x.replace('$', '').replace(',', '')
                                    if isinstance(x, str) else x).astype(float)

    average_salary = (df1_salary.at[len(df1_salary) -1, '2022-23'])/(len(df1_salary)-1)
    print(round(average_salary, 2))

    average_age = (df1_salary.at[len(df1_salary) - 1, 'Age'])/(len(df1_salary) - 1)
    print(round(average_age, 2))

    url_curry = 'https://www.basketball-reference.com/players/c/curryst01.html'

    table_html_curry = str((BeautifulSoup(urlopen(url_curry), 'html.parser').findAll('table', id = 'per_game')[0]))

    url_miller = 'https://www.basketball-reference.com/players/m/millere01.html'

    table_html_miller = str((BeautifulSoup(urlopen(url_miller), 'html.parser').findAll('table', id = 'per_game')[0]))

    df_curry = pd.read_html(table_html_curry)[0]

    df1_curry = df_curry.iloc[0:17, [0, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]]

    df_miller = pd.read_html(table_html_miller)[0]

    df1_miller = df_miller.iloc[0:17, [0, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]]

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(x = df1_curry['3PA'], y = df1_curry['3P'], marker = 'o', label = 'curry')
    ax1.scatter(x = df1_miller['3PA'], y = df1_miller['3P'], marker = 'x', label = 'miller')
    plt.legend()
    plt.show()

    data = pd.DataFrame()

    for year in range(1977, 2021):
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        table_E = soup.find(
            lambda tag: tag.name == "table"
                        and tag.has_attr("id")
                        and tag["id"] == "confs_standings_E"
        )

        table_E_head = table_E.find("thead").findAll("tr")[1]
        table_E_body = table_E.find("tbody").findAll("tr")

        # extracts data from table head
        column_headers = [th.getText() for th in table_E_head]
        filtered_column_headers = list(filter(lambda t: t != " ", column_headers))[1:]

        # actual data from the table
        team_data = [
            [td.getText() for td in table_E_body[i].findAll("td")]
            for i in range(len(table_E_body))
        ]

        df = pd.DataFrame(team_data, columns=filtered_column_headers)
        df["Year"] = year
        data = pd.concat([data, df])
        print(year)

    data.to_csv('../data/teams.csv')

    for year in range(1977, 2021):
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        table_E = soup.find(
            lambda tag: tag.name == "table"
                        and tag.has_attr("id")
                        and tag["id"] == "confs_standings_E")

        table_W = soup.find(
            lambda tag: tag.name == "table"
                        and tag.has_attr("id")
                        and tag["id"] == "confs_standings_W")