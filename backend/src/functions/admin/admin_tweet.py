# -*- coding: utf-8 -*-

import json
import boto3
import base64
import urllib
import urllib2
import os

access_key = os.environ["TWITTER_ACCESS_TOKEN"]
access_secret = os.environ["TWITTER_TOKEN_SECRET"]
twitter_api = os.environ["TWITTER_API"]


# ToDo: Fix bugs
def authenticate():
    auth_url = f'{twitter_api}oauth2/token'
    token = f'{access_key}:{access_secret}'
    b64_encoded_key = base64.b64encode(token)
    auth_headers = {
        'Authorization': f'Basic {b64_encoded_key}',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }

    auth_data = "grant_type=client_credentials"
    req = urllib2.Request(auth_url, auth_data, auth_headers)
    try:
        res = urllib2.urlopen(req).read()
    except Exception as e:
        res = str(e)
    return res


#todo: tweet!
# this code is very buggy. its not working yet.
def tweet(token, msg):
    #todo: get tweet-id
    tweetId = ""
    client=""

    #write stats
    dynamodb = boto3.client('dynamodb')
    '''
    return {\'msg\': \'please check that action\'''}
    
    response = dynamodb.put_item(
        TableName = 'TODO: PLEASE_CHECK',
        Item={
            'tweetId': tweetId,
            'msg': msg
        }
    )
    '''
    try:
      response = dynamodb.updateItem(
          TableName = 'TODO: PLEASE_CHECK',
          Item={
              'tweetId': tweetId,
              'msg': msg
          }
      )
    except:
      pass

    #try 5
    test = dynamodb.select_item(
        TableName="DVSA-TWEETER-DB",
        Key={
            'tweetId': tweetId,
            'msg': msg
        }
    )


    #try 6
    response = client.get_item(
        TableName="DVSA-TWEETER-DB",
        Key={
            'tweetId': tweetId,
            'msg': msg
        }
    )
    item = response['Item']

    return response


def lambda_handler(event, context):
    key_secret = f'{access_key}:{access_secret}'.encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    access_token = json.loads(authenticate())["access_token"]

    auth_header = {'Authorization': f'Bearer {access_token}'}

    action = event['api']
    url = f'{twitter_api}{action}'

    data = event["data"] if "data" in event and event["data"] != "" else None
    req = urllib2.Request(url, data=data, headers=auth_header)

    try:
        res = urllib2.urlopen(req).read()

        try:
            if event["action"] == "tweet":
                tweet(res["token"], event["msg"])
        except:
            pass

    except Exception as e:
        res = str(e.reason)

    return res
