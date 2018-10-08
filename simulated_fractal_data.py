#simulated-fractal- Data Generating Script - fractal_data
# Author - Julia You - 2018 - v1

import boto3, random, tqdm, time, botocore, uuid
from botocore.exceptions import ClientError
from tqdm import trange
from tqdm import tqdm

# Boto init
loadmin_session = boto3.Session(profile_name='loadmin')
db_c = loadmin_session.client('dynamodb')
db_r = loadmin_session.resource('dynamodb')

#------------------------------------------------------------------------------
def strTimeProp(start, end, format, prop):
   """Get a time at a proportion of a range of two formatted times.
   start and end should be strings specifying times formated in the
   given format (strftime-style), giving an interval [start, end].
   prop specifies how a proportion of the interval to be taken after
   start.  The returned time will be in the specified format.
   """
   stime = time.mktime(time.strptime(start, format))
   etime = time.mktime(time.strptime(end, format))
   ptime = stime + prop * (etime - stime)
   return time.strftime(format, time.localtime(ptime))
#------------------------------------------------------------------------------
def randomDate(start, end, prop):
   return strTimeProp(start, end, '%Y%m%d%H%M', prop)
#------------------------------------------------------------------------------
def d_table(): # define table configuration
   table_config={}
   ## starting provisioned throughput settings for each table
   table_config['ProvisionedThroughput'] = { 'ReadCapacityUnits' : 5, 'WriteCapacityUnits' : 5 }
   table_config['KeySchema'] = [
           {'AttributeName' : 'SN', 'KeyType' : 'HASH'}, \
           {'AttributeName' : 'TS', 'KeyType' : 'RANGE'}, \
   ]
   table_config['AttributeDefinitions'] = [
       {'AttributeName' : 'SN', 'AttributeType' : 'S'},\
       {'AttributeName' : 'TS', 'AttributeType' : 'S'},\
   ]
   table_config['TableName'] = 'simulated_fractal_data'

   return table_config
#------------------------------------------------------------------------------
def c_table (c): # create dynamo DB tables
   try:
       print ("INFO :: Creating %s Table....." % c['TableName'])
       db_r.create_table(**c)
       print("INFO :: Waiting for completion...")
       db_r.Table(c['TableName']).wait_until_exists()
   except botocore.exceptions.ClientError as e:
       if e.response['Error']['Code'] == "ResourceInUseException":
           print("INFO :: Table exists, deleting ....")
           db_r.Table(c['TableName']).delete()
           print( "INFO :: Waiting for delete..")
           db_r.Table(c['TableName']).wait_until_not_exists()
           c_table (c)
       else:
           print("Unknown Error")
#------------------------------------------------------------------------------
def p_table (stations, datapoints): # Populate Table
   with db_r.Table('simulated_fractal_data').batch_writer() as batch:
       for station in trange(stations, desc='Stations'):
           for datapoint in trange(datapoints, desc='Datapoints'):
               item = item_gen(station)
               batch.put_item(Item=item)
#------------------------------------------------------------------------------
def item_gen(SN): # Generate ITEM for a given serial number
   i={}
   i['SN'] = str(SN)
   i['TS'] = str(randomDate("201801010000", "201806302359", random.random()))
   i['payload'] = {}
   i['payload']["ChaSt"] = "Charging"
   i['payload']['DERTyp']= "ESS"
   i['payload']["Evt"]= "00111"
   i['payload']["Hz"]="60"
   i['payload']["KWAC"] = random.randrange(4000,5000)
   return i;
#------------------------------------------------------------------------------
if __name__ == "__main__":
   num_of_stations=10
   num_of_datapoints=100
   print("Re-creating fractal_data table,")
   table_config = d_table() # create table config.
   t_conf=d_table() # generate table config
   c_table(t_conf) # create table, with the above config
   p_table(num_of_stations, num_of_datapoints) # populate the table with X rows
   print("INFO :: Data Entry Complete")
