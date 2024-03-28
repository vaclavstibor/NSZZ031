#add additional DAGs folders 

import os
import sys
from airflow.models import DagBag

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../dag/extract'))

dag_bag = DagBag(os.path.join(os.path.dirname(__file__), '../../dag'))

if dag_bag:
    for dag_id, dag in dag_bag.dags.items():
        globals()[dag_id] = dag
