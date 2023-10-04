# gitlab-api-helper

This is a tool that calls the Gitlab API. It can query the list of projects, list branches of a specific project, and, after specifying the project and branch name, display the commit log.

# Installation

```
% pip install gitlab-api-helper
```

---

# Gitlab Setup

## Prepare the AccessToken

### Add a personal access token

https://gitlab.example.com/-/profile/personal_access_tokens

- read_api
- read_user
- read_repository

### Invite members 

- Select a role
  - Reporter

---

# Usage

```
% gitlab-api-helper --api https://gitlab.example.com/
{
    "info": [
        "config file not found: .env"
    ],
    "result": {
        "data": [],
        "error": 0,
        "errorMessage": null,
        "status": true
    },
    "version": "1.0.0"
}
```

## Projects

```
% gitlab-api-helper --api https://gitlab.example.com --apiAccessToken 'glpat-XXXXXXXXXXXXX'
{
    "info": [
        "config file not found: .env"
    ],
    "result": {
        "data": [
            {
                "created_at": "2023-10-03T00:00:00.000+08:00",
                "http_url_to_repo": "https://gitlab.example.com/web/test.git",
                "id": 179,
                "name": "test",
                "name_with_namespace": "web / test",
                "path": "test",
                "path_with_namespace": "web/test",
                "ssh_url_to_repo": "git@gitlab.example.com:web/test.git",
                "web_url": "https://gitlab.example.com/web/test"
            },
            ...
        ],
        "error": 0,
        "errorMessage": null,
        "status": true
    },
    "version": "1.0.0"
}
```

## Branches

```
% gitlab-api-helper --api https://gitlab.example.com --apiAccessToken 'glpat-XXXXXXXXX' --lookup branch --lookupProjectID 1
{
    "info": [
        "config file not found: .env"
    ],
    "result": {
        "data": [
            {
                "name": "alpha",
                "web_url": "https://gitlab.example.com/web/test/-/tree/alpha"
            },
            {
                "name": "develop",
                "web_url": "https://gitlab.example.com/web/test/-/tree/develop"
            },
            {
                "name": "main",
                "web_url": "https://gitlab.example.com/web/test/-/tree/main"
            }
        ],
        "error": 0,
        "errorMessage": null,
        "status": true
    },
    "version": "1.0.0"
}
```

## Commits

```
% gitlab-api-helper --api https://gitlab.example.com --apiAccessToken 'glpat-XXXXXXXXXXXX' --lookup commit --lookupProjectID 1 --lookupBranch develop
{
    "info": [
        "config file not found: .env",
        "sinceISO8601FormatDateValue: 2023-10-03T00:00:00.281140"
    ],
    "result": {
        "data": [
            {
                "author_email": "user@gitlab.example.com",
                "author_name": "user",
                "committed_date": "2023-10-03T00:10:05.000+08:00",
                "committer_email": "user@gitlab.example.com",
                "created_at": "2023-10-03T00:10:05.000+08:00",
                "id": "xxxxxxxxxxxxxxxxxxxxxx",
                "message": "init\n",
                "short_id": "xxxxx",
                "title": "init"
            },
            ...
        ],
        "error": 0,
        "errorMessage": null,
        "status": true
    },
    "version": "1.0.0"
}
```
