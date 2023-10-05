import requests
import json

class ApiError(Exception):
    def __init__(self, error, description):
        self.error = error
        self.description = description
        super().__init__(f"{self.__class__.__name__}: {error}: {description}")

API_BASE_URL = "https://api.modrinth.com/"

def alive() -> bool:
    """
    Checks if the Modrinth API is alive and responsive.

    Returns:
        bool: True if the API is alive, False otherwise.
    """
    try:
        response = requests.get(API_BASE_URL)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def search_projects(query, facets=None, index="relevance", offset=0, limit=10) -> dict:
    """
    Searches for projects on Modrinth based on the given query and parameters.

    Args:
        query (str): The search query.
        facets (dict, optional): Filters to apply to the search (e.g., {"game": "minecraft"}).
        index (str, optional): The sorting index for search results.
        offset (int, optional): The offset for paginating through results.
        limit (int, optional): The maximum number of results to return.

    Returns:
        dict: A dictionary containing search results, or None if an error occurs.
    """
    search_url = f"{API_BASE_URL}v2/search"
    
    params = {
        "query": query,
        "index": index,
        "offset": offset,
        "limit": limit
    }

    if facets:
        params["facets"] = json.dumps(facets)

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status() 

        if response.status_code != 200:
            error_data = response.json()
            error_message = error_data.get("error", "Unknown error")
            error_description = error_data.get("description", "No description provided")
            raise ApiError(error_message, error_description)

        return response.json()
    except requests.exceptions.RequestException as e:
        raise ApiError("Request Error", str(e))
    except ValueError as e:
        raise ApiError("JSON Parsing Error", str(e))

def get_project(id_slugs) -> dict:
    """
    Retrieves detailed information about a project or multiple projects on Modrinth by their IDs or slugs.

    Args:
        id_slugs (str or list): The ID(s) or slug(s) of the project(s). Can be a single string or a list of strings.

    Returns:
        dict: A dictionary containing project information, or None if an error occurs.
    """
    if not isinstance(id_slugs, list):
        id_slugs = [id_slugs]

    if len(id_slugs) == 1:
        project_url = f"{API_BASE_URL}v2/project/{id_slugs[0]}"
    else:
        project_url = f"{API_BASE_URL}v2/projects?ids={json.dumps(id_slugs)}"

    try:
        response = requests.get(project_url)
        response.raise_for_status()

        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json()
            error_message = error_data.get("error", "Unknown error")
            error_description = error_data.get("description", "No description provided")
            raise ApiError(error_message, error_description)
    except requests.exceptions.RequestException as e:
        raise ApiError("Request Error", str(e))
    except ValueError as e:
        raise ApiError("JSON Parsing Error", str(e))
