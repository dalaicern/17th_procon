# PROCON NAPROCK: 17th International Programming Contest example server

https://www.procon.gr.jp/wp-content/uploads/2025/06/NAPROCK_17th_International_Programming_Contest_ENGver.pdf


## Set up

```Shell
python3 -m venv procon
source ./procon/bin/activate
pip3 install -r requirements
```

## Running the server

1. Get a token passing your team name.

```Shell
curl -X 'POST' \
  'http://localhost:8000/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
      "name": "team name"
    }'
```

2. Get a problem using your token received from previous step.

```Shell
curl -s -X GET http://127.0.0.1:8000/problem \
     -H "Authorization: Bearer <your token>"
```


3. Submit your solution (not implemented yet)

```Shell
curl -X 'POST' \
  'http://localhost:8000/submit \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer <your token>"
  -d '{
    "ops": [
        {"x": 0, "y": 0, "n": 2},
        {"x": 2, "y": 2, "n": 2}
    ]
  }'
```

## Development

For now it can be only used for testing your program solutions. It will be fully development by 15 Nov. Till then, keep checking this repo.
