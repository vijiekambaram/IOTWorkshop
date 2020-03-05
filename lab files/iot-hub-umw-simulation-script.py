import time
from datetime import datetime
import numpy as np
import pandas as pd

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
# CONNECTION_STRING = 
CONNECTION_STRING = "<replace the connection string here>"

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}, "eventTime": "{eventTime}"}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        df = pd.read_excel('Genset Log1.xls')


        # replace field that's entirely space (or empty) with NaN
        df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
        df.fillna('', inplace=True)

        for index, row in df.iterrows():
            ser_dict = row.to_dict()
            ser_dict['eventTime'] = str(datetime.now())
            msg_txt_formatted = str(ser_dict).replace("'",'"')
            print(msg_txt_formatted)

            message = Message(msg_txt_formatted)

            # Send the message.
            print( "Sending message: {}".format(message) )
            # client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(3)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )


def iothub_client_telemetry_more_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        df = pd.read_excel('Genset Log 1 - Modified.xlsx')


        # replace field that's entirely space (or empty) with NaN
        df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
        df.fillna('', inplace=True)

        df_count = iterate_df_count = len(df)
        # parameter to decide how many inputs needs to run in single request
        records_per_batch = 5

        record_start = 0
        record_end = records_per_batch

        while iterate_df_count > 0:
            print('simulation data is available')

            #     print(f'df_count - {df_count}')
            #     print(f'iterate_df_count - {iterate_df_count}')
            #     print(f'record_start - {record_start}')
            #     print(f'record_end - {record_end}')

            if record_end < df_count:
                temp_df = df[record_start:record_end].copy()
                temp_df['eventTime'] = str(datetime.now())
                data_dict = temp_df.to_dict(orient='records')
                msg_txt_formatted = str(data_dict).replace("'", '"')

            else:
                temp_df = df[record_start:].copy()
                temp_df['eventTime'] = str(datetime.now())
                data_dict = temp_df.to_dict(orient='records')
                msg_txt_formatted = str(data_dict).replace("'", '"')

            message = Message(msg_txt_formatted)
            # Send the message.
            print( "Sending message: {}".format(message) )
            print(f"No. of messages sent - {len(data_dict)}")

            # Message pushed to IoT Hub
            client.send_message(message)

            print("Message successfully sent")
            time.sleep(10)

            record_start = record_end
            record_end = record_end + records_per_batch

            iterate_df_count = iterate_df_count - records_per_batch

            print('- ' * 20)
        else:
            print('no data to simulate')

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )

    # to run the inputs one by one
    # iothub_client_telemetry_sample_run()

    # to run multiple inputs in one go
    iothub_client_telemetry_more_sample_run()
