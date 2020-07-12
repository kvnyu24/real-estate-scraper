from api.qqheat_api import QQHeatAPI    
    
    
    
qq_try = QQHeatAPI()
print(len(qq_try.get("2020_07_11", "2020_07_12", "tmp")))
