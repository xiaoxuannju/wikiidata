import requests
import  pandas as pd
from bs4 import BeautifulSoup
import re
from bokeh.io import show
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.plotting import figure
import ssl
from bokeh.models import HoverTool
import urllib  # for extracting image
from urllib import request
from pandas.core.frame import DataFrame
import pandas_bokeh
from bokeh.models import HoverTool, ColumnDataSource



def president_info(page_url,name):
    """
    :param page_url:
    :return:
    """
    # enter the page
    president_page = requests.get(page_url)
    # print(president_page.status_code)
    html = BeautifulSoup(president_page.text, "html.parser")  # remove:from_encoding="utf-8"

    # extract info: image(url), start time/end time, series ordinal
    image = html.find("div", id="P18")
    president_image = image.find("img")
    # print(president_image['src'])
    image_url = "https:"+president_image['src']
    # print(image_url)
    # urllib.request.urlretrieve("https:"+president_image['src'],"president.jpg")   # get the image of president

    position_held_html = html.find("div",class_="wikibase-snakview wikibase-snakview-6496d8678e3425e78f15c6e9e14c68ceedb9cc55")
    president_of_the_us_html = position_held_html.parent.parent

    info_list = ["start time","series ordinal","replaces","end time","image"]
    get_list = []
    for text in president_of_the_us_html.stripped_strings:  # remove "\n"
        get_list.append(text)

    info_value = []
    for temp in info_list:
        if temp in get_list:
            p = get_list.index(temp)
            info_value.append(get_list[p+1])

    if len(info_value) < len(info_list)-1:
        info_value.append("present")

    info_value.append(image_url)
    list = {"Info":info_list, "Value":info_value}
    data = pd.DataFrame(list)
    data = data.append([{'Info': "president_name",'Value':name}], ignore_index=True)

    # print(data)
    return data


def former_president_url(page_url,dataframe):
    """
    :param page_url:
    :param dataframe:
    :return:
    """
    president_page = requests.get(page_url)
    # print(president_page.status_code)
    html = BeautifulSoup(president_page.text, "html.parser")

    # find the link of the former president
    president_replaces_from = dataframe.loc[dataframe['Info'] == 'replaces','Value']
    replace_html = html.find("a",text=president_replaces_from)
    # print(replace_html['href'])
    url = "https://www.wikidata.org" + replace_html['href']
    name = replace_html.text

    return url, name


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context

    # Q11696: President of the United States
    # open the webpage:https://www.wikidata.org/wiki/Q11696
    url = "https://www.wikidata.org/wiki/Q11696"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    page = requests.get(url, headers=headers)
    # print(page.status_code)
    soup = BeautifulSoup(page.text, "html.parser")
    tag = soup.find("div", class_="wikibase-snakview wikibase-snakview-9f52e066ced9ef6e472d3478fb4ef717b141aea6")   # find the tag of P18 image
    tag2 = tag.find('a', href=re.compile("/wiki/Q"))  # find the href of the Q6279
    link = "https://www.wikidata.org" + tag2['href']
    president_name = tag2.text
    data = president_info(link,president_name)
    former_url, former_president_name = former_president_url(link,data)
    # print(former_url)

    i = 0
    while i < 5:
        data1 = president_info(former_url,former_president_name)
        # print(data1)
        former_url,former_president_name = former_president_url(former_url,data1)
        data = pd.merge(data,data1,on='Info')
        i += 1

    # data processing
    data = data.set_index(["Info"])
    data = data.T
    data = data[["series ordinal","president_name", "start time", "end time", "replaces", "image"]]
    data = data.reset_index()
    data = data.drop(["index"], axis=1)
    data = data.loc[1:,]
    data["series ordinal"] = data["series ordinal"].apply((pd.to_numeric))
    data['start time'] = pd.to_datetime(data['start time'])
    data['end time'] = pd.to_datetime(data['end time'])
    data['start year'] = data['start time'].dt.year
    data['end year'] = data['end time'].dt.year
    data['served term'] = data['end year']-data['start year']  # served term
    print(data)
    # data.to_csv("test.csv")

    # data visualization
    # Table
    source = ColumnDataSource(data)
    columns = [
        TableColumn(field="series ordinal", title="series ordinal"),
        TableColumn(field="president_name", title="president_name"),
        TableColumn(field="start time", title="start time",formatter=DateFormatter()),
        TableColumn(field="end time", title="end time",formatter=DateFormatter()),
        TableColumn(field="replaces", title="replaces"),
        TableColumn(field="image", title="image",),
    ]
    data_table = DataTable(source=source, columns=columns, width=1500, height=500)
    show(data_table)


    """
    x = data['series ordinal']
    y = data['served term']
    p = figure(
        title="the former president of us",
        toolbar_location=None,
        tools=[HoverTool()],
        tooltips="Data point @x has the value @y",
        width=350,
        height=250,
        x_axis_label="series ordinal of the former president",
        y_axis_label="served term",
    )
    circle = p.circle(x, y, fill_color="red", size=15)
    show(p)
    """
















