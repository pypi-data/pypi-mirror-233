#!usr/bin/env python3

import requests

class HarvestAPI:
    """
    A wrapper around the getharvest.com API using the basic authentication (user token)

    :param user_agent: The user agent of your client
    :type user_agent: String

    :param access_token: The API Access token for the user
    :type access_token: String

    :param account_id: The account id for the user
    :type account_id: String
    """

    HARVEST_BASE_URL = "https://api.harvestapp.com/v2"

    def __init__(self, user_agent, access_token, account_id):

        self.user_agent = user_agent
        self.access_token = access_token
        self.account_id = account_id

    def __get_request_headers(self):
        """
        get_request_headers builds a dict of headers required by harvest's API based on configuration details passed by the user

        :return: a dict containing an Authorization, Harvest-Account-Id, and User-Agent for use in a HTTP request to the Harvest API
        """

        return {"Authorization": "Bearer {}".format(self.access_token), "Harvest-Account-Id": self.account_id, "User-Agent": self.user_agent}

    def get_projects(self, parameters):

        """
        get_projects queries for projects

        :param parameters: Query parameters
        :type parameters: Dict

        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/projects", headers = self.__get_request_headers(), params = parameters)

    def get_project_by_id(self, project_id):
        """
        get_project_by_id returns the project by the given id

        :param project_id: the id of the project
        :type project_id: String

        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/projects/{project_id}", headers = self.__get_request_headers())

    def create_project(self, payload):

        """
        create_project creates a new project with the given payload.

        :param payload: The payload parameters to create the project
        :type payload: Dict

        :return: requests.response representing the API response to the request
        """
        return requests.post(f"{self.HARVEST_BASE_URL}/projects", headers = self.__get_request_headers(), json = payload)

    def update_project(self, project_id, payload):
        """
        update_project updates the project with the given id

        :param project_id: the id of the project
        :type project_id: String

        :param payload: The payload parameters to update the project, all omitted parameters will be left the same
        :type payload: Dict

        :return: requests.response representing the API response to the request
        """

        return requests.patch(f"{self.HARVEST_BASE_URL}/projects/{project_id}", headers = self.__get_request_headers(), json = payload)

    def delete_project(self, project_id):
        """
        delete_project deletes a project by its id

        :param project_id: the id of the project
        :type project_id: String

        :return: requests.response representing the API response to the request
        """

        return requests.delete(f"{self.HARVEST_BASE_URL}/projects/{project_id}", headers = self.__get_request_headers())

    def get_user_assignments(self, parameters):

        """
        get_user_assignments will query for user_assignment objects

        :param parameters: A dict of query parameters
        :type parameters: Dict

        :return: requests.response representing the API response to the request
        """
        return requests.get(f"{self.HARVEST_BASE_URL}/user_assignments", headers = self.__get_request_headers(), params = parameters)

    def get_project_user_assignments(self, project_id, parameters):

        """
        get_project_user_assignments will query for user assignments on the given project id

        :param project_id: The project id
        :type project_id: String

        :param parameters: A dict of query parameters
        :type parameters: Dict
        """
        return requests.get(f"{self.HARVEST_BASE_URL}/projects/{project_id}/user_assignments", headers = self.__get_request_headers(), params = parameters)

    def get_project_user_assignment_by_id(self, project_id, user_assignment_id):
        """
        get_project_user_assignment_by_id will return a user assignment by its id

        :param project_id: The project id
        :type project_id: String

        :param user_assignment_id: The id of the user assignment to update
        :type user_assignment_id: String


        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/projects/{project_id}/user_assignments/{user_assignment_id}", headers = self.__get_request_headers())

    def create_project_user_assignment(self, project_id, payload):
        """
        create_project_task_assignment will create a new user assignment under the given project

        :param project_id: The project id
        :type project_id: String

        :param payload: The payload of parameters to update. Parameters not included will not be updated.
        :type payload: Dict

        :return: requests.response representing the API response to the request
        """

        return requests.post(f"{self.HARVEST_BASE_URL}/projects/{project_id}/user_assignments", headers = self.__get_request_headers(), json = payload)

    def update_project_user_assignment(self, project_id, user_assignment_id, payload):
        """
        update_project_task_assignment will update the user_assignment for the given project 

        :param project_id: The project id
        :type project_id: String

        :param user_assignment_id: The id of the user assignment to update
        :type user_assignment_id: String

        :param payload: The payload of parameters to update. Parameters not included will not be updated.
        :type payload: Dict

        :return: requests.response representing the API response to the request
        """

        return requests.patch(f"{self.HARVEST_BASE_URL}/projects/{project_id}/user_assignments/{user_assignment_id}", headers = self.__get_request_headers(), json = payload)

    def delete_project_user_assignment(self, project_id, user_assignment_id):

        """
        delete_project_user_assignment deletes the user assignment for the given project id and user_assignment id

        :param project_id: The id of the project
        :type project_id: String

        :param user_assignment_id: The id of the user assignment to delete
        :type user_assignment_id: String

        :return: requests.response representing the API response to the request
        """
        return requests.delete(f"{self.HARVEST_BASE_URL}/projects/{project_id}/user_assignments/{user_assignment_id}", headers = self.__get_request_headers())

    def get_users(self, parameters):

        """
        get_users queries for users

        :param parameters: Query parameters
        :type parameters: Dict

        :return: requests.response representing the API response to the request
        """
        return requests.get(f"{self.HARVEST_BASE_URL}/users", headers = self.__get_request_headers(), params = parameters)

    def get_current_user(self):
        """
        get_current_user returns the user currently authenticated by the bearer token

        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/users/me", headers = self.__get_request_headers())

    def get_user_by_id(self, user_id):
        """
        get_user_by_id returns the user by the given id

        :param user_id: The id of the user
        :type user_id: String

        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/users/{user_id}", headers = self.__get_request_headers())

    def create_user(self, payload):

        """
        create_user creates a user with the provided parameters

        :param payload: The payload of parameters.
        :type payload: Dict

        :return: requests.response representing the API response to the request
        """
        return requests.post(f"{self.HARVEST_BASE_URL}/users", headers = self.__get_request_headers(), json = payload)

    def update_user(self, user_id, payload):
        """
        update_user updates the user with the given id

        :param user_id: The id of the user to update
        :type user_id: String

        :param payload: The payload of parameters. Parameters not included will not be updated.
        :type payload: Dict

        :return: requests.response representing the API response to the request
        """

        return requests.patch(f"{self.HARVEST_BASE_URL}/users/{user_id}", headers = self.__get_request_headers(), json = payload)

    def delete_user(self, user_id):

        """
        delete_user deletes the user with the given id

        :param user_id: The id of the user to delete
        :type user_id: String

        :return: requests.response representing the API response to the request
        """
        return requests.delete(f"{self.HARVEST_BASE_URL}/users/{user_id}", headers = self.__get_request_headers())

    def get_user_cost_rates(self, user_id, parameters):
        """
        
        :param user_id: The id of the user
        :type user_id: String

        :param parameters: Query parameters
        :type parameters: Dict

        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/users/{user_id}/cost_rates", headers = self.__get_request_headers(), params = parameters)

    def get_user_cost_rate_by_id(self, user_id, cost_rate_id):
        """
        
        :param user_id: The id of the user
        :type user_id: String

        :param cost_rate_id: The id of the cost_rate
        :type cost_rate_id: String

        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/users/{user_id}/cost_rates/{cost_rate_id}", headers = self.__get_request_headers())

    def create_user_cost_rate(self, user_id, payload):

        """
        create_user_cost_rate creates a cost rate for the user given by the user id

        :param user_id: The id of the user
        :type user_id: String

        :param payload: The payload of parameters. Parameters not included will not be updated.
        :type payload: Dict

        :return: requests.response representing the API response to the request
        """
        return requests.post(f"{self.HARVEST_BASE_URL}/users/{user_id}/cost_rates", headers = self.__get_request_headers(), json = payload)

    def get_user_billable_rates(self, user_id, parameters):

        """
        get_user_billable_rates returns all billable rates on a user by the provided user_id

        :param user_id: The id of the user
        :type user_id: String

        :param parameters: Query parameters only "page" and "per_page" are supported
        :type parameters: Dict

        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/users/{user_id}/billable_rates", headers = self.__get_request_headers(), params = parameters)

    def get_user_billable_rate_by_id(self, user_id, billable_rate_id):

        """
        get_user_billable_rate_by_id returns a billable rate by the provided id

        :param user_id: The id of the user
        :type user_id: String

        :param billable_rate_id: The id of the billable rate
        :type billable_rate_id: String

        :return: requests.response representing the API response to the request
        """
        return requests.get(f"{self.HARVEST_BASE_URL}/users/{user_id}/billable_rates/{billable_rate_id}", headers = self.__get_request_headers())

    def create_user_billable_rate(self, user_id, payload):
        """
        create_user_billable_rate creates a billable rate on the given user

        :param user_id: The id of the user
        :type user_id: String

        :param payload: The payload of parameters. Parameters not included will not be updated.
        :type payload: Dict

        :return: requests.response representing the API response to the request
        """

        return requests.post(f"{self.HARVEST_BASE_URL}/users/{user_id}/billable_rates", headers = self.__get_request_headers(), json = payload)

    def get_user_teammates(self, user_id, parameters):

        """
        get_user_teammates returns a list of assigned teammates for the user

        :param user_id: The id of the user
        :type user_id: String

        :param parameters: Query parameters
        :type parameters: Dict

        :return: requests.response representing the API response to the request
        """
        return requests.get(f"{self.HARVEST_BASE_URL}/users/{user_id}/teammates", headers = self.__get_request_headers(), params = parameters)

    def update_user_assigned_teammates(self, user_id, payload):

        """
        update_user_assigned_teammates will update the list of assigned teammates for the user

        :param user_id: The id of the user
        :type user_id: String

        :param payload: The payload of parameters. Parameters not included will not be updated.
        :type payload: Dict

        :return: requests.response representing the API response to the request
        """

        return requests.patch(f"{self.HARVEST_BASE_URL}/users/{user_id}/teammates", headers = self.__get_request_headers(), json = payload)

    def get_active_user_project_assignments(self, user_id, parameters):

        """
        get_active_user_project_assignments returns a list of currently active projects for the user given by the user id

        :param user_id: The id of the user
        :type user_id: String

        :param parameters: Query parameters. Only "page" and "per_page" are supported.
        :type parameters: Dict

        :return: requests.response representing the API response to the request
        """
        return requests.get(f"{self.HARVEST_BASE_URL}/users/{user_id}/project_assignments", headers = self.__get_request_headers(), params = parameters)

    def get_active_project_assignments_for_current_user(self, parameters):
        
        """
        get_active_project_assignments_for_current_user returns a list of project assignments for the user of the current bearer token

        :param parameters: Query parameters. Only "page" and "per_page" are supported.
        :type parameters: Dict

        :return: requests.response representing the API response to the request
        """
        return requests.get(f"{self.HARVEST_BASE_URL}/users/me/project_assignments", headers = self.__get_request_headers(), params = parameters)

    def get_task_assignments(self, parameters):

        """
        get_task_assignments queries for task assignments. For a list of parameters, see https://help.getharvest.com/api-v2/projects-api/projects/task-assignments/#list-all-task-assignments

        :param parameters: A dict of parameters for querying
        :type parameters: Dict
            
        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/task_assignments", headers = self.__get_request_headers(), params = parameters)

    def get_task_assignments_by_project_id(self, project_id, parameters):

        """
        get_task_assignments_by_project_id queries for task assignments under the given project id. For a list of parameters, see https://help.getharvest.com/api-v2/projects-api/projects/task-assignments/#list-all-task-assignments-for-a-specific-project

        :param parameters: A dict of parameters for querying
        :type parameters: Dict
            
        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/projects/{project_id}/task_assignments", headers = self.__get_request_headers(), params = parameters)

    def get_project_task_assignment_by_id(self, project_id, task_assignment_id):

        """
        get_project_task_assignment_by_id queries for a specific task assignment by id in a project given by the project id. 

        :param project_id: The Project id for the task assignment
        :type project_id: String

        :param task_assignment_id: The id of the task assignment
        :type task_assignment_id: String

        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/projects/{project_id}/task_assignments/{task_assignment_id}", headers = self.__get_request_headers())

    def create_project_task_assignment(self, project_id, payload):

        """
        create_project_task_assignmenttask assignment in a project given by the project id. 

        :param project_id: The Project id for the task assignment. The "task_id" parameter is required in the payload to associate the task. See https://help.getharvest.com/api-v2/projects-api/projects/task-assignments/#create-a-task-assignment
        :type project_id: String

        :param payload: The payload of the task assignment. Must contain a "task_id" parameter.

        :return: requests.response representing the API response to the request
        """

        return requests.post(f"{self.HARVEST_BASE_URL}/projects/{project_id}/task_assignments", headers = self.__get_request_headers(), json = payload)

    def update_project_task_assignment(self, project_id, task_assignment_id, payload):
        
        """
        update_project_task_assignment updates the task assignment given by the id from the project given by the project id

        :param project_id: The Project id for the task assignment. 
        :type project_id: String

        :param task_assignment_id: The id for the task assignment
        :type task_assignment_id: String

        :param payload: The payload of the task assignment. Any parameters not included won't be updated.

        :return: requests.response representing the API response to the request
        """

        return requests.patch(f"{self.HARVEST_BASE_URL}/projects/{project_id}/task_assignments/{task_assignment_id}", headers = self.__get_request_headers(), json = payload)


    def delete_project_task_assignment(self, project_id, task_assignment_id):

        """
        delete_project_task_assignment deletes the task assignment given by the id from the project given by the project id

        :param project_id: The Project id for the task assignment. 
        :type project_id: String

        :param task_assignment_id: The id for the task assignment
        :type task_assignment_id: String

        :return: requests.response representing the API response to the request
        """
        
        return requests.patch(f"{self.HARVEST_BASE_URL}/projects/{project_id}/task_assignments/{task_assignment_id}", headers = self.__get_request_headers())

    def get_time_entries(self, parameters):

        """
        get_time_entries queries for time entries. For a list of parameters see https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#list-all-time-entries 

        :param parameters: A dict of parameters for querying
        :type parameters: Dict
            
        :return: requests.response representing the API response to the request
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/time_entries", headers = self.__get_request_headers(), params = parameters)

    def get_time_entry_by_id(self, time_entry_id):

        """
        get_time_entry_by_id retrieves a specific time entry object by its id.

        :param time_entry_id: The id of the time entry
        :type param: String
        """

        return requests.get(f"{self.HARVEST_BASE_URL}/time_entries/{time_entry_id}", headers = self.__get_request_headers())
    
    def create_time_entry(self, payload):

        """
        create_time_entry creates a time entry for the given project and task, on the given date, and for the given time period. parameters MUST contain at least "project_id", "task_id", and "spent_date". If you want to log time by number of hours pass "hours" as a float e.g. 1.75 == 1h 45mins. If you want to log time by start and end time, pass "started_time" and "ended_time" as a string e.g. "8:00am". If you pass "started_time" but not "ended_time", then the entry is counted as "running" until stopped. See https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#create-a-time-entry-via-duration for more details.

        :param payload: Dict of parameters to create the time entry
        :type payload: Dict

        :return: requests.response representing the API response to the request.
        """

        return requests.post(f"{self.HARVEST_BASE_URL}/time_entries", headers = self.__get_request_headers(), json = payload)

    def update_time_entry(self, time_entry_id, payload):

        """
        update_time_entry updates the time entry for the given id. Any parameters not included in the payload won't be updated. See https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#update-a-time-entry

        :param time_entry_id: The time entry id to update
        :type time_entry_id: String

        :param payload: Dict of parameters to create the time entry
        :type payload: Dict

        :return: requests.response representing the API response to the request.
        """

        return requests.patch(f"{self.HARVEST_BASE_URL}/time_entries/{time_entry_id}", headers = self.__get_request_headers(), json = payload)

    def delete_time_entry_external_reference(self, time_entry_id):
        """
        Delete the external_reference from the given time entry.

        :param time_entry_id: The time entry id from which to delete the time entry
        :type time_entry_id: String

        :return: requests.response representing the API response to the request.
        """

        return requests.delete(f"{self.HARVEST_BASE_URL}/time_entries/{time_entry_id}/external_reference", headers = self.__get_request_headers())

    def delete_time_entry(self, time_entry_id):

        """
        delete_time_entry deletes the time entry for the given id.

        :param time_entry_id: The id of the time entry to delete
        :type time_entry_id: String

        :return: requests.response representing the API response to the request.
        """

        return requests.delete(f"{self.HARVEST_BASE_URL}/time_entries/{time_entry_id}", headers = self.__get_request_headers())

    def restart_stopped_time_entry(self, time_entry_id):
        
        """
        restart_stopped_time_entry restarts a time entry if it is not currently running.

        :param time_entry_id: The id of the time entry to restart
        :type time_entry_id: String

        :return: requests.response representing the API response to the request.
        """

        return requests.patch(f"{self.HARVEST_BASE_URL}/time_entries/{time_entry_id}/restart", headers = self.__get_request_headers())

    def stop_running_time_entry(self, time_entry_id):

        """
        stop_running_time_entry stops a time entry if it is not already stopped.

        :param time_entry_id: The id of the time entry to stop
        :type time_entry_id: String

        :return: requests.response representing the API response to the request.
        """

        return requests.patch(f"{self.HARVEST_BASE_URL}/time_entries/{time_entry_id}/stop", headers = self.__get_request_headers())

