# ServeHub Python client

This is a Python client for [ServeHub](https://servehub.co). It lets you run ML APIs hosted on your infrastructure from anywhere Python runs (pipelines, Jupyter notebooks, etc).

## Install

```sh
pip install servehub
```

## Authenticate

Before running any Python scripts that use the API, you need to set your ServeHub API token in your environment.

Grab your token from [servehub.co/settings](https://servehub.co/settings) and set it as an environment variable:

```
export SERVEHUB_API_TOKEN=<your token>
```

We recommend not adding the token directly to your source code, because you don't want to put your credentials in source control. If anyone used your API key, their usage would be charged to your account.

## Run a model

Create a new Python file and add the following code:

```python
>>> import servehub
>>> servehub.run(
        "<user_name>/<api_name>:<deployment_name>",
        input={"prompt": "a 19th century portrait of a wombat gentleman", "another_arg": "its value"}
    )

```

## Errors and Exceptions
- `servehub.exceptions.ServeHubException` - The base class that all the below errors inherit from.
- `servehub.exceptions.ServeHubError` - Raised when an error originates from ServeHub.
- `servehub.exceptions.ApiNotFoundError` - Raised when trying to run an API that does not exist, or that the user doesn't have access to.
- `servehub.exceptions.ApiNotDeployedError` - Raised when trying to run an API that is not deployed.
- `servehub.exceptions.ApiError` - An error from the deployed API's code.

