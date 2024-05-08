import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy.dialects.sqlite import insert
from datetime import datetime

engine = create_engine("sqlite:///uiuc_crime_log.sqlite")
metadata = MetaData()
crime_log_table = Table("crime_log", metadata,
                        Column("number", String, primary_key=True),
                        Column("reported_date_time", String, primary_key=True),
                        Column("occurred_date_time", String, primary_key=True),
                        Column("location", String, primary_key=True),
                        Column("description", String, primary_key=True),
                        Column("disposition", String, primary_key=True))
metadata.create_all(engine)

url = "https://police.illinois.edu/info/daily-crime-log/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
tbody = soup.select_one("tbody")
crime_logs = tbody.find_all("tr")

with engine.connect() as connection:
    for log in crime_logs:
        number = log.select_one("td:nth-child(1)")
        reported_date_time = log.select_one("td:nth-child(2)")
        reported_date_time = reported_date_time.text
        if len(reported_date_time) >= 14:
            date_object = datetime.strptime(reported_date_time, "%m/%d/%Y %H:%M")
            reported_date_time = date_object.strftime("%Y-%m-%d %H:%M")
        else:
            date_object = datetime.strptime(reported_date_time, "%m/%d/%y %H:%M")
            reported_date_time = date_object.strftime("%Y-%m-%d %H:%M")
        occurred_date_time = log.select_one("td:nth-child(3)")
        location = log.select_one("td:nth-child(4)")
        description = log.select_one("td:nth-child(5)")
        disposition = log.select_one("td:nth-child(6)")

        insert_query = insert(crime_log_table).values(number=number.text,
                                                      reported_date_time=reported_date_time,
                                                      occurred_date_time=occurred_date_time.text,
                                                      location=location.text,
                                                      description=description.text,
                                                      disposition=disposition.text)
        connection.execute(insert_query.on_conflict_do_nothing(index_elements=['number',
                                                                               'reported_date_time',
                                                                               'occurred_date_time',
                                                                               'location',
                                                                               'description',
                                                                               'disposition']))
    connection.commit()
