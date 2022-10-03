from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

class ActionStockTracker(Action):
    def name(self) -> Text :
        return "stock_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        
        
        # get the location slot

        name = tracker.get_slot('stock_name')
        #name = "HAL"
        

                        
        stock_url  = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol='+ name
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
        response = requests.get(stock_url, headers=headers)
        if str(response) == '<Response [200]>':
            soup = BeautifulSoup(response.text, 'html.parser')
            data_array = soup.find(id='responseDiv').getText()
            jsonStr = json.loads(data_array)
            date=jsonStr['tradedDate']
            #trade_date.append(date)
            name = jsonStr['data'][0]['symbol']
            #stock_name.append(name)
            close_p = jsonStr['data'][0]['closePrice']
            #stock_closePrice.append(close_p)
            last_p = jsonStr['data'][0]['lastPrice']
            #stock_lastPrice.append(last_p)
        else:
            print("Error : Requst cannot be completed!")

        message1="Date: "+date+" Name: "+name+" Close Price: "+close_p+" Last Price: "+last_p
        dispatcher.utter_message(text=message1)

        return []