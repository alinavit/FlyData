import logging.config
import config
import fly_extract
from timeit import default_timer

start = default_timer()

logging.config.fileConfig("C:\\Users\\48575\\PycharmProjects\\FlyData2\\conf\\logging.conf")
logger = logging.getLogger('FlyDataMain')

logger.info('Start Main')

gatherer_szz = fly_extract.FlyDataSZZ(url=config.URL_SZZ,
                                      pcode='SZZ')
gatherer_szz.etl_csv()

gatherer_gdn = fly_extract.FlyDataGDN(url_arr=config.URL_GDN_ARR,
                                      url_dep=config.URL_GDN_DEP,
                                      pcode='GDN')
gatherer_gdn.etl_csv()

gatherer_ktw = fly_extract.FlyDataKTW(url=config.URL_KTW,
                                      pcode='KTW',
                                      selenium=True,
                                      default_arr=False,
                                      cookies_selector=config.COOKIES_KTW,
                                      switch_selector=config.SWITCH_KTW)
gatherer_ktw.etl_csv()

gatherer_poz = fly_extract.FlyDataPOZ(url=config.URL_POZ,
                                      pcode='POZ',
                                      selenium=True,
                                      default_arr=True,
                                      cookies_selector=config.COOKIES_POZ,
                                      switch_selector=config.SWITCH_POZ)
gatherer_poz.etl_csv()

gatherer_lcj = fly_extract.FlyDataLCJ(url=config.URL_LCJ,
                                      pcode='LCJ',
                                      selenium=True,
                                      default_arr=False,
                                      cookies_selector=config.COOKIES_LCJ,
                                      switch_selector=config.SWITCH_LCJ)
gatherer_lcj.etl_csv()

gatherer_krk = fly_extract.FlyDataKRK(url_arr=config.URL_KRK_ARR,
                                      url_dep=config.URL_KRK_DEP,
                                      pcode='KRK',
                                      selenium=True)
gatherer_krk.etl_csv()

gatherer_wmi = fly_extract.FlyDataWMI(url=config.URL_WMI,
                                      pcode='WMI',
                                      selenium=True,
                                      cookies_selector=config.COOKIES_WMI,
                                      switch_selector=config.SWITCH_WMI,
                                      default_arr=True)
gatherer_wmi.etl_csv()

stop = default_timer()
print(stop-start)



# TODO Schedule
