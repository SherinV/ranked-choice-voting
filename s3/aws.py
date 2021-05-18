import boto3
import pandas as pd


s3 = boto3.client("s3",\
                  region_name='us-east-1',\
                  aws_access_key_id='',\
                  aws_secret_access_key='')

response = s3.list_objects(Bucket="rcvproject",\
Prefix="10Kelections/")



def test_fun():
    df_list = []    
    for file in response["Contents"][1:]:
        obj = s3.get_object(Bucket="rcvproject", Key=file["Key"])        
        obj_df = pd.read_csv(obj["Body"])        
        df_list.append(obj_df)    
        df = pd.concat(df_list)    
    return df


df=test_fun()

df.to_csv("new_master.csv",index=False)
