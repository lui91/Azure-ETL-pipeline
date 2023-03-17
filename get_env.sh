#!/bin/bash
echo "Exporting"
export TF_VAR_RESOURCE_GROUP=terra-tweets-group
export TF_VAR_POSTGRE_HOST=postgres-tweets.postgres.database.azure.com
export TF_VAR_POSTGRE_DB=disaster_data
export TF_VAR_POSTGRE_LOGIN=terra_lui
export TF_VAR_POSTGRE_PASSWORD='gSDcN&4&bs5Jkt'
echo "Completed"