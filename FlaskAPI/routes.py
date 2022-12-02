from pathlib import Path
from flask import Blueprint, render_template
import pandas as pd
from pandas_profiling import ProfileReport
from .zube_utilities import fetch_project_id_names

routes = Blueprint('routes', __name__)




# LogIn/Home Page
@routes.route('/')
@routes.route('/home')
def home():
    return render_template('home.html')

# About Us page  Routing
@routes.route('/about_us', methods=('POSTS', 'GET'))
def aboutUs():
    return render_template('aboutus.html')


# >>>>>>>>>>>>>>>>>>>>>>>   Load the JSON Data into Pandas Dataframe    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
sample_DF = pd.read_json('./secrets/zubeio.json')



# To render the dataframe in tabular format on the website
@routes.route('/dataframe', methods=("POST", "GET"))
def zubeDataFrame():
    # APIURL = "https://zube.io/api/cards"
    # jsonData = fetchZubeJSONdata(APIURL)
    # sample_DF = pd.json_normalize(jsonData)
    return render_template('dataframe.html',
                            PageTitle="dataframe",
                            table=[sample_DF.to_html(classes='data', index=False, header=True)],
                            titles=sample_DF.columns.values)



# To render the quick data analysis report on the created dataframe
qda_file = Path(__file__).parent/"templates/qda.html"
# print(qda_file)
if not qda_file.is_file():
    print('Report html is not present!, Creating One....')
    zubeProfile = ProfileReport(sample_DF, title="Data Analysis Report",
                                        explorative=True)  # explorative=True
    zubeProfile.to_file(qda_file)


@routes.route('/quick_data_analysis', methods=("POST", "GET"))
def quick_data_analysis():
    return render_template('qda.html')



#################  Zube - Ananlysis Routes  ##################

@routes.route('/deployment_frequency', methods=('POSTS', 'GET'))
def deployment_frequency():
    project_id_name_dict, proj_ws_id_dict, proj_ws_name_dict = fetch_project_id_names()
    return render_template("analysis/deployment_frequency.html", project_id_names=project_id_name_dict)

@routes.route('/burn_down', methods=("POST", "GET"))
def  burn_down():
    project_id_name_dict, proj_ws_id_dict, proj_ws_name_dict = fetch_project_id_names()
    project_id_name_zip = zip(list(proj_ws_id_dict.values()), proj_ws_name_dict.values())
    return render_template('analysis/burn_down.html',project_id_names=project_id_name_dict, proj_workspace=project_id_name_zip)


@routes.route('/burn_up', methods=("POST", "GET"))
def  burn_up():
    project_id_name_dict, proj_ws_id_dict, proj_ws_name_dict = fetch_project_id_names()
    project_id_name_zip = zip(list(proj_ws_id_dict.values()), proj_ws_name_dict.values())
    return render_template('analysis/burn_up.html',project_id_names=project_id_name_dict, proj_workspace=project_id_name_zip)


@routes.route('/code_velocity', methods=("POST", "GET"))
def  code_velocity():
    project_id_name_dict, proj_ws_id_dict, proj_ws_name_dict = fetch_project_id_names()
    project_id_name_zip = zip(list(proj_ws_id_dict.values()), proj_ws_name_dict.values())
    return render_template('analysis/code_velocity.html',project_id_names=project_id_name_dict, proj_workspace=project_id_name_zip)



#################  Filter Routes  ##################
@routes.route('/project_filter', methods=('POSTS', 'GET'))
def projectFilter():
    project_id_name_dict, proj_ws_id_dict, proj_ws_name_dict = fetch_project_id_names()
    # print(project_names), print(project_ids)
    return render_template('filters/project_filter.html', project_id_names=project_id_name_dict)


@routes.route('/user_filter', methods=('POSTS', 'GET'))
def userFilter():
    return render_template('filters/user_filter.html')


@routes.route('/date_range_filter', methods=('POSTS', 'GET'))
def dateRangeFilter():
    return render_template('filters/date_range_filter.html')