import oauth2, json

def oauth_req(url, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key="btJN1gTmXhKcZpoTP4muM4Okx", secret="Qtdq5htnwJmL1f6mSHHOzpp1EUYywExKemVx4yKMEGhJxA25BY")
    token = oauth2.Token(key="481788327-tHoitX5IFtgI5rOdmAUdzxc9XdYuThz1pPikZO6v", secret="wGaYFm7RJhtQubTQLwjcVGRd5wXQp2prJAML4SIilHWNJ")
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

home_timeline = oauth_req('https://api.twitter.com/1.1/statuses/home_timeline.json')
test = json.loads(home_timeline)
print test
for x in test:
	print x
	print ""