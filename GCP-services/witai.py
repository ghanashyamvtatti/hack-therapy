from wit import Wit
import random
import json
import flask
import requests
from twilio.rest import Client

# {'document_tone': {'tones': [{'score': 0.597205, 'tone_id': 'sadness', 'tone_name': 'Sadness'}, {'score': 0.588447, 'tone_id': 'fear', 'tone_name': 'Fear'}]}}

client = Wit("xxxxxxxxxxxxxxxxxxxxxxxxx")
intent_action_map = {
    'greet': ['Hi. How are you doing today?', 'How can I support you today?', 'Hello. How can I help you today?'],
    'feeling': ["I'm sorry to hear that. Would you like to tell me about it?",
                "What's going on?",
                "What's bothering you?",
                "What's on your mind?"],
    'tipp_prompt': ["I'm here for you. If you're interested, we could try some relaxation techniques.",
                    "Would you like to try out some relaxation techniques?"],
    'tipp': [
        "You could try holding your breath and putting your face in a bowl of cold water or holding a cold pack on your eyes and cheeks for at least 30 seconds. Did that help?",
        "Try to engage in intensive exercise, even if it's only for a short amount of time. Try running, walking at a fast pace, doing jumping jacks, etc. Did that help?",
        "Breathe deeply into your stomach. Try to slow down the pace of your inhales and exhales (on average, five to six breaths per minute). It helps if you try to breathe out more slowly than you breathe in. Did that help?",
        "While breathing deeply and slowly, deeply tense each of your body muscles one by one. Notice this tension and then breathe out and let go of the tension by completely relaxing your muscles. Pay attention to the difference in your body as you tense and let go of each muscle group. Did that help?"
    ],
    'tipp_follow_up': ["Would you like to try another relaxation technique?",
                       "How about another relaxation technique?"],
    'goodbye': ["I hope you feel better. Remember, I'm always here for you. Take care.",
                "It was lovely speaking with you. I'm here if you ever need me. See you!"],
    'default': ['Can you please elaborate so that I can help you better?'],
    'purpose': [
        'Sometimes, contributing to a cause greater than oneself gives people a sense of greater purpose. Would you like to make a donation towards the Australian bushfire relief?'],
    'amount': ["How much would you like to donate?"],
    'post_donate': [
        "Thank you for your generous donation. You can follow this [link](https://horizon-testnet.stellar.org/accounts/GDYC7QBANT5HCU3CAJVYDBDMGKUMOSWRULN737XRSDV56HIGSIUEQ6WJ) to see how your donation is making a difference"]
}


def handle_intents(request_json):
    message = request_json['message']
    witai_resp = get_witai_resp(message)
    print(witai_resp)
    context = update_context(request_json['context'], witai_resp)
    if message.lower() == 'bob! i am your father!':
        return {'message': 'Noooooooooooooooooooooooooooo!!!', 'context': context}

    if 'intent' not in witai_resp:
        witai_resp['intent'] = 'default'
    if 'is_issue' in context:
        witai_resp['intent'] = 'tipp_prompt'
        del context['is_issue']
        context['tipp_confirm'] = True

    if 'entities' in witai_resp and 'amount_of_money' in witai_resp['entities']:
        witai_resp['intent'] = 'post_donate'
        url = 'https://us-central1-neural-sunup-253704.cloudfunctions.net/stellaranchorpay'
        myobj = {'money': witai_resp['entities']['amount_of_money']}
        requests.post(url, json=myobj)
    if 'entities' in witai_resp and 'purpose' in witai_resp['entities']:
        # Start purpose flow
        context['donate_prompt'] = True
        witai_resp['intent'] = 'purpose'

    if 'intent' in witai_resp and witai_resp['intent'] == 'feeling':
        context['is_issue'] = True

    if witai_resp['intent'] == 'affirmation':
        if 'tipp_confirm' in context:
            if witai_resp['entities']['yes_no'] == "Yes":
                witai_resp['intent'] = 'tipp'
            else:
                witai_resp['intent'] = 'goodbye'
                if 'topic' in context and context['topic'] == 'academics' and 'courses' in context:
                    send_mail(context['courses'])
            del context['tipp_confirm']
        elif 'donate_prompt' in context:
            if witai_resp['entities']['yes_no'] == "Yes":
                witai_resp['intent'] = 'amount'
            else:
                witai_resp['intent'] = 'goodbye'
            del context['donate_prompt']
        else:
            witai_resp['intent'] = 'tipp_follow_up'
            context['tipp_confirm'] = True

    if message != "" and (witai_resp['intent'] == 'feeling' or witai_resp['intent'] == 'tipp_prompt'):
        severity = int(get_emotion(message))
        if severity == 2:
            # Send memes and music
            l = ["https://www.scoopify.org/wp-content/uploads/2019/06/cheer-up-meme-1024x576.jpg",
                 "https://i.pinimg.com/originals/1c/3c/df/1c3cdfc6d19f4bc0810865d9dacdc238.jpg",
                 "https://i.pinimg.com/originals/44/92/f0/4492f0adf5f9da1414cc6551b9e77919.jpg",
                 "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-selfie-meme-1546529212.png?crop=1.00xw:0.843xh;0,0.0218xh&resize=480:*"]
            return {"message": "Hope this cheers you up!",
                    "context": {"memes": random.choice(l), "music": "https://www.youtube.com/watch?v=lFcSrYw-ARY"}}

        elif severity == 3 or ('entities' in witai_resp and 'suicidal' in witai_resp['entities']):
            # Alert emergency contact
            print("Severeity heavy anthe anta")
            account_sid = 'xxxxxxxxxxxxxxxxxxxx'
            auth_token = 'xxxxxxxxxxxxxxxxxxx'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_='+xxxxxxxxxx',
                body="Your friend isn't feeling well, please take care of them.",
                to='+xxxxxxxxxxx'
            )
            print(message.sid)
            return {"message": "Please take care! I strongly urge you to consult a Counselor", "context": context}
    return {'message': random.choice(intent_action_map[witai_resp['intent']]), 'context': context}


def get_witai_resp(message):
    witai_resp = {}
    entities = {}
    if message == '':
        witai_resp['intent'] = 'greet'
        return witai_resp
    resp = client.message(message)
    for key, val in resp['entities'].items():
        if key == 'intent':
            witai_resp['intent'] = val[0]['value']
        else:
            entities[key] = val[0]['value']
    witai_resp['entities'] = entities
    return witai_resp


def update_context(context, witai_resp):
    if 'entities' in witai_resp:
        for key, val in witai_resp['entities'].items():
            if key == 'financial' or key == 'academics' or key == 'purpose':
                context['topic'] = key
    return context


def send_mail(courses):
    for course in courses:
        resp = requests.post('https://us-central1-neural-sunup-253704.cloudfunctions.net/getprofessor',
                             json={'id': course['value']})
        print(resp.text)


def get_emotion(message):
    API_ENDPOINT = "https://apis.paralleldots.com/v4/emotion"
    API_KEY = "xxxxxxxxxxxxxxxxxxxxxx"
    data = {"api_key": API_KEY, "text": message}
    r = requests.post(url=API_ENDPOINT, data=data).json()
    result = r['emotion']["Sad"] + r['emotion']["Angry"]
    if 0.4 <= result < 0.6:
        return "1"
    elif 0.6 <= result <= 0.7:
        return "2"
    elif result > 0.7:
        return "3"

    return "0"


def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('okay done', 204, headers)

    request_json = request.get_json()
    # return get_emotion(request_json["message"])

    response = handle_intents(request_json)
    response = flask.jsonify(response)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    return (response, 200, headers)
