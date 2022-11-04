#aws lambda code for 
#How to Make a Chatbot Using Amazon Lex and AWS Lambda (Python) | Conversational AI Part 2
# https://youtu.be/W6T-RFei6SY
import json
import datetime
import time

def validate(slots):

    valid_cities = ['mumbai','delhi','banglore','hyderabad']

    if not slots['Location']:
        print("Inside Empty Location")
        return {
        'isValid': False,
        'violatedSlot': 'Location'
        }        

    if slots['Location']['value']['originalValue'].lower() not in  valid_cities:
        
        print("Not Valide location")

        return {
            'isValid': False,
            'violatedSlot': 'Location',
            'message': f'We currently  support only {", ".join(valid_cities)} as a valid destination.?',
        }


    if not slots['CheckInDate']:

        return {
        'isValid': False,
        'violatedSlot': 'CheckInDate',
    }

    if not slots['Nights']:
        return {
        'isValid': False,
        'violatedSlot': 'Nights'
    }

    return (
        {'isValid': True}
        if slots['RoomType']
        else {'isValid': False, 'violatedSlot': 'RoomType'}
    )
    
def lambda_handler(event, context):
    
    # print(event)
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event['invocationSource'])
    print(slots)
    print(intent)
    validation_result = validate(event['sessionState']['intent']['slots'])

    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            
            return (
                {
                    "sessionState": {
                        "dialogAction": {
                            'slotToElicit': validation_result['violatedSlot'],
                            "type": "ElicitSlot",
                        },
                        "intent": {'name': intent, 'slots': slots},
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": validation_result['message'],
                        }
                    ],
                }
                if 'message' in validation_result
                else {
                    "sessionState": {
                        "dialogAction": {
                            'slotToElicit': validation_result['violatedSlot'],
                            "type": "ElicitSlot",
                        },
                        "intent": {'name': intent, 'slots': slots},
                    }
                }
            )

        else:
            return {
                "sessionState": {
                    "dialogAction": {"type": "Delegate"},
                    "intent": {'name': intent, 'slots': slots},
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    'name': intent,
                    'slots': slots,
                    'state': 'Fulfilled',
                },
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Thanks, I have placed your reservation",
                }
            ],
        }