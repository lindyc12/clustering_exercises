from env import host, user, password
import env
import pandas as pd

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    
sql_query = '''
SELECT *
FROM properties_2017
        RIGHT JOIN (SELECT parcelid, MAX(transactiondate) AS transaction_date 
            FROM predictions_2017
                GROUP BY (predictions_2017.parcelid)) AS table2 USING (parcelid)
                    WHERE transaction_date < 2018;
'''
    
def get_zillow_data():
    df = pd.read_sql(sql_query, get_connection('zillow'))
    df = df.drop(columns='id')
    return df