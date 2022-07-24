# -*- coding: utf-8 -*-

import os 
from apscheduler.schedulers.blocking import BlockingScheduler
import multiprocessing as mp
import datetime
import oss2
import shutil
import json
from .base_api import BaseAPI


class BaiduQXAPI(BaseAPI):
    """Baiduqx API."""

    def __init__(self, time_between):
        """
        the spiders are initiated every @param:time_between seconds
        @param(int:seconds):time_between
        """
        self.bucket = oss2.Bucket(oss2.Auth(YOUR_ACCESS_KEY_ID, YOUR_ACCESS_KEY_SECRET), YOUR_BUCKET_URL, 'baiduqx')
        self.time_between = time_between


    def crawl(self):
        scheduler = BlockingScheduler()
        scheduler.add_job(self.mp_crawl, 'interval', seconds=self.time_between)
        print("Job added.")
        scheduler.start()
        print("Spider initiated")


    def crawl_baiduqx(self, spider_name):
        timestamp =  datetime.datetime.now().strftime("%Y-%m-%d-%I-%M-%p")
        os.system("scrapy crawl BaiduQx{}Spider -o baiduqx_{}_at_{}.json".format(spider_name, spider_name, timestamp))
        
        self.bucket.put_object_from_file('baiduqx_{}_at_{}.json'.format(spider_name, timestamp), 'baiduqx_{}_at_{}.json'.format(spider_name, timestamp))
        os.system('rm baiduqx_{}_at_{}.json'.format(spider_name, timestamp))

    def mp_crawl(self):
        startstamp =  datetime.datetime.now().strftime("%Y-%m-%d-%I-%M-%p")
        print("Crawling at {}".format(startstamp))
        spiders_list = ["If", "Io", "Mi"]
        p = mp.Pool()
        p.map_async(self.crawl_baiduqx, spiders_list)
        p.close()
        p.join()
        
        finishstamp = datetime.datetime.now().strftime("%Y-%m-%d-%I-%M-%p")
        print("Job finished at {}".format(finishstamp))


    def get(self, timestamp_a, timestamp_b, data_type, target_path):
        """
        get baiduqx data between @param:timestamp_a and @param:timestamp_b at @param:city
        @param(str:yyyy_mm_dd):timestamp_a
        @param(str:yyyy_mm_dd):timestamp_b
        @param(str):data_type
        """
        time_a = [int(i) for i in timestamp_a.split("_")]
        time_b = [int(i) for i in timestamp_b.split("_")]
        timestamp_a = datetime.date(time_a[0], time_a[1], time_a[2])
        timestamp_b = datetime.date(time_b[0], time_b[1], time_b[2])

        files = [obj.key for obj in oss2.ObjectIterator(self.bucket)]
        res_files = []
        for obj_file in files:
            creation_time = obj_file.split("_")[-1].strip(".json") 
            creation_times = creation_time.split("-")
            obj_data_type = obj_file.split("_")[1] 
            timestamp_created = datetime.date(int(creation_times[0]), int(creation_times[1]), int(creation_times[2]))
            if timestamp_created >= timestamp_a and timestamp_created <= timestamp_b:
                if obj_data_type == data_type:
                    res_files.append(obj_file)

        for obj_file in res_files:
            object_stream = self.bucket.get_object(obj_file)
            with open(os.path.join(target_path, obj_file), 'wb') as local_fileobj:
                shutil.copyfileobj(object_stream, local_fileobj)
        return



