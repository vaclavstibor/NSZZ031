# docker exec extract-transform-load-webserver-1 airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

airflow db migrate

#airflow users create \
#    --username admin \
#    --password admin \
#    --firstname Admin \
#    --lastname User \
#    --role Admin \
#    --email admin@example.com

#airflow db migrate

# Don't forget chmod +x init-admin.sh