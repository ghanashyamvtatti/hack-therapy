def hello_world(request):
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
            'Access-Control-Allow-Methods': 'GET,POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('okay done', 204, headers)

   
    import flask
    import requests
    import json
    import sendgrid
    
    request_json = request.get_json()
    
    url = "https://sandbox.api.it.nyu.edu/class-roster-exp/classes?course_id=" + request_json["id"]
    header = {"Authorization": "Bearer 50075d77-fa22-30ae-a9e2-7dd3e527edee"}
    res = requests.get(url,headers=header).json()
    print (res)
    name = res[0]["instructor_name"].replace("," , " ").replace("." , " ")
    text = "Hi " + name + ", Students in your class are having a tought time coping up with course load. Kindly look into the matter."

    sg = sendgrid.SendGridAPIClient('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')
    data = {
      "personalizations": [
        {
          "to": [
            {
              "email": "sharmasuryateja@gmail.com"
            }
          ],
          "subject": "hacktherapy"
        }
      ],
      "from": {
        "email": "sambi97@gmail.com"
      },
      "content": [
        {
          "type": "text/plain",
          "value": text
        }
      ]
    }
    result = sg.client.mail.send.post(request_body=data)
    response = flask.jsonify("Success")
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.set( 'Access-Control-Allow-Headers', 'Content-Type')
    return response