import json
import boto3
import os

def lambda_handler(event, context):
    userId = event["user"]
    userData = event["profile"]
    avatar = userData["avatar"]
    if avatar is None:
        avatar = "https://i.imgur.com/tAmofRW.png"
    for item in userData:
        if userData[item] == "":
            userData[item] = " "

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( os.environ["USERS_TABLE"] )
    update_expr = 'SET fullname = :fullname, address = :address, phone = :phone, avatar = :avatar'
    response = table.update_item(
        Key={ "userId":userId },
        UpdateExpression=update_expr,
        ExpressionAttributeValues={
            ':fullname': userData['name'],
            ':address': userData['address'],
            ':phone': userData['phone'],
            ':avatar': avatar
        }
    )
    return (
        {"status": "ok", "msg": "profile updated"}
        if response['ResponseMetadata']['HTTPStatusCode'] == 200
        else {"status": "err", "err": "could not update profile"}
    )
