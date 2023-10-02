# Python Harvest API Wrapper

Yet another Python wrapper for the [Harvest API](https://help.getharvest.com/api-v2/) project management and time tracker application.

This wrapper has incredibly humble goals, which are to support some specific API calls on some functionality to support a Harvest CLI application.

No Oauth2, authentication is done by passing an API token and a user ID into the constructor. The constructor also requires a user agent to be passed down, as the wrapper is intended to sit as a library within a larger application.

## Basic usage

```python
from getharvest_api_wrapper import HarvestAPI

h = HarvestAPI("$USER_AGENT", "$ACCESS_TOKEN", "$ACCOUNT_ID")

# Some basic functionality. Wherever the API specifies you can have query parameters in a GET request, you should pass in a dict of parameters. This can be empty.
# For payloads for the POST and PATCH requests, you should pass in a dict of these parameters as well.

my_project_assignments = h.get_active_project_assignments_for_current_user({}).json()

response = h.update_user_assigned_teammates('$TARGET_USER_ID', {'teammate_ids': [1234, 5678]})

```

## Documentation

For now, view the documentation using pydoc:

```
python3 -m pydoc getharvest_api_wrapper/harvest_api.py
```
