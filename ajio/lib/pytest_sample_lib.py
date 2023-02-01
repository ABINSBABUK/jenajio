import kpi_names
import os
#lib_dir = os.path.join(root_dir, 'lib')
import label_categories
import genre_ids as genre_ids
import time

def init_timing(session_data):
    # initialising variables
    session_data.KPI_COUNT = 2
    session_data.status = "Fail_launch"
    session_data.pass_count = 0
    session_data.fail_count = 0
    session_data.ADD_KPI_ANNOTATION = True
    session_data.app_size_info= None
    session_data.delta_time = 5
    session_data.connection_status= ""
    session_data.data_kpi = True
    session_data.debug = False

    # Categories
    session_data.KPI_LABEL_CATEGORY = label_categories.STREAMING_LABEL_KPI
    session_data.HS_LABEL_CATEGORY = label_categories.HS_LABEL_CATEGORY
    session_data.ACTION_LABEL_CATEGORY = label_categories.APPIUM_ACTION_LABEL_CATEGORY
    session_data.genre_id = genre_ids.STREAMING_GENRE


    # KPIs
    session_data.app_launch_time = None
    session_data.app_login_time = None

    #Data KPI's
    session_data.data_kpis = {}

    # KPI Labels
    session_data.kpi_labels = {}
    session_data.kpi_labels[kpi_names.LAUNCH_TIME] = {'start': None, 'end': None}
    ##session_data.kpi_labels[kpi_names.LOGIN_TIME] = {'start': None, 'end': None}
    #session_data.kpi_labels[kpi_names.RELAUNCH_TIME] = {'start': None, 'end': None}
    session_data.kpi_labels[kpi_names.SEARCH_TIME] = {'start': None, 'end': None}
    #session_data.kpi_labels[kpi_names.DETAILS_PAGE_LOAD] = {'start': None, 'end': None}
    #session_data.kpi_labels[kpi_names.CHART_LOAD_TIME] = {'start': None, 'end': None}

    
    # Action Labels
    session_data.ADD_KPI_ANNOTATION = True
    session_data.session_start = None
    session_data.appium_timestamps = {}
    session_data.action_labels = {}
