import fly_extract
import logging.config
import os

logging.config.fileConfig("C:\\Users\\48575\\PycharmProjects\\FlyData\\conf\\logging.conf")
logger = logging.getLogger('webMon')


class WebMon(fly_extract.FlyData):
    def __init__(self, url=None, default_arr=True, switch_selector=None, url_arr=None, url_dep=None, selenium=False,
                 cookies_selector=None, pcode='UNKNOWN'):
        super().__init__(url, default_arr, switch_selector, url_arr, url_dep, selenium, cookies_selector, pcode)

        self.soup = None
        self.soup_arr = None
        self.soup_dep = None

    def detect_change(self):
        if self.selenium:
            self.fetch_data_selenium()
        else:
            self.fetch_data_requests()
        logger.info(f'Page is read using {"selenium" if self.selenium else "requests"}')

        if self.soup_arr and self.soup_dep:
            file_arr_exists = os.path.isfile(f"files\\f_prev_arr_{self.pcode}.txt")
            file_dep_exists = os.path.isfile(f"files\\f_prev_dep_{self.pcode}.txt")

            if not file_arr_exists or not file_dep_exists:
                logger.info('No files detected. Creating files...')
                # create file if it doesn't exist yet
                with open(f'files\\f_prev_arr_{self.pcode}.txt', 'w+', encoding='utf-8') as file:
                    file.write(str(self.soup_arr))
                with open(f'files\\f_prev_dep_{self.pcode}.txt', 'w+', encoding='utf-8') as file:
                    file.write(str(self.soup_dep))

                return [True, True]

            else:
                # read file - > compare -> return if diff catch
                logger.info('Reading and comparing files...')
                with open(f'files\\f_prev_arr_{self.pcode}.txt', 'r+', encoding='utf-8') as file:
                    prev_arr = file.read()
                    diff_catch_arr = str(self.soup_arr) != prev_arr
                    file.seek(0)
                    file.write(str(self.soup_arr))

                with open(f'files\\f_prev_dep_{self.pcode}.txt', 'r+', encoding='utf-8') as file:
                    prev_dep = file.read()
                    diff_catch_dep = str(self.soup_dep) != prev_dep
                    file.seek(0)
                    file.write(str(self.soup_dep))

                logger.info(f'{"changes detected" if diff_catch_arr or diff_catch_dep else "changes not detected"}')

                return [diff_catch_arr, diff_catch_dep]

        elif self.soup and not self.soup_arr and not self.soup_dep:
            file_one_exists = os.path.isfile(f"\\files\\f_prev_{self.pcode}.txt")
            if not file_one_exists:
                logger.info('No file detected. Creating file...')
                # create file if it doesn't exist yet
                with open(f'files\\f_prev_{self.pcode}.txt', 'w+', encoding='utf-8') as file:
                    file.write(str(self.soup_arr))
                return [False]
            else:
                with open(f'files\\f_prev_{self.pcode}.txt', 'r+', encoding='utf-8') as file:
                    prev = file.read()
                    diff_catch = str(self.soup) != prev
                    file.seek(0)
                    file.write(str(self.soup))

                    logger.info(f'{"changes detected" if diff_catch else "changes not detected"}')

                    return [diff_catch]
        else:
            logger.warning('Something went wrong')
