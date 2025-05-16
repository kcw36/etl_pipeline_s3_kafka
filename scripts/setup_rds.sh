BASENAME=$(basename "$(pwd)")
if [ "$BASENAME" = "Coursework-Advanced-Data-Week-1"  ]
then 
    source .env
    psql --host=$DATABASE_IP --port=$DATABASE_PORT --username=$DATABASE_USERNAME --dbname=$DATABASE_NAME --password -f "./example_db/schema.sql"
fi
if [ "$BASENAME" = "scripts"  ]
then 
    source ../env
    psql --host=$DATABASE_IP --port=$DATABASE_PORT --username=$DATABASE_USERNAME --dbname=$DATABASE_NAME --password -f "../example_db/schema.sql"
fi


                 