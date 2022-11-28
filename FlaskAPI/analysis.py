import base64
import io
import pandas as pd
pd.options.mode.chained_assignment = None
from flask import Flask, render_template, Blueprint, request, send_file
from .zube_utilities import fetchZubeJSONdata, fetch_project_id_names, plot_render_image
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import calendar
sns.set_style('darkgrid')

analysis = Blueprint('analysis', __name__, static_folder='static')

########################################################################################
#########          Display Project-Wise Data in a Table format              ############
########################################################################################

@analysis.route("/display_project_wise_data", methods=("POST", "GET"))
def displayProjectData():
    project_id = request.form.get('fetchProjectid')
    APIURL = "https://zube.io/api/cards?where%5Bproject_id%5D=" + project_id

    # workspace_id = request.form.get('workspaceid')
    # APIURL2 = "https://zube.io/api/workspaces/" + workspace_id + "/sprints"
    # print(APIURL)
    projectIdData = fetchZubeJSONdata(APIURL)
    sample_DF = pd.json_normalize(projectIdData)
    columnList = ['project_id', 'sprint_id', 'body', 'category_name', 'closed_at',
                  'points', 'priority', 'status', 'title', 'created_at', 'assignees']
    newDF = sample_DF[columnList]
    project_id_name_dict, proj_ws_id_dict, proj_ws_name_dict = fetch_project_id_names()  # Sticky Form
    return render_template('filters/project_filter.html',
                           PageTitle="dataframe",
                           table=[newDF.to_html(
                               classes='data', index=False, header=True)],
                           titles=newDF.columns.values, project_id_names=project_id_name_dict)



################################################################################################
#    Plotting Deployment Frequency based on selected filter; e.g. Project, User & Date-Range   #
################################################################################################

@analysis.route('/plot_deployment_frequency', methods=("POST", "GET"))
def plot_deployment_frequency():
    # Sticky Form Codes
    project_id_name_dict, proj_ws_id_dict, proj_ws_name_dict = fetch_project_id_names()

    if request.form.get('filter_type_name') == "choose":
        return render_template('analysis/deployment_frequency.html', error_msg = "Please select a value from the dropdown", project_id_names=project_id_name_dict)

    if request.form.get('filter_type_name') == "project":
        project_id = request.form.get('fetchProjectid')
        APIURL = "https://zube.io/api/cards?where%5Bproject_id%5D=" + project_id
        # print(APIURL)
        projectIdData = fetchZubeJSONdata(APIURL)
        sample_DF = pd.json_normalize(projectIdData)
        plotDF = sample_DF[pd.notnull(sample_DF['closed_at'])]
        plotDF['month'] = pd.DatetimeIndex(plotDF['closed_at']).month
        plotDF['month'] = plotDF['month'].fillna(0)
        plotDF['month'] = plotDF['month'].apply(lambda x: calendar.month_name[x])

        # Below function call plot_render_image() is to draw & rendering CountPlot
        imgInMemory = plot_render_image(plotDF['month'], "Month", "Count of Closed Tasks")
        return render_template('analysis/deployment_frequency.html', plot_url=imgInMemory.decode('utf-8'), project_id_names=project_id_name_dict)

    if request.form.get('filter_type_name') == "users":
        project_id = request.form.get('fetchProjectid')
        APIURL = "https://zube.io/api/cards?where%5Bproject_id%5D=" + project_id
        # print(APIURL)
        projectIdData = fetchZubeJSONdata(APIURL)
        sample_DF = pd.json_normalize(projectIdData)
        userdf = sample_DF[pd.notnull(sample_DF['closed_at'])]
        userdf['usernames'] = userdf['assignees'].apply(lambda x: x[0]['username'])

        # Below function call plot_render_image() is to draw & rendering CountPlot
        imgInMemory = plot_render_image(userdf['usernames'], "Usernames", "Count of Closed Tasks")
        return render_template('analysis/deployment_frequency.html', plot_url=imgInMemory.decode('utf-8'), project_id_names=project_id_name_dict)

    if request.form.get('filter_type_name') == "date_range":
        try:
            project_id = request.form.get('fetchProjectid')
            start_date = request.form.get('start_date_name')
            end_date = request.form.get('end_date_name')

            # print(start_date, end_date)
            APIURL = "https://zube.io/api/cards?where%5Bproject_id%5D=" + project_id
            projectIdData = fetchZubeJSONdata(APIURL)
            sample_DF = pd.json_normalize(projectIdData)
            sample_DF['closed_at'] = pd.to_datetime(sample_DF['closed_at'])
            sample_DF['created_at'] = pd.to_datetime(sample_DF['created_at'])
            datedf = sample_DF[pd.notnull(sample_DF['closed_at'])]
            # print(datedf.dtypes)
            datedf['created_date'] = datedf.created_at.map(lambda x: x.strftime('%Y-%m-%d'))
            date_range_mask = (datedf['created_date'] > start_date) & (datedf['created_date'] <= end_date)
            datedf_filtered = datedf.loc[date_range_mask]
            # print(datedf_filtered)

            # Below function call plot_render_image() is to draw & rendering CountPlot
            imgInMemory = plot_render_image(datedf_filtered['created_date'], "Date", "Count of Closed Tasks")
            return render_template('analysis/deployment_frequency.html', plot_url=imgInMemory.decode('utf-8'), project_id_names = project_id_name_dict)
        except ValueError:
            return render_template('analysis/deployment_frequency.html', error_msg = "No tasks are available within this Date-Range!", project_id_names=project_id_name_dict)



