import sqlite3
import configparser

class DatabaseHelper:
    def __init__(self):
        config = configparser.ConfigParser()
        
        config.read("../config/config.ini")
        self.DB_NAME = config['DB']['DB_NAME']
        self.conn = sqlite3.connect(self.DB_NAME)
        self.create_tables()

    def create_tables(self):
        # Create tables if they don't exist
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                city TEXT PRIMARY KEY,
                temperature REAL,
                feels_like REAL
            )''')


    def insert_weather_data(self, city, temperature, feels_like):
        try:
            qry = '''INSERT OR REPLACE INTO weather_data(city, temperature, feels_like)
             VALUES(?, ?, ?)'''
            cur = self.conn.cursor()
            cur.execute(qry, (city, temperature, feels_like))
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting data for {city}: {e}") 
            raise

    def get_weather_data(self, city):
        try:
            qry = '''SELECT temperature, feels_like FROM weather_data WHERE city = ?'''
            cur = self.conn.cursor()
            cur.execute(qry, (city,))
            result = cur.fetchone()
            return {
            "temperature": result[0] if result else None,
            "feels_like": result[1] if result else None
        }
        except Exception as e:
             print(f"Error retrieving data: {e}")
             raise 
        

    
    def get_column_names(self, table_name):
        try:
            cur = self.conn.cursor()
            columns = [i[1] for i in cur.execute(f'PRAGMA table_info({table_name})')]
            return columns
        except Exception as e:
            print(f"Error retrieving column names: {e}")
            raise  
        
    def add_average_column(self):
        try:
            qry= '''ALTER TABLE weather_data ADD average REAL'''
            cur = self.conn.cursor()
            cur.execute(qry)
            self.conn.commit()
        except Exception as e:
             print( f"Error retrieving data: {e}")
             raise


    def update_average(self):
        try:
            qry = '''UPDATE weather_data
                 SET average = (temperature + feels_like) / 2;'''
            cur = self.conn.cursor()
            cur.execute(qry)
            self.conn.commit()
        except Exception as e:
             print(f"Error updating average values: {e}"
                   )
             

    def highest_temperature(self):
        try:
            qry = '''SELECT city, MAX(average) AS highest_average FROM weather_data;'''
            cur = self.conn.cursor()
            cur.execute(qry)
            result = cur.fetchone()
            return {
            "city_with_highest_average" : result[0],
            "highest_average_temperature" :result[1]
        }   
        except Exception as e:
             print(f"Error retrieving data: {e}")



