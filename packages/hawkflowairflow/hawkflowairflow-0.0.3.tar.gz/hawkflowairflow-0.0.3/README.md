![HawkFLow.ai](https://hawkflow.ai/static/images/emails/bars.png)

# HawkFlow.ai apache airflow integration

1. First, sign up to hawkflow for free: https://hawkflow.ai/ and get an API key
2. Install the pip package `pip install hawkflowairflow`
3. Add this to the top of your DAG
   
```python
from hawkflowairflow import hawkflow_callbacks

hawkflow_callbacks.HF_API_KEY = "YOUR_HAWKFLOW_API_KEY_HERE"
```

4. Add these two lines to default_args in your DAG:

```
default_args={    
    "on_success_callback": hawkflow_callbacks.hawkflow_success_callback,
    "on_execute_callback": hawkflow_callbacks.hawkflow_start_callback
}
``` 

All done. Now when your DAG runs, you will see the output in the HawkFlow UI. https://app.hawkflow.ai/login


### <span style="color:#D10000">Known Issues</span>

If you are on an <span style="color:red">ARM mac</span> and notice that your DAG is just hanging. You may need to put this
at the top of your DAG. Airflow is running as a different user on your mac, and the security is blocking outgoing requests.

```
import os
os.environ['NO_PROXY'] = '*'
```

### More examples

More examples: [HawkFlow.ai Python examples](https://github.com/hawkflow/hawkflow-examples/tree/master/python)

Read the docs: [HawkFlow.ai documentation](https://docs.hawkflow.ai/)

## What is HawkFlow.ai?

HawkFlow.ai is a new monitoring platform that makes it easier than ever to make monitoring part of your development process. 
Whether you are an Engineer, a Data Scientist, an Analyst, or anyone else that writes code, HawkFlow.ai helps you and your team take ownership of monitoring.
