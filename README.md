# 4517-img-processing-proj
4517's Image Processing Django Application

This is an app that let users to upload images and view them. 

However, there is no functionality to download images. Maybe if I am not lazy, I will add that functionality. 

Must do:

1. All the images are saved in media/ folder. So before running this app, make sure to create a directory called media/.

media/ should be on the same level as README.md, requirements.txt along with other top files and directories. 

2. There is a portion that uploads images to S3. Make sure to configure your AWS credential correctly. 

3. Make sure to create a virtualenv, clone this repo and run pip install -r requirements.txt to receive all the packages.

--------------------------------------------------------------------------

If you want to deploy this application with auto-scaling group on AWS, make sure to:

1. Specify the Load Balancer's port to that of the port in which DJANGO server run on each instance. The port value by default for this app is 8000. 

But if you want to change it, make sure to change it in the start_gunicorn.sh script.

2. Since we use gunicorn to deploy our DJANGO app, I suggest you to google how to create init script. Make sure to specify the command su - "sh /path/to/start_gnicorn.sh" user_that_you_use_to_clone_this_repo in order to start gunicorn. 

--------------------------------------------------------------------------
Endpoints:

/display_images: to see images with their names
/image_upload: to upload images
/success: should show up after a user has successfully uploaded an image

For more endpoints, look into urls.py and views.py in imgApp/ directory.
--------------------------------------------------------------------------

A few more things to keep in mind:

To Run the server run:
python3 manage.py runserver 0.0.0.0:8000

To sync db to prevent table not found error and if images not showing up:
python manage.py migrate --run-syncdb

To deploy the DJANGO app, install gunicorn:
pip3 install gunicorn

Make sure port 8000 is opened on your machine

Make sure to change the variable path and name to reflect your application

Run sh start_gnicorn.sh to deploy your application.
