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
    
    from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset
    
    request_json = request.get_json()
    cash = request_json["money"]
    print (cash)
    
    source_keypair = Keypair.from_secret("xxxxxxxxxxxxxxxxxxxxxxxxxxx")
    server = Server(horizon_url="https://horizon-testnet.stellar.org")
    source_account = server.load_account(account_id=source_keypair.public_key)
    
    base_fee = server.fetch_base_fee()
    path = []
    
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .append_path_payment_op(destination="GDYC7QBANT5HCU3CAJVYDBDMGKUMOSWRULN737XRSDV56HIGSIUEQ6WJ", send_code="XLM", send_issuer=None, send_max="100", dest_code="USD",
                          dest_issuer="GACN4CNWBINPRWT2YKXXMEIPIBL5PEJNSKEBNOGCCXDKZBE5M44YFNXB", dest_amount=str(cash), path=path)
        .set_timeout(30)
        .build()
    )
    transaction.sign(source_keypair)
    res = server.submit_transaction(transaction)
    print(res)
    import json
    import flask
    request_json = request.get_json()
    response = flask.jsonify("https://horizon-testnet.stellar.org/accounts/GDYC7QBANT5HCU3CAJVYDBDMGKUMOSWRULN737XRSDV56HIGSIUEQ6WJ")
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.set( 'Access-Control-Allow-Headers', 'Content-Type')
    return response