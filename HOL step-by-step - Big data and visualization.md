![Microsoft Cloud Workshop](https://github.com/vijiekambaram/IOTWorkshop/blob/master/media/tiger_analytics_logo.PNG 'Microsoft Cloud Workshop')

<div class="MCWHeader1">
Real Time Monitoring of IOT data
</div>

<div class="MCWHeader2">
Hands-on lab step-by-step
</div>

<div class="MCWHeader3">
March 2020
</div>



**Contents**

<!-- TOC -->

- [Real Monitoring of IOT data hands-on lab step-by-step](#iot-data-and-monitoring-hands-on-lab-step-by-step)
  - [Abstract and learning objectives](#abstract-and-learning-objectives)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Exercise 1: Register a Device to IOT Hub](#exercise-1-register-device)
  - [Exercise 2: Environment for Data Ingestion into IOT Hub](#exercise-2-environment-setup)  
  - [Exercise 3: Upload the Reference data into Blob](#exercise-3-data-upload)
  - [Exercise 4: Configure Stream Analytics Job](#exercise-4-stream-analytics-setup)
  - [Exercise 5: Start Stream Analytics Job](#exercise-5-start-stream-analytics)
  - [Exercise 6: Run the Ingestion code to push data to IOT Hub](#exercise-7-run-ingestion-code)
  - [Exercise 7: Login to PowerBI Online account](#exercise-8-power-bi-online)

<!-- /TOC -->

# Real Time Monitoring of IOT data hands-on lab step-by-step

## Abstract and learning objectives

This hands-on lab is designed to provide exposure to many of Microsoft's transformative line of business applications built using Microsoft big data and advanced analytics.

By the end of the lab, you will be able to show an end-to-end solution, leveraging many of these technologies, but not necessarily doing work in every component possible.

## Requirements

1. Microsoft Azure subscription must be pay-as-you-go or MSDN.

   - Trial subscriptions will not work.


3. Follow all the steps provided in [Before the Hands-on Lab](Before%20the%20HOL%20-%20Big%20data%20and%20visualization.md).

## Exercise 1: Register a Device to IOT Hub

1.	In the Azure Portal, type IOT Hub in Search box and Click on IOT Hub
2.	On the Left pane, Click on Shared Access Policies and click on iothubowner
    ![Copy SAS](media/exercise1_2.png)
 
    Copy the Primary Key and Store it in a Notepad, we will need this during Stream Analytics Input configuration
    ![Copy Primary Key](media/exercise1_2b.png)
		 
3.	On the Left pane scroll down and Click on IOT Devices to create an identity for device to ingest the data into IOT Hub. Click +New
  
    ![Create Identity](media/exercise1_3.png)
 

4.	Enter a Device ID and Click on Save
    ![Enter Device Id](media/exercise1_4.png)

 
5.	Click on gensetdevice 
    
    ![Click on device](media/exercise1_5.png)

6.	Copy the Primary Connection String and Store it in a Notepad. This is needed to update the connection string in the code that will run on a device.
 
    ![Copy Primary Connection String](media/exercise1_6.png)
   

## Exercise 2: Environment for Data Ingestion into IOT Hub

Duration: 20 minutes

In this exercise, you will set up the environment needed to run the ingestion code into IOT Hub

1.	Ensure Python 3.7+ is installed
2.	Download Python code from Lab Files
3.	Genset data will be emailed during the lab
4.	Open the Python code in the a Python Editor or Notepad++ and update the connection string

    ![Connection String](media/exercise2_4.png)

5.	Update the input file location in iothub_client_telemetry_more_sample_run function 

    ![File Location](media/exercise2_5.png)
  
6.	Ensure pandas, numpy, xlrd are installed. Else run the following commands.

	pip install pandas
	pip install numpy
	pip install xlrd

7.	Install the Azure IOT SDK.
	pip install azure-iot-device

## Exercise 3: Upload the Reference data into Blob

Duration: 10 minutes

In this exercise, you will upload the reference data into Blob. Download the device_reference_data from lab files to local.

1.	Go to the Storage Account and click on Container and Select iot-hub-asa
    ![Storage Container](media/exercise3_1.png)

2.	Select the device_reference_data.json from your local and Click on Upload
3.	Click on Advanced and enter Upload to Folder as iotreferencedata. Click on Upload
    ![Upload Container](media/exercise3_4.png)
 

## Exercise 4: Configure Stream Analytics Job

In this exercise, you will configure Stream Analytics - Input, Output and Query.

1.	Go to Stream Analytics resource that was created in Before HOL 

## Input Section
2.	Click on Inputs and then +Add Stream Input

    ![Stream Input](media/exercise4_2.png)
 
3.	Enter the Input Alias name as iot-hub-input
4.	Click Select IoT Hub from your subscriptions. If it doesn’t populate automatically, select Provide IoT Hub settings manually
5.	Enter/Select IOT Hub as iothubworkshopdemo and other details as below. Click on Save

    ![Select IOT Hub](media/exercise4_5.png)

6.	Click on +Add reference input and Select Blob Storage
7.	Enter Input alias as blob-input
8.	Click on Select Blob storage from your subscriptions
9.	Select the right Storage Account, Container, path pattern where the reference data resides. Click on Save. Path Pattern as  iotreferencedata/device_reference_data.json

    ![Select Storage Account](media/exercise4_9_1.png)

## Output Section 

10.	On the Left Pane, Click on Outputs and Click on +Add -> PowerBI. This is for real time monitoring.

    ![Select PowerBI Output](media/exercise4_10.png)

11.	Click on Authorize if there is already PowerBI Online account. Else Click on Sign Up using work account. 
12.	Once Authorized, enter the Output Alias as power-bi-output, select the Authentication Type as User Token
13.	Select My Workspace from drop down and enter dataset name as streamingData and table as streamingTable

    ![Select PowerBI Workspace](media/exercise4_13_1.png)

14.	Add another output blob-raw-output, to store the raw input without any transformations in Blob for batch reporting or analytics

15.	On the Left Pane, Click on Outputs and Click on +Add -> Blob storage

    ![Select Blob Output](media/exercise4_15.png)

16.	Enter Output alias as blob-raw-input
17.	Click on Select Blob storage from your subscriptions
18.	Select the right Storage Account, Container
19.	Give the path pattern as umw_iot_hub_raw_data_1/{datetime:yyyy}_{datetime:MM}_{datetime:dd}/{datetime:HH} where the data will get written. Click on Save.
20.	Similarly add one more output for storing a copy of aggregated data in Blob. Give the Output Alias as blob-agg-output and path pattern as umw_iot_hub_agg_data_1/{datetime:yyyy}_{datetime:MM}_{datetime:dd}/{datetime:HH} 

## Query Section

This is where the Business rules logic will be written and it is more of Query Language.

21.	From the Left Pane in Stream Analytics window, Click on Query.
22.	Copy the Query from lab files – Stream Analytics Query and paste in the Query editor.
23.	Click on Save Query.

## Exercise 5: Start Stream Analytics Job

Duration: 10 minutes

In this exercise, you will trigger the Stream Analytics Job. 

1.	On the Left Pane in Stream Analytics, Overview -> Start -> Job output start time as Now. Click on Start. This will take some time to start the Streaming job

    ![Start Streaming](media/exercise5_1.png)


## Exercise 6: Run the Ingestion code to push data to IOT Hub

In the Azure Portal, Click on Cloud Shell icon and it will open a Bash or Powershell Prompt depending on what we choose. Enter the command az extension add --name azure-cli-iot-ext in Cloud Shell

   ![Cloud Shell](media/cloud_shell.PNG)

1.	On your local machine, execute the Python code either using PyCharm or execute the command manually. Go to the location where Python code resides and enter the command python iot-hub-umw-simulation-script.py
2.	This will keep ingesting the data into IOT Hub for every 10 secs.

To view the messages from IOT Hub, from Azure Portal, go to Cloud Shell icon and enter the command 

az iot hub monitor-events --hub-name iot-hub-free-tier-f1 --device-id gensetdevice

![IOT Hub Message View](media/cloud_shell_message_view.PNG)


In the Azure portal, go to  IOT Hub resource, on the right pane scroll down to see Device to Cloud Messages

   ![Device to Cloud Messages](media/iot_hub_message_monitor.PNG)
	 
In the Azure portal, go to Stream Analytics resounce and on the right pane scroll down to Monitoring chart to see the arrival of incoming and output messages

   ![Stream Monitoring](media/stream_analytics_message_monitor.PNG)

## Exercise 7: Login to PowerBI account

Duration: 10 minutes 

1. Go  https://app.powerbi.com and login using the account created
2. From My Workspace, scroll down go to Datasets check if table got created

	![Dataset Check](media/power_bi_dataset_list.png)
	
3. Click on My Workspace to create a Dashboard. Give the dashboard name as iot-hub-demo

	![Create Dashboard](media/power_bi_create_dashboard.png)
	
	Dashboard is created
	
	![List Dashboard](media/power_bi_dashboard_list.png)
		
	
4. Click on the Dashboard and Add Tile. Select Custom Streaming Data and then Next

	![Add tile Dashboard](media/power_bi_add_tile1.png)

5. Click on the Dataset and then Next

      ![Add tile Dashboard](media/power_bi_select_ur_dataset.png)
	
6. Select Visualization Type as Card and Field, Add Value as AVG_POWER, Click Next

      ![Add tile Card](media/power_bi_add_tile1_card.png)

7. Give the Title as Power and Click Apply

      ![Add tile Card Details](media/power_bi_add_tile1_card_details.png)
	
8. Similary do for others Add Tile, Visualization Type as Card, Value as AVG_GFrq Frequency, Title as Generator Frequency

9. Add Tile, Visualization Type as Gauge, Value as AVG_VBAT, Minimum Value as ideal_min_VBAT, Maximum Value as ideal_max_VBAT, Target Value as target_VBAT, Title as Battery
10. Add Tile, Visualization Type as Gauge, Value as AVG_RPM, Minimum Value as ideal_min_RPM, Maximum Value as ideal_max_RPM, Target Value as target_RPM, Title as RPM
11. Add Tile, Visualization Type as Card, Value as AVG_Eclt Frequency, Title as Coolant Temperature
12. Add Tile, Visualization Type as Line Chart, Axis ingestion_timestamp, Values AVG_IL1, AVG_IL2, AVG_IL3, Time Window to Display 1 Minutes, Title as Line Current IL1 vs IL2 vs IL3
13. Add Tile, Visualization Type as Line Chart, Axis ingestion_timestamp, Values AVG_VG1, AVG_VG2, AVG_VG3, Time Window to Display 1 Minutes, Title as Phase to Ground Voltage
14. Add Tile, Visualization Type as Line Chart, Axis ingestion_timestamp, Values AVG_VG12, AVG_VG23, AVG_VG31, Time Window to Display 1 Minutes, Title as Phase to Phase Voltage
	
Final Dashboard would be

   ![Real Time Streaming](media/exercise7_2.png)
    
## After the hands-on lab

Duration: 10 minutes

In this exercise, attendees will deprovision any Azure resources that were created in support of the lab.

### Task 1: Delete resource group

1. Using the Azure portal, navigate to the Resource group you used throughout this hands-on lab by selecting **Resource groups** in the menu.

2. Search for the name of your research group and select it from the list.

3. Select **Delete** in the command bar and confirm the deletion by re-typing the Resource group name and selecting **Delete**.

You should follow all steps provided _after_ attending the Hands-on lab.
