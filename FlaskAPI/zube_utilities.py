import requests
import json
import io, base64
import pandas as pd
pd.options.mode.chained_assignment = None
from .generate_zube_jwt import ZubeAPI
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

def refreshJWT():
    CLIENT_ID = 'faad3c4a-4984-11ed-8358-0beb81465ab6'
    PRIVATE_KEY = './secrets/joy_zube_api_key.pem'

    config = {
        'CLIENT_ID': CLIENT_ID,
        'KEY': PRIVATE_KEY,
    }

    zubeAPI_object = ZubeAPI(**config)
    # print(zubeAPI_object.generateFinalToken())
    return zubeAPI_object.generateFinalToken()

# CLIENT_ID = "faad3c4a-4984-11ed-8358-0beb81465ab6"
# APIURL = "https://zube.io/api/cards?where%5Bproject_id%5D=29638"


def fetchZubeJSONdata(APIURL):
    """
        Function that accepts Zube API-URL, and a JWT token;
        to fetch the data and return in JSON format.
    """
    JWT_token = refreshJWT()
    # print(JWT_token)
    headers = {
        "Authorization": "Bearer " + JWT_token,
        "X-Client-ID": "faad3c4a-4984-11ed-8358-0beb81465ab6",
        "Accept": "application/json",
    }
    response = requests.get(APIURL, headers=headers)

    # print(response.status_code)
    jsonData = json.loads(response.content.decode('utf-8'))['data']

    # print(jsonData[0]['sprint_id'])
    return jsonData



def fetch_project_id_names():
    APIURL = "https://zube.io/api/projects"
    projectData = fetchZubeJSONdata(APIURL)
    # print(projectData)
    # project_ids = []
    # project_names = []
    project_id_name_dict={}
    proj_ws_id_dict = {}
    proj_ws_name_dict = {}
    for item in projectData:
        # print(item)
        # project_ids.append(item['id'])
        # project_names.append(item['name'])
        project_id_name_dict.update({item['id']: item['name']})
        proj_ws_id_dict.update({item['id']: [ws['id'] for ws in item['workspaces']]})
        proj_ws_name_dict.update({item['id']: [ws['name'] for ws in item['workspaces']]})

    return project_id_name_dict, proj_ws_id_dict, proj_ws_name_dict


def plot_render_image(plotData, xlabel, ylabel):
    plt.figure(figsize=(8, 8))
    myAxis = sns.countplot(x=plotData)
    myAxis.set(xlabel=xlabel, ylabel=ylabel)
    # myAxis.tick_params(axis='x', labelrotation = 45)
    imgBuffer = io.BytesIO()
    myAxis.figure.savefig(imgBuffer, format="jpeg") # In memory
    imgBuffer.seek(0)
    return base64.b64encode(imgBuffer.getvalue())