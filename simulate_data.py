import boto3
import random
import json
import time

PUBLISH_INTERVAL = 1 # seconds
SWITCH_AIRCON_INTERVAL = 5 # seconds
NUMBER_OF_MESSAGES = 1
DELTA = 0.75

region = 'us-west-2'
access_key_id = ''
secret_access_key = ''

service = 'sns'

client = boto3.client(
        service, 
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )

def increaseTemperature(temp):
    return round(100*(temp+DELTA))/100

def decreaseTemperature(temp):
    return round(100*(temp-DELTA))/100

def switchAirCon(start_time):
    if (time.time() - start_time) >= SWITCH_AIRCON_INTERVAL:
        return True
    return False

def publish(msg, arn):
    return client.publish(
        TopicArn=arn,
        MessageStructure='json',
        Message = json.dumps({
            "default": "my default",
            "email": json.dumps(msg)
        })
    )

def main():     

    topic_ARNs = {
        'Thermos': 'arn:aws:sns:us-west-2:658401060424:test',
        'AirCon': 'arn:aws:sns:us-west-2:658401060424:AirCon'
    }    

    temp = 45
    airConditioningIsOn = 0    

    ain_con_start = time.time()
    for i in range(NUMBER_OF_MESSAGES):
        sender_id = 'sender_'+ str(int(random.random()*1000+1))

        if switchAirCon(ain_con_start):
            ain_con_start = time.time()
            airConditioningIsOn = 1 - (random.random()>=0.5)        

        if airConditioningIsOn==0: 
            airConditioningStatus = 'Off'
            temp = increaseTemperature(temp)
        else: 
            airConditioningStatus = 'On'
            temp = decreaseTemperature(temp)

        thermos_msg = {
            "sender_id": sender_id,        
            "temperature": temp
        }

        airCon_msg = {
            "sender_id": sender_id,        
            "airConditioningStatus": airConditioningStatus
        }

        print('Sending: ', json.dumps(thermos_msg))
        response = publish(thermos_msg, topic_ARNs['Thermos']) 

        print('Sending: ', json.dumps(airCon_msg))
        response = publish(airCon_msg, topic_ARNs['AirCon'])     

        time.sleep(PUBLISH_INTERVAL)

if __name__ == '__main__':
    main()