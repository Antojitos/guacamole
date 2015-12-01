# guacamole
Upload any file, get a URL back.

## Installation

`python setup.py install`

## Run the app

`python run.py`

or using [gunicorn](http://gunicorn.org/):

`gunicorn guacamole:app`

## API

### Post a file

#### Endpoint 
`POST /files/`
	
  Parameter   |    Type    | Required
------------- | ---------- | --------
    file      |    file    |   yes
    tags      |   string   |   no

#### Example

##### Request
`curl -F "file=@tests/fixtures/image.jpg" -F "tags=Mexican, food" 127.0.0.1:5000/files/`

##### Response
```json
{
  "upload_date": 1448922069,
  "hash": [
    "80e0ad2f295b80a4b248b2bb286368243e60d610"
  ],
  "name": "image.jpg",
  "tags": [
    "mexican",
    "food"
  ],
  "uri": "QVbB/OU2s/1atb/XtWn/8kwm/sT2w/image.jpg",
  "mime_type": "image/jpeg",
  "size": 39092
}
```

### Get a file

#### Endpoint 
`GET /files/{uri}`

  Parameter   |    Type    | Required
------------- | ---------- | --------
     uri      |   string   |   yes

#### Example

##### Request
`curl 127.0.0.1:5000/files/QVbB/OU2s/1atb/XtWn/8kwm/sT2w/image.jpg`


### Get a file's metadata

#### Endpoint 
`GET /files/{uri}/meta`

parameter|type|required
uri|string|yes

#### Example

##### Request
`curl 127.0.0.1:5000/files/QVbB/OU2s/1atb/XtWn/8kwm/sT2w/image.jpg/meta`

##### Response
```json
{
  "upload_date": 1448922069,
  "hash": [
    "80e0ad2f295b80a4b248b2bb286368243e60d610"
  ],
  "name": "image.jpg",
  "tags": [
    "mexican",
    "food"
  ],
  "uri": "QVbB/OU2s/1atb/XtWn/8kwm/sT2w/image.jpg",
  "_id": {
    "$oid": "565ccbd54d88a005130bc72f"
  },
  "mime_type": "image/jpeg",
  "size": 39092
}
```

## Tests

`python setup.py test`