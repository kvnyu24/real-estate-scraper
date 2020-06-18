import os 
import multiprocessing as mp

def crawl(spider_name):
    os.system("scrapy crawl Fang{}Spider".format(spider_name))

if __name__ == "__main__":
    spiders_list = ["Esf", "XzlZu", "XzlShou"]
    p = mp.Pool()
    p.map_async(crawl, spiders_list)
    p.close()
    p.join()