import sys 
import json
import argparse
import os.path
import requests
from urllib.parse import urlparse
from datetime import datetime, timedelta

def jsonOutput(data):
    return json.dumps(data, sort_keys=True, indent=4)

def urlValidator(url):
    try:
        result = urlparse(url)
        return True
    except:
        return False

def getCommits(api, accessToken, projectId, branchName, sinceISO8601Format = None, outputFields = [
    'short_id', 'id', 'created_at',
    'title', 'message',
    'author_name', 'author_email', 'authored_date'
    'committer_name', 'committer_email', 'committed_date',
    ]):
    output = { "status": False, "error": 0, "errorMessage": None, "data": [] }
    apiURL = f"{api}/api/v4/projects/{projectId}/repository/commits"

    queryParams = {}
    queryParams['private_token'] = accessToken
    queryParams['ref_name'] = branchName
    if sinceISO8601Format:
        queryParams['since'] = sinceISO8601Format
    # https://www.w3schools.com/python/ref_requests_get.asp
    # output['data'] = json.loads(response.text)
    response = requests.get(apiURL, params=queryParams)
    #print(f"debug: {jsonOutput(json.loads(response.text))}")
    if response.status_code == 200:
        output['status'] = True
        try:
            for item in json.loads(response.text):
                outputItem = {}
                for field in outputFields:
                    if field in item:
                        outputItem[field] = item[field]
                output['data'].append(outputItem)
        except Exception as e:
            output['status'] = False
            output['error'] = -1
            output['errorMessage'] = str(e)

    return output

def getBranches(api, accessToken, projectId, outputFields = [
    'web_url', 'name',
    ]):
    output = { "status": False, "error": 0, "errorMessage": None, "data": [] }
    apiURL = f"{api}/api/v4/projects/{projectId}/repository/branches"

    queryParams = {}
    queryParams['private_token'] = accessToken
    queryParams['simple'] = 'true'
    # https://www.w3schools.com/python/ref_requests_get.asp
    # output['data'] = json.loads(response.text)
    response = requests.get(apiURL, params=queryParams)
    #print(f"debug: {jsonOutput(json.loads(response.text))}")
    if response.status_code == 200:
        output['status'] = True
        try:
            for item in json.loads(response.text):
                outputItem = {}
                for field in outputFields:
                    if field in item:
                        outputItem[field] = item[field]
                output['data'].append(outputItem)
        except Exception as e:
            output['status'] = False
            output['error'] = -1
            output['errorMessage'] = str(e)

    return output

def getProjects(api, accessToken, query = { 'simple': 'true', 'order_by': 'path' }, outputFields = [
    'id', 'created_at', 'web_url', 'http_url_to_repo', 'ssh_url_to_repo',
    'name', 'name_with_namespace',
    'path', 'path_with_namespace'
    ]):
    output = { "status": False, "error": 0, "errorMessage": None, "data": [] }
    apiURL = f"{api}/api/v4/projects"

    queryParams = {}
    queryParams['private_token'] = accessToken
    for key, value in enumerate(query):
        queryParams[key] = value

    # https://www.w3schools.com/python/ref_requests_get.asp
    # output['data'] = json.loads(response.text)
    response = requests.get(apiURL, params=queryParams)
    if response.status_code == 200:
        output['status'] = True
        try:
            for item in json.loads(response.text):
                outputItem = {}
                for field in outputFields:
                    if field in item:
                        outputItem[field] = item[field]
                output['data'].append(outputItem)
        except Exception as e:
            output['status'] = False
            output['error'] = -1
            output['errorMessage'] = str(e)

    return output
