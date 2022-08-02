import requests
import time
import pandas as pd
import json
def site_validation(X,Y,url,save_file,iterations =2,additional = False):
    def validate_json(instance):
        try: 
            json.loads(instance)
            return True
        except ValueError as e:
            return False
        
    def validate():
        
        t0 = time.time()
        resp =requests.get(url)
        t1 = time.time() - t0
        
        flag = 'application/json' in resp.headers.get('content-type')
        
        str = f'Czas zdarzenia: {time.time()}, Czas otwarcia: {t1}, Kod: {resp.status_code}, Json: {flag}, Poprawność Jsona: {validate_json(resp.text)}'
        print(str)
        if additional: #dodatkowe
            df = pd.json_normalize(resp.json()['rates'])
            temp =df.effectiveDate.loc[df.mid.between(4.5,4.7)].to_string()
            str = str + ', Daty: ' +temp
            
        return (str + '\n')
    
    for j in range(iterations):
        starttime = time.time()
        for i in range(X):
            with open(save_file, 'a') as the_file:
                the_file.write(validate())
                
            
        time.sleep(Y - ((time.time() - starttime) % Y))
        
url = 'http://api.nbp.pl/api/exchangerates/rates/a/eur/last/100/?format=json'
site_validation(10,5,url,"log.txt",additional= True)