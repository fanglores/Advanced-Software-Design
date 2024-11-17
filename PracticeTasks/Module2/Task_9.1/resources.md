# Resources list
## Open API Schema
Members:
- id: links schema to a specific model
- data: actual API Schema as a JSON

Responsibilities:
Store API Schema

## HTTP Request/Response
Members:
- id: hash of the request body (only for request)
- data: body of the request/response

Responsibilities:
Stores request/response data for further processing

## Source Code
Members:
- Source code: model source code

Responsibilities:
Stores model source code for generating OpenAPI schema if needed

## CRD
Members:
- data: CRD data

Responsibilities:
Store data for further model processing and deployment

## Cached Response
Members:
- id: hash of the response body
- datetime: timestamp of the cache creation
- data: body of the response

Responsibilities:
Stores cached response by hashed request

## Log File
Members:
- name: filename

Responsibilities:
Stores Log Entries

## Log Entry
Members:
- datetime: time of log creation
- severity: log severity level
- data: log string

Responsibilities:
Stores log data

## Manifest
Members:
- name: manifest name
- repoUrl: url to model source code in the repository
- modelType: model type
- modelClass: model class

Responsibilities:
Stores model data for creation of the docker container