import time
import requests
import json
import uuid

#constants
RECONIFY_TRACKER = 'https://track.reconify.com/track'
RECONIFY_UPLOADER = 'https://track.reconify.com/upload'
RECONIFY_MODULE_VERSION = '1.0.4'

#private variables 
__appKey = None
__apiKey = None
__debug = False
__tracker = RECONIFY_TRACKER
__uploader = RECONIFY_UPLOADER
__user = {}
__session = ''
__sessionTimeout = ''
__trackImages = True

def __logInteraction(input, output, timestampIn, timestampOut, type):
    if __debug:
        print('Logging interaction')
    
    requestId = output.get("ResponseMetadata").get("RequestId")
    #body = ''
    #if 'body' in output:
    #    body = json.loads(output.get("body").read().decode('utf-8'))
    body = output.get("parsedBody")
    payload = {
        "reconify" :{
            "format": 'bedrock',
            "appKey": __appKey,
            "apiKey": __apiKey,
            "type": type,
            "version": RECONIFY_MODULE_VERSION,
        },
        "request": input,
        "response": {
            "requestId": requestId,
            "body": body
        },
        "user": __user,
        "session": __session,
        "sessionTimeout": __sessionTimeout,
        "timestamps": {
            "request": timestampIn,
            "response": timestampOut
        },
    }
    if __debug:
        print('Sending payload: ', payload)
    try:
        requests.post(__tracker, json=payload)
    except requests.exceptions.RequestException as err:
        if __debug:
            print('Send error: ', err)

    return

def __uploadImage(payload):
    if __debug:
        print('uploading image')
    
    try:
        requests.post(__uploader, json=payload)
    except requests.exceptions.RequestException as err:
        if __debug:
            print('upload error: ', err)
    return

def __logInteractionWithImageData(input, output, timestampIn, timestampOut, type):
    if __debug:
        print('Logging interaction with image data')

    requestId = output.get("ResponseMetadata").get("RequestId")
    #body = ''
    #if 'body' in output:
    #    body = json.loads(output.get("body").read().decode('utf-8'))
    body = output.get("parsedBody")
    data = body.get('artifacts')
    n = len(data)
    images = []
    randomId = str(uuid.uuid4())
    for i in range(n):
        images.append(
            {
                "filename": f"{randomId}-{timestampIn}-{i}.png",
                "seed": data[i].get("seed"),
                "finishReason": data[i].get("finishReason")
            }
        )

    payload = {
        "reconify" :{
            "format": 'bedrock',
            "appKey": __appKey,
            "apiKey": __apiKey,
            "type": type,
            "version": RECONIFY_MODULE_VERSION,
        },
        "request": input,
        "response": {
            "requestId": requestId,
            "body": {
                "images": images,
                "format": 'b64_json'
            }
        },
        "user": __user,
        "session": __session,
        "sessionTimeout": __sessionTimeout,
        "timestamps": {
            "request": timestampIn,
            "response": timestampOut
        },
    }
    if __debug:
        print('Sending payload: ', payload)
    try:
        requests.post(__tracker, json=payload)
    except requests.exceptions.RequestException as err:
        if __debug:
            print('Send error: ', err)    

    #send each image
    for i in range(n):
        __uploadImage({
        "reconify" :{
            "format": 'bedrock',
            "appKey": __appKey,
            "apiKey": __apiKey,
            "type": 'image_upload',
            "version": RECONIFY_MODULE_VERSION,
        },
        "upload": {
            "filename": images[i].get('filename'),
            "type": 'response-image',
            'data': data[i].get('base64'),
            'format': 'b64_json'
        }
        })

    return

def config (bedrock, appKey, apiKey, **options):
    global __appKey
    global __apiKey
    global __debug
    global __tracker
    global __uploader
    global __user
    global __session
    global __sessionTimeout
    global __trackImages

    __appKey = appKey
    __apiKey = apiKey
    if __appKey is None or __apiKey is None:
        raise Exception('An appKey and apiKey are required')
    #optional overides
    if 'debug' in options and options.get('debug') == True:
        __debug = True

    if 'tracker' in options:
        __tracker = options.get('tracker')

    if 'uploader' in options:
        __uploader = options.get('uploader')

    if 'trackImages' in options and options.get('trackImages') == False:
        __trackImages = False

    #override invoke_model
    bedrock.originalInvokeModel = bedrock.invoke_model
    def __reconifyInvokeModel(**kwargs):
        tsIn = round(time.time()*1000)
        response = bedrock.originalInvokeModel(**kwargs)
        tsOut = round(time.time()*1000)
        model = ''
        if 'modelId' in kwargs:
            model = kwargs.get('modelId')
        
        if model.startswith('anthropic.') or model.startswith('ai21.') or model.startswith('cohere.'):
            body = json.loads(response.get("body").read().decode('utf-8'))
            response["parsedBody"] = body
            __logInteraction(kwargs, response, tsIn, tsOut, 'chat')
        elif model.startswith('stability.'): 
            body = json.loads(response.get("body").read().decode('utf-8'))
            response["parsedBody"] = body
            __logInteractionWithImageData(kwargs, response, tsIn, tsOut, 'image')

        return response 
    bedrock.invoke_model = __reconifyInvokeModel 

    return

def setUser(user):
    global __user
    __user = user

def setSession(session):
    global __session
    __session = session

def setSessionTimeout(sessionTimeout):
    global __sessionTimeout
    __sessionTimeout = sessionTimeout