"""
This script is used to load the extract transform load DAG in the `extract-transform-load/dag` folder into the Airflow webserver.
We use the `DagBag` class from the `airflow.models` module to load the DAGs into the global namespace.
"""

import os
from airflow.models import DagBag


# Create a DagBag instance
dag_bag = DagBag(os.path.join(os.path.dirname(__file__), "../../dag"))

# If the DagBag instance is not empty
if dag_bag:
    # Iterate over all the DAGs in the DagBag
    for dag_id, dag in dag_bag.dags.items():
        # Add each DAG to the global namespace
        globals()[dag_id] = dag

