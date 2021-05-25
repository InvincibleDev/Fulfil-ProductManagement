# Fulfil-ProductManagement
Product Management

### Tech used:
1) Django Backend
2) Vue Js Frontend
3) Postgres DB
4) Celery with Redis for Async Tasks

### Steps to run:

<ul>
<li> Install packages from requirements.txt </li>
<li> Install and run redis server and configure the same in settings.py </li>
<li> Configure Celery and run celery worker </li>
<li> Set all required environment variables like: </li>
<ul>
<li> IS_PRODUCTION </li>
<li> DB_USER  </li>
<li> DB_PASSWORD </li>
<li> DB_NAME </li>
</ul>
</ul>

### TODO :
1) Save celery task details to the database to maintain task status even after reloading in the frontend.
2) Double check if the file uploaded has the proper column names and filetype inside.
