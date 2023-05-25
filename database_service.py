import harperdb
import pandas as pd
def db_connection():
    url="https://heatwave1-heatwave.harperdbcloud.com"
    username="heat_wave"
    password="heatwave@123"

    db=harperdb.HarperDB(
        url=url,
        username=username,
        password=password
        )
    return db


def insert_subscribers(db,Mail,City):
        SCHEMA="heatwave_repo"
        TABLE="subscribers"
        insert_data={
        "Mail":Mail,
        "City":City }

        return db.insert(SCHEMA,TABLE,[insert_data])

def check_subscribers(db,Mail,City):

    query=db.sql("select City,Mail from heatwave_repo.subscribers")
    df=pd.DataFrame(query,columns=["Mail","City"])
    flag=0
    for i in range(0,len(df)):
        if (df.loc[i,"Mail"]==Mail and df.loc[i,"City"]==City):
             flag=1
    return flag

    

# query=db.sql("select City,Mail from heatwave_repo.subscribers")

# df=pd.DataFrame(query,columns=["Mail","City"])
# query=pd.read_sql_query('''select mail,city from heatwave_repo.subscribers''',db)
# df=pd.DataFrame(query,columns=["Mail","City"])
# print(df)





