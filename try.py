from api.qqheat_api import QQHeatAPI    
from api.ke_api import KeAPI   
    
    
# qq_try = QQHeatAPI()
# print(len(qq_try.get("2020_07_11", "2020_07_12", "tmp")))
ke_try = KeAPI(5, "北京", 30)
ke_try.crawl()