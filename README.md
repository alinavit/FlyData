# FlyData
Fly Data project gatheres data from Polish airports related to current arrivals and departures. 
The data is extracted, transformed, and loaded into a PostgreSQL database using Python. 
Additionally, the project includes a procedure to archive daily data and a view for Power BI visualization.

![FlyData.png](https://github.com/alinavit/FlyData/blob/main/FlyData.png)

## Project Components
1. [main.py](https://github.com/alinavit/FlyData/blob/main/main.py) - runs ETL
2. [fly_extract.py](https://github.com/alinavit/FlyData/blob/main/fly_extract.py) - holds all details on data move
3. [logging.conf](https://github.com/alinavit/FlyData/blob/main/conf/logging.conf) - configuration for logging
4. [database.py](https://github.com/alinavit/FlyData/blob/main/database.py) - holds scripts to connect and write data to postgres database
5. [clean_data_m](https://github.com/alinavit/FlyData/blob/main/DDL.sql) - procedure for cleaning data_m table and move the data to data_hst
6. [v_data_m](https://github.com/alinavit/FlyData/blob/main/DDL.sql) - a view which is used in Power BI

## Prerequisites
1. Python 3.10
   * logging
   * psycopg2
   * selenium
   * bs4
   * requests
   * datetime
2. PostgreSQL


![FlyDataPBI](https://github.com/alinavit/FlyData/blob/main/FlyDataPBI.png)
