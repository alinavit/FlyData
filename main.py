import logging
import logging.config


import fly_extract

logging.config.fileConfig("C:\\Users\\48575\\PycharmProjects\\FlyData2\\conf\\logging.conf")
logger = logging.getLogger('FlyDataMain')


logger.info('Start Main')


# URL = 'https://airport.com.pl/'
# gatherer = fly_extract.FlyDataSZZ(url=URL, pcode='SZZ')
# gatherer.etl_csv()



# URL_PA = 'https://www.airport.gdansk.pl/loty/tablica-przylotow-p1.html'
# URL_PD = 'https://www.airport.gdansk.pl/loty/tablica-odlotow-p2.html'
# gatherer_gdn = fly_extract.FlyDataGDN(url_arr=URL_PA, url_dep=URL_PD, pcode='GDN')
# gatherer_gdn.etl_csv()

# URL_KTW = 'https://www.katowice-airport.com/pl/dla-pasazera/tablica-lotow-online'
# cookies = ['#mr > div > section > div > div > button.button.button--smaller.button--green.button--chevron.cookies__button.js-cookies-accept']
# switch = '#App > section > section.filter-board.charters__filter.filter__container.container > div > form > div > div.radio-button.filter-board__flight.filter-board__container > div > div:nth-child(1) > label'
# gatherer_ktw = fly_extract.FlyDataKTW(url=URL_KTW, pcode='KTW', selenium=True, default_arr=False, cookies_selector=cookies, switch_selector=switch)
# gatherer_ktw.etl_csv()

# URL_POZ = 'https://poznanairport.pl/'
# COOKIES_POZ = ['#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll', 'body > div.alertBoxes > ul > li > div > button']
# SWITCH_POZ = 'body > section.flightsTabs > div > div > div > section > div.boardArchive__section > div > div > div > div.dataLoader__header > div > div > ul > li:nth-child(1) > ul > li:nth-child(4) > a > div.flightsTabs__menuTitle'
# gatherer_poz = fly_extract.FlyDataPOZ(url=URL_POZ, pcode='POZ', selenium=True, default_arr=True, cookies_selector=COOKIES_POZ, switch_selector=SWITCH_POZ)
# gatherer_poz.etl_csv()


# URL_LCJ  = 'https://www.lodz-airport.pl/en/passenger-zone/our-destinations'
# COOKIES_LCJ = ['#cookiesModal > div > div > div.modal-footer.justify-content-center > a.success.rounded-0']
# SWITCH_LCJ = 'body > div.content-page.d-flex.flex-wrap.align-items-stretch.justify-content-between > main > article > div > div.flights-table.simple > div.tabs > div.tab.arrival-tab.d-flex > span.tab-body.d-flex.align-items-center > a > span.d-none.d-sm-flex.flex-column.align-items-start.text-uppercase'
# gatherer_lcj = fly_extract.FlyDataLCJ(url=URL_LCJ, pcode='LCJ', selenium=True, default_arr=False, cookies_selector=COOKIES_LCJ, switch_selector=SWITCH_LCJ)
# gatherer_lcj.etl_csv()

URL_KRK_ARR = 'https://krakowairport.pl/en/passenger/flights/destinations/arrivals'
URL_KRK_DEP = 'https://krakowairport.pl/en/passenger/flights/destinations/departures'

gatherer_krk = fly_extract.FlyDataKRK(url_arr=URL_KRK_ARR, url_dep=URL_KRK_DEP, pcode='KRK', selenium=True )
gatherer_krk.etl_csv()



# TODO web monitor
# TODO postgres
# TODO Schedule
# TODO What are the next steps? Analysis?

