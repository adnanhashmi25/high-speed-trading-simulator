# from kafka import KafkaProducer
# import json
from stock_object import Stock
import csv
from datetime import datetime, timedelta


def start(stocks,st,et):

    st = datetime.strptime(st, "%Y-%m-%d")
    et = datetime.strptime(et, "%Y-%m-%d")

    # print(et.weekday())
    a = Stock()
    current_date = st
    # current_date = et
    data_hold = []
    # data_current = a.get_current_data(stocks,current_date)
    while current_date <= et:
        if current_date.weekday() in [5,6]:
            current_date += timedelta(days=1)
            continue
        data_before = a.last_week_stock_data(stocks,current_date)
        data_current = a.get_current_data(stocks,current_date)
        if data_current is not None:
            data_hold = data_current
        if data_before is None or data_current is None:
            print(f'{current_date} is skipped')
            current_date += timedelta(days=1)
            continue
        for stock in stocks:
            last_week_price = data_before['Close'].get(stock, None)
            current_price = data_current['Close'].get(stock, None)
            a.make_decision(current_price,last_week_price,stock)
        
        print(f'{current_date} done')
        # Move to the next day
        current_date += timedelta(days=1)
    
    a.get_holdings(data_hold)
    
    
    a.close_db_connection()



if __name__ == "__main__": 
    # print('High speed trading Emulator')
    stocks_list = set()
    with open('stocks_list.csv','r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for i,row in enumerate(csv_reader):
            stocks_list.add(row[0])
    start_time = '2025-02-10'
    end_time = '2025-02-13'

    if stocks_list:
        start(stocks_list,start_time,end_time)
