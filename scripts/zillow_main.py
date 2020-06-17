import os 
import multiprocessing as mp

def crawl(spider_name):
    os.system("scrapy crawl {}".format(spider_name))

if __name__ == "__main__":
    spiders_list = ["ZillowBuy", "ZillowRent", "ZillowForeclosure"]
    p = mp.Pool()
    p.map_async(crawl, spiders_list)
    p.close()
    p.join()