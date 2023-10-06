import boto3
import random
import string
import io
import yaml
import sys

def retrievedata(clientid):
 region = 'us-west-2'
 client = boto3.client('appconfig',region_name=region)
 letters = string.ascii_letters
 random_string = ''.join(random.choice(letters) for i in range(10))
 application_id = 'govdvmm'
 environment_id = 'ei5a24p'
 client_id = clientid

 appconfig_client = boto3.client('appconfig', region_name=region)
 response = appconfig_client.list_configuration_profiles(ApplicationId=application_id)
 for profile in response['Items']:
     if profile['Name'] == client_id:
             configuration_profile_id=profile['Id']

 response = client.get_configuration(
         Application=application_id,
         Environment=environment_id,
         Configuration=configuration_profile_id,
         ClientId=client_id
 )
 configuration_data = response['Content'].read().decode('utf-8')
 config_data = configuration_data

 data = yaml.safe_load(config_data)

 return data


retrievedata("hlbackend")
#print(data)
#print(data["db"])
#print(data["db"]["db_replication_lag_threshold"])



