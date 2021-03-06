### [Deecamp scrapers written with Scrapy]


#### Installation
- run `pip install -r requirements.txt` 
- install and setup mongodb at port 27017
- Fill in your own parameter specs for Aliyun APIs.

#### Usage
- Scrape down data from webpages
    - Sample
        - run `scrapy crawl ZillowBuySpider -o 'try_zillow_buy.json'` in the main directory
    - Customization
        - Create an item file that contains an object used to store data
        - Create a spider that stores the main logic of the crawling
        - run `scrapy crawl SPIDERNAME -o test.json` to test the spider
    - Supports
        - zillow (buy/rent)
        - fangtianxia (ershoufang, zuxiezilou, shouxiezilou)
        - baiduqianxi (city/province-wise in/out, immigration/emmigration, internal flow)
        - qqheat (xingyun map)
        - beikezufang (ershoufang, xinfang, zufang)
    - API (bucket names can be easily changed from source code)
        - Base API
            - method: crawl
                - customizable crawling & upload files to oss & save to mongodb
            - method: get
                - download json files from oss to target dirrectories for usage
        - QQXingyuntu API
            - ```python
                from api.qqheat_api import QQHeatAPI
                # outside of this folder:
                # from deecamp_scraper.api.qqheat_api import QQHeatAPI  

                qqheat = QQHeatAPI(30) #time_between=30s
                # begin crawling
                qqheat.crawl()
                # get (timestamp_a, timestamp_b, save_dir)
                qqheat.get("2020_07_11", "2020_07_12", "tmp")

              ```
        - Beikezufang API
            - ```python
                from api.ke_api import KeAPI 
                # outside of this folder:
                # from deecamp_scraper.api.ke_api import KeAPI  
 
                ke_try = KeAPI(5, "北京", 30) #page_num=5, location="北京", time_between=30s
                # begin crawling
                ke_try.crawl() 
                # get (timestamp_a, timestamp_b, save_dir)
                ke_try.get("2020_07_11", "2020_07_12", "Esf", "tmp")
              ```
        
        - Baiduqianxi API
            - ```python
                from api.baiduqx_api import BaiduQXAPI 
                # outside of this folder:
                # from deecamp_scraper.api.baiduqx_api import BaiduQXAPI  
 
                baiduqx = BaiduQXAPI(30) #time_between=30s
                # begin crawling
                baiduqx.crawl() 
                # get (timestamp_a, timestamp_b, save_dir)
                baiduqx.get("2020_07_11", "2020_07_12", "Io", "tmp")
              ```
