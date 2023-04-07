import requests
import json
from datetime import datetime, timedelta
import time
import argparse

# Warning: running the command below will load data to FeatureBase from the first Nest device you have access to indefinitely 
# Example cli command:
# python nest_ingest.py --project_id <> --access_token <> --refresh_token <> --client_id <> --client_secret <> --fb_user <> --fb_pw <> --fb_db <>

class nestConn():
    """This class is used to make connection to Nest devices
    """
    def __init__(self, project_id, token, refresh_token=None, client_id=None, client_secret=None):
        """Initialize class

        Args:
            project_id (string): Nest project id
            token (string): Nes access token
            refresh_token (string, optional): Nest refresh token if you want to run for a long period of time. Defaults to None.
            client_id (string, optional): client id to use refresh token. Defaults to None.
            client_secret (string, optional): client secret to use refresh token. Defaults to None.
        """
        self.project_id=project_id
        self.token=token
        self.refresh_token=refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = {
                            'Content-Type': 'application/json',
                            'Authorization': self.token,
                        }

    def renew_token(self):
        """generate a new token using the refresh token
        """
        params = (
            ('client_id', self.client_id),
            ('client_secret', self.client_secret),
            ('refresh_token', self.refresh_token),
            ('grant_type', 'refresh_token'),
        )

        response = requests.post('https://www.googleapis.com/oauth2/v4/token', params=params)

        response_json = response.json()
        access_token = response_json['token_type'] + ' ' + response_json['access_token']
        self.token = access_token
        self.headers = {
                            'Content-Type': 'application/json',
                            'Authorization': self.token,
                        }

    def print_token(self):
        """ print current token"""
        print(self.token)


    def get_devices(self):
        """Get all of the devices in your nest project

        Returns:
            List: List of devices under your nest project
        """
        url_get_devices = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/' + self.project_id + '/devices'
        response = requests.get(url_get_devices, headers=self.headers)

        return response.json()

    def get_device_stats(self,device_name):
        """Get the device stats for a single nest device

        Args:
            device_name (string): device name

        Returns:
            json: all stats for the passed device
        """
        url_get_device = 'https://smartdevicemanagement.googleapis.com/v1/' + device_name
        iso_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        response = requests.get(url_get_device, headers=self.headers)
        response_json = response.json()
        response_json['req_time'] = iso_date
        return response_json

class featurebaseConn():
    """This class is used to make a connection to FeatureBase Cloud
    """
    def __init__(self, username, password, api_version='v2', database=None):
        self.username=username
        self.password=password
        self.database=database
        self.api_version=api_version
        self.token=self.featurebase_authenticate()

    def featurebase_authenticate(self):
        """A helper function to retrieve an OAuth 2.0 token 'IdToken' which will be
            used to make authenticated HTTP API calls. Returns the token
        """

        # Send HTTP POST request
        print("Generating new FeatureBase Token")
        response = requests.post(
            url  = "https://id.featurebase.com",
            json = { 'USERNAME' : self.username, 'PASSWORD' : self.password })

        # Check for a HTTP 200 OK status code to confirm success.
        if response.status_code != 200:
            raise Exception(
            "Failed to authenticate. Response from authentication service:\n" +
            response.text)

        # On a successful authentication, you should retrieve the IdToken located in
        # the response at 'AuthenticationResult.IdToken'. This will be needed for any
        # further API calls.
        json  = response.json()

        token = json['AuthenticationResult']['IdToken']
        self.token=token
        return token

    def use_database(self,database):
        """Set the database to use with the database id

        Args:
            database (string): database id
        """
        self.database=database

    def run_query(self,query):
        """run a sql query against the database in use

        Args:
            query (string): SQL query to execute

        Returns:
            json: SQL response
        """

        url  = f'https://query.featurebase.com/{self.api_version}/databases/{self.database}/query/sql'
        body = query.encode('utf-8')
        headers = {"Content-Type": "text/plain",
            "Authorization": f'Bearer {self.token}'}
        
        response = requests.post(url,headers=headers,data=body)
        if response.status_code != 200:
            print(response.text)

        # Check if schema exists in the response, which indicates success. Exit if error discovered
        try:
            response.json()['schema']
        except KeyError:
            print(f'Some Issue Occurred: \n {response.json()}')
            exit()

        # Check if errors exist in in the response, which indicates errors. Exit if error discovered
        try:
            response.json()['error']
        except KeyError:
            print(f'Query Executed!')
        else:
            print(f'Some Issue Occurred: {response.json()}')
            exit()
        return response.json()



