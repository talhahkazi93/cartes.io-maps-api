from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
import sys,os,time
from subprocess import Popen, PIPE
from extract_location import run_loc

def get_map_id(ti):
    path = os.path.join(sys.path[0], "mapper.py")
    p = Popen(['python', path, '-m'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == 0:
        val = output.decode("utf-8")
        ti.xcom_push(key='map_id', value=val)
    else:
        ti.xcom_push(key='map_id', value='060e1fea-bc79-4a29-bd87-e7a577361d3b')
        # raise ValueError('No return value for map_id')

def put_marker(ti):
    mapid = ti.xcom_pull(key='map_id' , task_ids='create_map')
    markers = ti.xcom_pull(key='locations_dict', task_ids='extract_locations')

    for key,value in markers.items():
        print("================================+++++++++++++++++++++++++++++++++++++++++++++++++")
        path = os.path.join(sys.path[0], "mapper.py")
        p = Popen(['python', path, '-c','-mi',mapid,'-rn',key,'-rl',value['latitude'],'-rg',value['longitude']],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        val = output.decode("utf-8")
        print(val)
        time.sleep(5)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3)
}

with DAG('cartes_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    extract_loc = PythonOperator(
        task_id = 'extract_locations',
        python_callable = run_loc,
        op_kwargs = Variable.get("get_location_settings",deserialize_json=True),
        do_xcom_push = False
    )
    create_map = PythonOperator(
        task_id='create_map',
        python_callable=get_map_id,
        do_xcom_push=False
    )
    create_markers = PythonOperator(
        task_id='create_markers',
        python_callable=put_marker,
    )

    extract_loc >> create_map >> create_markers