import os 
from apscheduler.schedulers.blocking import BlockingScheduler
import multiprocessing as mp
import datetime
import oss2



def crawl(spider_name):
    timestamp =  datetime.datetime.now().strftime("%Y-%m-%d-%I-%M-%p")
    os.system("scrapy crawl QQHeat{}Spider -o qq_{}_at_{}.json".format(spider_name, spider_name, timestamp))
    
    auth = oss2.Auth('LTAI4G8PBUWLB5t35TUdLjei', 'GXjsOJK6ML9wHWjGTca0DtxNyvzP2M')
    bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'qqxingyuntu')

    bucket.put_object_from_file('qq_{}_at_{}.json'.format(spider_name, timestamp), 'qq_{}_at_{}.json'.format(spider_name, timestamp))
    os.system("rm qq_{}_at_{}.json".format(spider_name, timestamp))

def mp_crawl():
    startstamp =  datetime.datetime.now().strftime("%Y-%m-%d-%I-%M-%p")
    print("Crawling at {}".format(startstamp))
    spiders_list = ["XingYun0", "XingYun1", "XingYun2", "XingYun3"]
    p = mp.Pool()
    p.map_async(crawl, spiders_list)
    p.close()
    p.join()
    
    finishstamp = datetime.datetime.now().strftime("%Y-%m-%d-%I-%M-%p")
    print("Job finished at {}".format(finishstamp))
    os.system("mongo qqheat --eval 'db.dropDatabase()'")



if __name__ == "__main__":
    print("Initiating program...")
    scheduler = BlockingScheduler()
    scheduler.add_job(mp_crawl, 'interval', hours=1)
    print("Job added.")
    scheduler.start()
    print("Spider initiated")

