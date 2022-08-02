import json
import uuid
import boto3
import os

# status list
# -----------
# 100: open
# 110: payment-failed
# 120: paid
# 200: processing
# 210: shipped
# 300: delivered
# 500: cancelled
# 600: rejected

def lambda_handler(event, context):
    orderId = event["orderId"]
    address = event["shipping"]
    userId = event["user"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])

    response = table.get_item(
        Key={
            "orderId": orderId,
            "userId": userId
        },
        AttributesToGet=['orderStatus']
    )
    if 'Item' not in response:
        res = {"status": "err", "msg": "could not find order"}
        return res

    if response["Item"]["orderStatus"] >= 200:
        res = {"status": "err", "msg": "too late to update order"}
        return res

    update_expr = 'SET address = :address'
    response = table.update_item(
        Key={"orderId": orderId, "userId": userId},
        UpdateExpression=update_expr,
        ExpressionAttributeValues={
            ':address': address
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {"status": "ok", "msg": "address updated"}
    else:
        return {"status": "err", "msg": "could not update address"}
