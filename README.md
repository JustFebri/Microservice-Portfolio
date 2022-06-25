# Microservice-Portfolio
For testing use localhost:8000/

## Simple Cloud Storage

Service that is used to upload and download files on the service (Uploaded files will be saved in
local folder named upload).
- /regis
- /login
- /logout
- /fileupload - upload file to local folder named upload
- /filedownload/(fileName) - download file based on filename

## Simple Calculator Services

Simple calculator service that are made using Celery to run the task asynchronously.
- celery -A tasks worker -l info -P gevent -> to activate Celery
- /api/prime/(number) - finding n-th prime numbers
- /api/palindrome/(number) - finding n-th palindrome prime numbers

## Students Paper Storage 

Service where students can add / save papers. 
- /regis
- /login
- /logout
- /uploadfile - upload file 
- /filedownload/(fileName) - download file based on filename

## Department News Board
Service that can be used to make news announcement. Certain News will be archived after 1 month has passed.
- /regis
- /login
- /logout
- /all_news - to see all unarchived news
- /all_news/(id) - to see news based on the news id
- /post_news - post news
- /update_news/(id) - edit news
- /delete_news/(id) - delete news
- /download/(id) - download news file by id
