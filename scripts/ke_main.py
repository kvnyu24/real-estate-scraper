import os 
from apscheduler.schedulers.blocking import BlockingScheduler
import multiprocessing as mp
import datetime
import oss2
import json


bucket = oss2.Bucket(oss2.Auth('LTAI4G8PBUWLB5t35TUdLjei', 'GXjsOJK6ML9wHWjGTca0DtxNyvzP2M'), 'http://oss-cn-shanghai.aliyuncs.com', 'beikezufang')
page_num = 100
location = "北京"


def crawl_ke(spider_name):
    timestamp =  datetime.datetime.now().strftime("%Y-%m-%d-%I-%M-%p")
    os.system("scrapy crawl Ke{}Spider -a page_num={} -a city_name={} -o ke_{}_{}_{}_at_{}.json".format(spider_name, page_num, location, spider_name, page_num, location, timestamp))
    
    bucket.put_object_from_file('ke_{}_{}_{}_at_{}.json'.format(spider_name, page_num, location, timestamp), 'ke_{}_{}_{}_at_{}.json'.format(spider_name, page_num, location, timestamp))
    os.system('rm ke_{}_{}_{}_at_{}.json'.format(spider_name, page_num, location, timestamp))

def mp_crawl():
    startstamp =  datetime.datetime.now().strftime("%Y-%m-%d-%I-%M-%p")
    print("Crawling at {}".format(startstamp))
    spiders_list = ["Xin", "Esf", "Zu"]
    p = mp.Pool()
    p.map_async(crawl_ke, spiders_list)
    p.close()
    p.join()
    
    finishstamp = datetime.datetime.now().strftime("%Y-%m-%d-%I-%M-%p")
    print("Job finished at {}".format(finishstamp))

if __name__ == "__main__":
    print("Initiating program...")
    scheduler = BlockingScheduler()
    scheduler.add_job(mp_crawl, 'interval', hours=1)
    print("Job added.")
    scheduler.start()
    print("Spider initiated")
