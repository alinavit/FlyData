import logging
import logging.config
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import time

logging.config.fileConfig("C:\\Users\\48575\\PycharmProjects\\FlyData\\conf\\logging.conf")
logger = logging.getLogger('DataTransferCSV')


class FlyData:
    """
    url = General URL (provide if one url is responsible for all extract)
    default arr [default True] = case when one url and from there we have to click and switch to another
    data default_arr = True means first we come to arrival data, False - to departures data
    switch selector [default None] - selector to switch to another data
    url_arr = URL of Arrivals
    url_dep = URL of Departures
    selenium = True , selenium is going to e used , if False  - requests is going to be used
    cookies selector = For selenium Only. Selector to accept cookies
    pcode = Airport code , is going to be used in the file

    """
    def __init__(self, url=None, default_arr=True, switch_selector=None, url_arr=None, url_dep=None, selenium=False,
                 cookies_selector=None, pcode='UNKNOWN'):
        self.url = url
        self.url_arr = url_arr
        self.url_dep = url_dep
        self.selenium = selenium
        self.cookies_selector = cookies_selector if self.selenium else None
        self.default_arr = default_arr if selenium else None
        self.switch_selector = switch_selector if selenium else None
        self.pcode = pcode

        self.soup = None
        self.soup_arr = None
        self.soup_dep = None

    def fetch_data_selenium(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.common.by import By

        # case when 2 links
        if self.url and (self.url_arr or self.url_dep):
            logger.warning('Please specify correctly URLs!')

        elif self.url_arr and self.url_dep and not self.url:
            try:
                # arrivals
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                driver.get(self.url_arr)
                driver.implicitly_wait(10)

                if self.cookies_selector:
                    for cookie_selector in self.cookies_selector:
                        accept_cookies = driver.find_element(By.CSS_SELECTOR, cookie_selector)
                        accept_cookies.click()
                        time.sleep(3)

                arrivals = driver.page_source
                self.soup_arr = BeautifulSoup(arrivals, 'lxml')

                # departures
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                driver.get(self.url_dep)
                driver.implicitly_wait(10)

                if self.cookies_selector:
                    for cookie_selector in self.cookies_selector:
                        accept_cookies = driver.find_element(By.CSS_SELECTOR, cookie_selector)
                        accept_cookies.click()
                        time.sleep(3)
                # TODO maybe it can be done as a separate method? cookies selector

                departures = driver.page_source
                self.soup_dep = BeautifulSoup(departures, 'lxml')

                logger.info('Successfully fetched data from both URLs')

            except Exception as e:
                logger.critical(f'Failed to fetch data from one of 2 URLs (Selenium)')
                logger.exception(f'Exception:{e}')

        # case when one link
        elif self.url and not self.url_arr and not self.url_dep:

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(self.url)
            time.sleep(3)

            try:
                if self.cookies_selector:
                    for cookie_selector in self.cookies_selector:
                        accept_cookies = driver.find_element(By.CSS_SELECTOR, cookie_selector)
                        accept_cookies.click()
                        time.sleep(3)

                else:
                    pass
                logger.info(f'Successfully fetched data from URL')
            except Exception as e:
                logger.critical(f'Failed to fetch data from URL (Selenium)')
                logger.exception(f'Exception:{e}')

            try:
                if self.default_arr is False:
                    # departures as default
                    departures = driver.page_source
                    self.soup_dep = BeautifulSoup(departures, 'lxml')

                    arrivals = driver.find_element(By.CSS_SELECTOR, self.switch_selector)
                    driver.execute_script("arguments[0].scrollIntoView();", arrivals)
                    driver.execute_script("arguments[0].click();", arrivals)
                    # arrivals_b.click()
                    time.sleep(3)
                    page_content = driver.page_source
                    self.soup_arr = BeautifulSoup(page_content, 'lxml')
                    logger.info('Data is ready for processing to Data Frames')

                elif self.default_arr is True:
                    # arrivals as default
                    arrivals = driver.page_source
                    self.soup_arr = BeautifulSoup(arrivals, 'lxml')

                    departures = driver.find_element(By.CSS_SELECTOR, self.switch_selector)
                    driver.execute_script("arguments[0].scrollIntoView();", departures)
                    driver.execute_script("arguments[0].click();", departures)
                    time.sleep(3)
                    # arrivals_b.click()
                    page_content = driver.page_source
                    self.soup_dep = BeautifulSoup(page_content, 'lxml')
                    logger.info('Data is ready for processing to Data Frames')

                else:
                    logger.warning('Have you specified Default page? If it is arrivals or departures')

            except Exception as e:
                logger.critical('Error occurred processing for Data Frames')
                logger.exception(f'Exception: {e}')

        else:
            logger.warning('URLs seem to be gives as wrong parameters')

    def fetch_data_requests(self):
        import requests
        # 2 links
        if self.url_arr and self.url_dep and not self.url:
            try:
                source_arr = requests.get(self.url_arr).text
                self.soup_arr = BeautifulSoup(source_arr, 'lxml')

                source_dep = requests.get(self.url_dep).text
                self.soup_dep = BeautifulSoup(source_dep, 'lxml')

                logger.info(f'Successfully fetched data from URLs')
            except Exception as e:
                logger.critical(f'Failed to fetch data from URLs')
                logger.exception(f'Exception: {e}')

        elif self.url and not self.url_dep and not self.url_arr:
            # 1 link
            try:
                source = requests.get(self.url).text
                self.soup = BeautifulSoup(source, 'lxml')

                self.soup_arr = self.soup.find('div', attrs={'id': 'arrivalsInfo'})  # USED IN SZZ ONLY
                self.soup_dep = self.soup.find('div', attrs={'id': 'departuresInfo'})  # USED IN SZZ ONLY

                logger.info(f'Successfully fetched data from URL')
            except Exception as e:
                logger.critical(f'Failed to fetch data from URL')
                logger.exception(f'Exception: {e}')
        else:

            logger.warning(f'Unexpected logic fetching data (requests)')

    def harvest_data(self, soup_section, arrival=True):
        pass

    def etl_csv(self):
        if self.selenium:
            self.fetch_data_selenium()
        else:
            self.fetch_data_requests()

        if self.soup_arr and self.soup_dep:
            arrivals = self.harvest_data(self.soup_arr)
            departures = self.harvest_data(self.soup_dep, arrival=False)

            df_arr = pd.DataFrame(arrivals)
            df_dep = pd.DataFrame(departures)

            df_all = pd.concat([df_arr, df_dep], ignore_index=True)

            date = datetime.today().strftime("%m_%d_%Y_%H_%M_%S")
            filename = f'files\\{self.pcode}_{date}.csv'
            df_all.to_csv(filename, index=False)
            logger.info(f'Data successfully saved to CSV file: {filename}')

        elif not self.soup_arr or not self.soup_dep:
            logger.warning('arrivals or departures were not fetched. No data to process or save')

        else:
            logger.warning('No data to process or save')


class FlyDataSZZ(FlyData):
    """
    url = General URL (provide if one url is responsible for all extract)
    default arr [default True] = case when one url and from there we have to click and switch to another data
    default_arr = True means first we come to arrival data, False - to departures data
    switch selector [default None] - selector to switch to another data
    url_arr = URL of Arrivals
    url_dep = URL of Departures
    selenium = True , selenium is going to e used , if False  - requests is going to be used
    cookies selector = For selenium Only. Selector to accept cookies
    pcode = Airport code , is going to be used in the file

    """
    def __init__(self, url=None, default_arr=True, switch_selector=None, url_arr=None, url_dep=None, selenium=False,
                 cookies_selector=None, pcode='UNKNOWN'):
        super().__init__(url, default_arr, switch_selector, url_arr, url_dep, selenium, cookies_selector, pcode)

        self.soup = None
        self.soup_arr = None
        self.soup_dep = None

    def harvest_data(self, soup_section, arrival=True):

        data = []

        for i in soup_section.find_all('tr'):
            date = ''
            flight = ''
            direction = ''
            status = ''

            try:
                date = i.find('td', attrs={'data-title': 'Czas'}).text
            except AttributeError:
                date = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception {e}')

            try:
                flight = i.find('td', attrs={'data-title': 'Lot'}).text
            except AttributeError:
                flight = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception {e}')

            try:
                direction = i.find('td', attrs={'data-title': 'Kierunek'}).text
            except AttributeError:
                direction = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception {e}')

            try:
                status = i.find('td', attrs={'data-title': 'Status'}).text
                status = status.replace('\t', '').replace('\n', '')
            except AttributeError:
                status = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception {e}')

            if arrival:
                data.append({
                    'date': date,
                    'flight': flight,
                    'destination': self.pcode,
                    'status': status,
                    'start_airport': direction,
                    'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                    'type': 'arrival_data'
                })
            else:
                # departures
                data.append({
                    'date': date,
                    'flight': flight,
                    'destination': direction,
                    'status': status,
                    'start_airport': self.pcode,
                    'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                    'type': 'departure_data'
                })

        logger.info(f'Data gathered successfully for {"arrivals" if arrival else "departures"}')
        return data


class FlyDataGDN(FlyData):
    """
    url = General URL (provide if one url is responsible for all extract)
    default arr [default True] = case when one url and from there we have to click and switch to another data
    default_arr = True means first we come to arrival data, False - to departures data
    switch selector [default None] - selector to switch to another data
    url_arr = URL of Arrivals
    url_dep = URL of Departures
    selenium = True , selenium is going to e used , if False  - requests is going to be used
    cookies selector = For selenium Only. Selector to accept cookies
    pcode = Airport code , is going to be used in the file

    """
    def __init__(self, url=None, default_arr=True, switch_selector=None, url_arr=None, url_dep=None, selenium=False,
                 cookies_selector=None, pcode='UNKNOWN'):
        super().__init__(url, default_arr, switch_selector, url_arr, url_dep, selenium, cookies_selector, pcode)

        self.soup = None
        self.soup_arr = None
        self.soup_dep = None

    def harvest_data(self, soup_section, arrival=True):
        data = []

        table = soup_section.find('div', class_='table__body')
        # rows = table.find_all('div', class_='table__time')

        for row in table.find_all('div', class_='table__element'):
            date = ''
            direction = ''
            flight = ''
            status = ''
            status_name = ''

            try:
                date = row.find('div', class_='table__time').text
                date = date.replace('\n', '')
            except AttributeError:
                date = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            try:
                direction = row.find('div', class_='table__airport').text
                direction = direction.replace('\n', '')
            except AttributeError:
                direction = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            try:
                flight = row.find('div', class_='table__flight').text
                flight = flight.replace('\n', '')
            except AttributeError:
                flight = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            parameters = row.find_all('div')
            try:
                for parameter in parameters:
                    if 'table__status' in parameter['class']:
                        status_name = parameter['class']
                        status_name = ' '.join(status_name)
                    else:
                        status_name = ''

                status = row.find('div', class_=status_name).text
                status = status.replace('\n', '')
            except AttributeError:
                status = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            if arrival:
                data.append({'date': date,
                             'flight': flight,
                             'destination': self.pcode,
                             'status': status,
                             'start_airport': direction,
                             'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                             'type': 'arrival_data'

                             })

            else:
                data.append({'date': date,
                             'flight': flight,
                             'destination': direction,
                             'status': status,
                             'start_airport': self.pcode,
                             'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                             'type': 'departure_data'
                             })

        return data


class FlyDataKTW(FlyData):
    """
    url = General URL (provide if one url is responsible for all extract)
    default arr [default True] = case when one url and from there we have to click and switch to another data
    default_arr = True means first we come to arrival data, False - to departures data
    switch selector [default None] - selector to switch to another data
    url_arr = URL of Arrivals
    url_dep = URL of Departures
    selenium = True , selenium is going to e used , if False  - requests is going to be used
    cookies selector = For selenium Only. Selector to accept cookies
    pcode = Airport code , is going to be used in the file

    """
    def __init__(self, url=None, default_arr=True, switch_selector=None, url_arr=None, url_dep=None, selenium=False,
                 cookies_selector=None, pcode='UNKNOWN'):
        super().__init__(url, default_arr, switch_selector, url_arr, url_dep, selenium, cookies_selector, pcode)

        self.soup = None
        self.soup_arr = None
        self.soup_dep = None

    def harvest_data(self, soup_section, arrival=True):
        data = []

        date = ''
        direction = ''
        flight = ''
        status = ''

        table = soup_section.find_all('div', class_='timetable__row flight-board__row')

        for i in table:
            try:
                date = i.find('div', class_='timetable__col flight-board__col--1').text
            except AttributeError:
                date = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            try:
                direction = i.find('div', class_='timetable__col flight-board__col--2').text
            except AttributeError:
                direction = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            # company = i.find('div', class_='timetable__col flight-board__col--3').img['alt']
            try:
                flight = i.find('div', class_='timetable__col flight-board__col--4').text
            except AttributeError:
                flight = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            try:
                status = i.find('div', class_='timetable__col flight-board__col--5 flight-board__col--lowercase').text
            except AttributeError:
                status = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            if arrival:
                data.append({'date': date,
                             'flight': flight,
                             'destination': self.pcode,
                             'status': status,
                             'start_airport': direction,
                             'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                             'type': 'arrival_data'

                             })

            else:
                data.append({'date': date,
                             'flight': flight,
                             'destination': direction,
                             'status': status,
                             'start_airport': self.pcode,
                             'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                             'type': 'departure_data'
                             })
        return data


class FlyDataPOZ(FlyData):
    """
    url = General URL (provide if one url is responsible for all extract)
    default arr [default True] = case when one url and from there we have to click and switch to another data
    default_arr = True means first we come to arrival data, False - to departures data
    switch selector [default None] - selector to switch to another data
    url_arr = URL of Arrivals
    url_dep = URL of Departures
    selenium = True , selenium is going to e used , if False  - requests is going to be used
    cookies selector = For selenium Only. Selector to accept cookies
    pcode = Airport code , is going to be used in the file

    """
    def __init__(self, url=None, default_arr=True, switch_selector=None, url_arr=None, url_dep=None, selenium=False,
                 cookies_selector=None, pcode='UNKNOWN'):
        super().__init__(url, default_arr, switch_selector, url_arr, url_dep, selenium, cookies_selector, pcode)

        self.soup = None
        self.soup_arr = None
        self.soup_dep = None

    def harvest_data(self, soup_section, arrival=True):
        data = []

        date = ''
        direction = ''
        flight = ''
        status = ''

        table = soup_section.find_all('li', class_='boardArchive__item')

        for i in table:
            row = i.ul
            try:
                date = row.div.text
                date = date.replace('Godzina', '').replace('\n ', '').replace(' ', '')
            except AttributeError:
                date = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            try:
                direction = i.find('li', class_='boardArchive__itemColumn boardArchive__itemColumn--destination')\
                    .text.strip()
            except AttributeError:
                direction = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            # company = i.find('div', class_='timetable__col flight-board__col--3').img['alt']
            try:
                flight = i.find('li', class_='boardArchive__itemColumn boardArchive__itemColumn--number').text.strip()
            except AttributeError:
                flight = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            try:
                status = i.find('li', class_='boardArchive__itemColumn boardArchive__itemColumn--status').text.strip()
                status = status.replace('Status', '').replace('\n ', '').replace(' ', '')
            except AttributeError:
                status = ''
            except Exception as e:
                logging.critical('An unexpected error occurred')
                logging.exception(f'Exception: {e}')

            if arrival:
                data.append({'date': date,
                             'flight': flight,
                             'destination': self.pcode,
                             'status': status,
                             'start_airport': direction,
                             'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                             'type': 'arrival_data'

                             })

            else:
                data.append({'date': date,
                             'flight': flight,
                             'destination': direction,
                             'status': status,
                             'start_airport': self.pcode,
                             'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                             'type': 'departure_data'
                             })
        return data


class FlyDataLCJ(FlyData):
    """
    url = General URL (provide if one url is responsible for all extract)
    default arr [default True] = case when one url and from there we have to click and switch to another data
    default_arr = True means first we come to arrival data, False - to departures data
    switch selector [default None] - selector to switch to another data
    url_arr = URL of Arrivals
    url_dep = URL of Departures
    selenium = True , selenium is going to e used , if False  - requests is going to be used
    cookies selector = For selenium Only. Selector to accept cookies
    pcode = Airport code , is going to be used in the file

    """
    def __init__(self, url=None, default_arr=True, switch_selector=None, url_arr=None, url_dep=None, selenium=False,
                 cookies_selector=None, pcode='UNKNOWN'):
        super().__init__(url, default_arr, switch_selector, url_arr, url_dep, selenium, cookies_selector, pcode)

        self.soup = None
        self.soup_arr = None
        self.soup_dep = None

    def harvest_data(self, soup_section, arrival=True):
        data = []
        try:
            table = soup_section.find('table', class_='table mb-0 text-uppercase').tbody
            rows = []
            for i in table:
                rows.append(i.text)

            rows = [i.replace('\n', '|').strip('|') for i in rows if i != '\n']
            rows = [i.split('|') for i in rows]

            for row in rows:
                if arrival:
                    data.append({'date': row[0],
                                 'flight': row[2],
                                 'destination': self.pcode,
                                 'status': row[3],
                                 'start_airport': row[1],
                                 'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                                 'type': 'arrival_data'

                                 })

                else:
                    data.append({'date': row[0],
                                 'flight': row[2],
                                 'destination': row[1],
                                 'status': row[3],
                                 'start_airport': self.pcode,
                                 'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                                 'type': 'departure_data'
                                 })
            return data

        except Exception as e:
            logger.error(f'Error extracting data')
            logging.exception(f'Exception {e}')


class FlyDataKRK(FlyData):
    """
    url = General URL (provide if one url is responsible for all extract)
    default arr [default True] = case when one url and from there we have to click and switch to another data
    default_arr = True means first we come to arrival data, False - to departures data
    switch selector [default None] - selector to switch to another data
    url_arr = URL of Arrivals
    url_dep = URL of Departures
    selenium = True , selenium is going to e used , if False  - requests is going to be used
    cookies selector = For selenium Only. Selector to accept cookies
    pcode = Airport code , is going to be used in the file

    """
    def __init__(self, url=None, default_arr=True, switch_selector=None, url_arr=None, url_dep=None, selenium=False,
                 cookies_selector=None, pcode='UNKNOWN'):
        super().__init__(url, default_arr, switch_selector, url_arr, url_dep, selenium, cookies_selector, pcode)

        self.soup = None
        self.soup_arr = None
        self.soup_dep = None

    def harvest_data(self, soup_section, arrival=True):
        import re
        data = []

        table = soup_section.find('tbody')
        rows = []
        for i in table:
            rows.append(i.text)

        rows = [re.sub(r'\n+|\s{2,}', '|', i) for i in rows if i != '\n']
        rows = [i.split('|') for i in rows]

        for row in rows:
            if arrival:
                data.append({'date': row[1],
                             'flight': row[5],
                             'destination': self.pcode,
                             'status': row[7],
                             'start_airport': row[3],
                             'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                             'type': 'arrival_data'

                             })

            else:
                data.append({'date': row[1],
                             'flight': row[5],
                             'destination': row[3],
                             'status': row[7],
                             'start_airport': self.pcode,
                             'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                             'type': 'departure_data'
                             })
        return data


class FlyDataWMI(FlyData):
    """
     url = General URL (provide if one url is responsible for all extract)
     default arr [default True] = case when one url and from there we have to click and switch to another data
     default_arr = True means first we come to arrival data, False - to departures data
     switch selector [default None] - selector to switch to another data
     url_arr = URL of Arrivals
     url_dep = URL of Departures
     selenium = True , selenium is going to e used , if False  - requests is going to be used
     cookies selector = For selenium Only. Selector to accept cookies
     pcode = Airport code , is going to be used in the file

     """

    def __init__(self, url=None, default_arr=True, switch_selector=None, url_arr=None, url_dep=None, selenium=False,
                 cookies_selector=None, pcode='UNKNOWN'):
        super().__init__(url, default_arr, switch_selector, url_arr, url_dep, selenium, cookies_selector, pcode)

        self.soup = None
        self.soup_arr = None
        self.soup_dep = None

    def harvest_data(self, soup_section, arrival=True):

        data = []

        if arrival:
            table_arr = soup_section.find('table', 'arrivals-table active')

            for idx, tr in enumerate(table_arr.find_all('tr')):

                if idx != 0:
                    row = [i.text for i in tr]

                    data.append(
                        {'date': row[2],
                         'flight': row[0],
                         'destination': self.pcode,
                         'status': row[3],
                         'start_airport': row[2],
                         'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                         'type': 'arrival_data'

                         }
                    )

        else:
            table_dep = soup_section.find('table', 'departures-table')

            for idx, tr in enumerate(table_dep.find_all('tr')):
                if idx != 0:
                    row = [i.text for i in tr]

                    data.append(
                        {'date': row[2],
                         'flight': row[0],
                         'destination': row[2],
                         'status': row[3],
                         'start_airport': self.pcode,
                         'time_reg': datetime.today().strftime("%m/%d/%Y, %H:%M:%S"),
                         'type': 'departure_data'
                         }
                    )

        logger.info(f'Data gathered successfully for {"arrivals" if arrival else "departures"}')
        return data

# TODO Warsaw  Warsaw Modlin
# TODO Krakow
# TODO remove visibility of chrome selenium
