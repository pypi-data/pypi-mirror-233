import boto3
import random
import string
import io
import yaml
import sys


# Specify the AWS region
region = 'us-west-2'
# Initialize the AppConfig client
client = boto3.client('appconfig',region_name=region)
def generate_random_string(length):
    # Get all the ASCII letters in lowercase and uppercase
    letters = string.ascii_letters
    # Randomly choose characters from letters for the given length of the string
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string
  
def get_appconfig_configuration(application_id, environment_id, configuration_profile_id,client_id):
    try:
        response = client.get_configuration(
            Application=application_id,
            Environment=environment_id,
            Configuration=configuration_profile_id,
            ClientId=client_id
        )

        # Extract the configuration data from the response
        configuration_data = response['Content'].read().decode('utf-8')

        return configuration_data

    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def get_appconfig_profile_id(client_id, application_id, region):

    try:
        # Initialize the AppConfig client
        appconfig_client = boto3.client('appconfig', region_name=region)

        # List all configuration profiles
        response = appconfig_client.list_configuration_profiles(ApplicationId=application_id)

        # Iterate through the profiles and find the one with the matching name
        for profile in response['Items']:
            if profile['Name'] == client_id:
                return profile['Id']

        # Return None if no matching profile is found
        return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None





# Replace with your AppConfig application, environment, and configuration profile IDs
random_string = generate_random_string(10)
application_id = 'govdvmm'
environment_id = 'ei5a24p'
#client_id = sys.argv[1]
client_id = 'hlbackend'
configuration_profile_id = get_appconfig_profile_id(client_id, application_id, region)

if configuration_profile_id is not None:
    print(f"Configuration Profile ID for {client_id}: {configuration_profile_id}")
else:
    print(f"No configuration profile with the name '{client_id}' found.")

config_data = get_appconfig_configuration(application_id, environment_id, configuration_profile_id, client_id)
# Example usage: generate a random string of length 10
if config_data:
#    print(f"{config_data.decode('utf-8')}")
#     print(f"{config_data}")
     print("data ready")
else:
    print("Failed to retrieve AppConfig configuration.")

data = yaml.safe_load(config_data)
print(data)
print(data["db"])
print(data["db"]["db_replication_lag_threshold"])
