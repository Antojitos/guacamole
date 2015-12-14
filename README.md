# guacamole ![Build Status](https://travis-ci.org/Antojitos/guacamole.svg?branch=master)

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


## Deployment

Before start to deploying you need to have root access into a remote
server using SSH with a public key.

Install [ansible](<http://docs.ansible.com/ansible/intro_installation.html>) and run:

```shell
cp deploy/hosts.example hosts
vim hosts # add your remote server
ansible-playbook -i hosts deploy/site.yml
```
