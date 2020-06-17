### [Deecamp scrapers written with Scrapy]


#### Installation
- run `pip install -requirements.txt` 
- install and setup mongodb at port 27017

#### Usage
- Scrape down data from webpages
    - Sample
        - run `scrapy crawl ZillowBuySpider -o 'try_zillow_buy.json'` in the main directory
    - Customization
        - Create an item file that contains an object used to store data
        - Create a spider that stores the main logic of the crawling
        - run `scrapy crawl SPIDERNAME -o test.json` to test the spider