if __name__ == "__main__":
    """Enable CLI runs of this script to constantly (if the refresh token is passed) load nest data into a FeatureBase database
    """

    # Add command line args for nest and featurebase
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_id', help='Nest Project ID', type=str, required=True)
    parser.add_argument('--access_token', help='Nest access token for authz', type=str, required=True)
    #Optional nest args but all must be passed or none. To improve by enforcing later
    parser.add_argument('--refresh_token', help='Nest refresh token used to generate new access tokens', type=str, required=False)
    parser.add_argument('--client_id', help='Nest client ID used to generate new access tokens', type=str, required=False)
    parser.add_argument('--client_secret ', help='Nest client secret used to generate new access tokens', type=str, required=False)

    parser.add_argument('--fb_user', help='FeatureBase username (email)', type=str, required=True)
    parser.add_argument('--fb_pw', help='FeatureBase password', type=str, required=True)
    parser.add_argument('--fb_db', help='FeatureBase database id', type=str, required=True)
    args = parser.parse_args()

    # Create a start time to track for token refreshes
    start_time=datetime.now()

    # if the refresh token is passed, create a connection to nest using it
    if args.refresh_token:
        conn = nestConn(args.project_id, args.access_token, args.refresh_token, args.client_id, args.client_secret)
        conn.renew_token()
    else:
        conn = nestConn(args.project_id, args.access_token)

    # get first device to get stats from    
    devices = conn.get_devices()
    device_0_name = devices['devices'][0]['name']

    #Create featurebase connection
    fb_conn = featurebaseConn(args.fb_user,args.fb_pw)
    fb_conn.use_database(args.fb_db)
    
    #Continuously run to stream data
    while 1==1:
        #After 55 minutes of running, get a new token before the old expires. this can only be done if a refresh token is passed
        if datetime.now() >= (start_time+ timedelta(minutes=55)) and not(conn.refresh_token is None):
            start_time=datetime.now()
            conn.renew_token()
            conn.print_token()
            fb_conn.featurebase_authenticate()
        #Get device stats
        device_stats = conn.get_device_stats(device_0_name)
        # Create BULK INSERT statment to load data
        sql = f'''BULK INSERT INTO gt-nest-thermo (
            _id, 
            display_name,
            device_type,
            device_status,
            fan_timer_mode,
            thermostat_mode,
            eco_mode,
            eco_heat_max_cel,
            eco_cool_min_cel,
            hvac_status,
            temp_display_unit,
            therm_heat_max_cel,
            therm_cool_min_cel,
            ambient_humidity_pct,
            ambient_temp_cel,
            measurement_ts,
            ambient_temp_far
            )
            MAP (
            '$["req_time"]' TIMESTAMP,
            '$["type"]' STRING,
            '$["traits"]["sdm.devices.traits.Humidity"]["ambientHumidityPercent"]' INT,
            '$["traits"]["sdm.devices.traits.Connectivity"]["status"]' STRING,
            '$["traits"]["sdm.devices.traits.Fan"]["timerMode"]' STRING,
            '$["traits"]["sdm.devices.traits.ThermostatMode"]["mode"]' STRING,
            '$["traits"]["sdm.devices.traits.ThermostatEco"]["mode"]' STRING,
            '$["traits"]["sdm.devices.traits.ThermostatEco"]["heatCelsius"]' DECIMAL(6),
            '$["traits"]["sdm.devices.traits.ThermostatEco"]["coolCelsius"]' DECIMAL(6),
            '$["traits"]["sdm.devices.traits.ThermostatHvac"]["status"]' STRING,
            '$["traits"]["sdm.devices.traits.Settings"]["temperatureScale"]' STRING,
            '$["traits"]["sdm.devices.traits.ThermostatTemperatureSetpoint"]["heatCelsius"]' DECIMAL(6),
            '$["traits"]["sdm.devices.traits.ThermostatTemperatureSetpoint"]["coolCelsius"]' DECIMAL(6),
            '$["traits"]["sdm.devices.traits.Temperature"]["ambientTemperatureCelsius"]' DECIMAL(6),
            '$["parentRelations"][0]["displayName"]' STRING
            )
            TRANSFORM(
            CAST(@0 as STRING),
            @14,
            @1,
            @3,
            @4,
            @5,
            @6,
            @7,
            @8,
            @9,
            @10,
            @11,
            @12,
            @2,
            @13,
            @0,
            (@13*9/5)+32)
            FROM '{json.dumps(device_stats)}'
            WITH
            BATCHSIZE 10000
            FORMAT 'NDJSON'
            INPUT 'STREAM'
            ALLOW_MISSING_VALUES;
            '''
        # Load data
        result = fb_conn.run_query(sql)
        print(result)
        # Rest 6 seconds as google limits device info to 10 QPM: https://developers.google.com/nest/device-access/project/limits
        time.sleep(6)