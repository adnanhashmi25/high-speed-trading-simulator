import yfinance as yf
from datetime import datetime, timedelta
import contextlib
import os
import psycopg2
import xlsxwriter

class Stock(object):
    
    def __init__(self):
        self.stock_data = {}
        self.capital_counter = 0
        self.table_name = 'trade_log'
        self.connect_to_db()
        # create new table every time the object is called
        self.create_trade_table()
        
    def connect_to_db(self):
        self.conn = psycopg2.connect(
            dbname="stock_trading_db", user="postgres", password="password", host="localhost", port="5432"
        )
    
    def create_trade_table(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS trade_log")
        cursor.execute(f'''
            CREATE TABLE {self.table_name} (
                id SERIAL PRIMARY KEY,
                symbol TEXT,
                date DATE,
                quantity INT,
                action TEXT,
                price DECIMAL,
                capital_counter DECIMAL
            )''')
        self.conn.commit()
        cursor.close()
    
    def insert_trade_record(self, symbol,val,action,price):
        cursor = self.conn.cursor()
        self.capital_counter = round(sum(value[1] for value in self.stock_data.values()),2)
        cursor.execute(f'''
            INSERT INTO {self.table_name} (symbol, date, quantity,action, price,capital_counter)
            VALUES (%s, %s, %s,%s, %s,%s)''', (symbol, self.date, val,action, price, self.capital_counter))
        self.conn.commit()
        cursor.close()

    def close_db_connection(self):
        self.conn.close()

    # Fetch stock data for the past week
    def last_week_stock_data(self,stocks,st):
        start_date = st - timedelta(days=7)
        end_date = start_date + timedelta(days=1)
        with open(os.devnull, "w") as f, contextlib.redirect_stderr(f):
            data = yf.download(stocks, start=start_date, end=end_date, interval='1d')
        if data.empty:
            return None
        return data
    
    def get_current_data(self,stocks,st):
        self.date = st
        start_date = st
        end_date = start_date + timedelta(days=1)
        #Redirect stderr to suppress "possibly delisted" messages
        with open(os.devnull, "w") as f, contextlib.redirect_stderr(f):
            data = yf.download(stocks, start=start_date, end=end_date, interval='1d')
        if data.empty:
            return None
        return data
    
    def make_decision(self,last_week_price,current_price,stock):
        last_week_price = round(last_week_price.values[0],2)  # Closing price 7 days ago
        current_price = round(current_price.values[0],2)
        price_change = ((current_price - last_week_price) / last_week_price) * 100
        if stock not in self.stock_data:
            self.stock_data[stock] = [0,0]
        if price_change <= -5:
            if self.stock_data[stock][0] < 0:
                self.stock_data[stock][0] += 1
                self.stock_data[stock][1] += current_price
            else:
                self.stock_data[stock][0] += 1
                self.stock_data[stock][1] -= current_price
            self.insert_trade_record(stock, 1,'BUY',current_price)
            return
        elif price_change >= 10:
            if self.stock_data[stock][0] <= 0:
                self.stock_data[stock][0] -= 1
                self.stock_data[stock][1] -= current_price
            else:
                self.stock_data[stock][0] -= 1
                self.stock_data[stock][1] += current_price
            self.insert_trade_record(stock,-1,'SELL',current_price)
            return
        else:
            return
        
    def get_holdings(self,current):
        cursor = self.conn.cursor()
        workbook = xlsxwriter.Workbook('holdings.xlsx',{'strings_to_numbers':True})
        header = ['Stock', 'Quantity', 'Average' , 'Current Value', 'Profit/Loss']
        ws1 = workbook.add_worksheet('Summary')
        cursor.execute('select symbol, sum(quantity), avg(price) from trade_log group by symbol')
        holdings = cursor.fetchall()
        row = 1
        sum_profit = 0
        for i in range(len(header)):
            ws1.write(0, i, header[i])
        for h in holdings:
            profit = 0
            curr_price = current['Close'].get(h[0], None)
            curr_price = round(curr_price.values[0],2)
            profit = h[1] * curr_price - h[1] * float(h[2])
            sum_profit += profit
            req = list(h) + [curr_price,profit]
            ws1.write_row(row, 0, req)
            row += 1  
        workbook.close()
        cursor.close()
        if sum_profit > 0:
            print(f'Congratulations you would have made {round(sum_profit,2)} profit on a total investment of {abs(self.capital_counter)}')
        else:
            print(f'You would have lost {round(abs(sum_profit),2)} on a total investment of {abs(self.capital_counter)}')
        print('\n\n Get Summary of Holdings in holdings.xlsx file in the same directory as this script')

    