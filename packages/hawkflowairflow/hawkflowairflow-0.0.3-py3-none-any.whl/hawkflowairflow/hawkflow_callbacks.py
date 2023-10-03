import re

from hawkflowclient.hawkflow_api import *

HF_API_KEY = ""


def hawkflow_start_callback(context):
    send_to_hawkflow('start', context)


def hawkflow_success_callback(context):
    send_to_hawkflow('end', context)


def remove_date_suffix(s):
    # This regex matches the pattern __ followed by 8 digits at the end of the string
    return re.sub(r'__\d{8}$', '', s)


def get_process_meta(context):
    # task_instance_key_str will be something like dag_name__task_name__date_string
    original_string = context['task_instance_key_str']
    split_string = original_string.split("__", 1)

    # Get the dag name and task name so that we can send  the 'process'
    # and 'meta' parameters to HawFlow. This will get the best details
    # in the HawkFlow UI.
    process = split_string[0]
    meta_with_date = split_string[1]
    meta = remove_date_suffix(meta_with_date)
    return process, meta


def send_to_hawkflow(action, context):
    hf = HawkflowAPI(HF_API_KEY)
    process, meta = get_process_meta(context)

    if action == "start":
        try:
            hf.start(process, meta)
        except Exception as e:
            # this will show in your airflow logs if there
            # are any errors. HawkFlow handles its own errors,
            # so it will never break your airflow DAGs
            print(traceback.format_exc())
            hf.exception(process, meta, traceback.format_exc())
    if action == "end":
        try:
            hf.end(process, meta)
        except Exception as e:
            # this will show in your airflow logs if there
            # are any errors. HawkFlow handles its own errors,
            # so it will never break your airflow DAGs
            print(traceback.format_exc())
            hf.exception(process, meta, traceback.format_exc())
