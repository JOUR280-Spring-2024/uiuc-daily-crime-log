# UIUC's Daily Crime Log

This scraper extracts data from UIUC's [Daily Crime Log](https://police.illinois.edu/info/daily-crime-log/).

The data is stored as a SQLite database named `uiuc_crime_log.sqlite`.

All fields in the table are part of the primary key, since there are no
natural primary keys in the data. In fact, there are even duplicate records where all the values are identical.

The code can be run every day to add new records to the database. Previous records are retained and new
records are added.

If you end up using this database in a news report, please give credit to Elissa Eaton.