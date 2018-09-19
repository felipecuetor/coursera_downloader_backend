#Coursera downloader

This app allows you to download and manage the files of coursera courses.
It was created using the coursera-dl python library, which facilitates the download process.

In order to install the app dependencies you can run the following command:

```
python -m pip install -r "requirements.txt"
```

In order to run the main app you can run the following commandline using the terminal:

```
python manage.py runserver
```

In order to manually download a course through run the following command (You will be prompted to input the necessary information):

```
python manual_course_download.py
```

If you already have the files of a previously downloaded course, you can import it by placing the files in the `<root_folder>/data/` directory and running the following command:

```
python populate_coursera_db.py
```

We recommend accessing this service though a https connection. If this is not an option, we recommend creating a file in the root directory with the following name: `default_user.conf`
The file should have the following structure(Without quotations, commas, or extra symbols):

```
username=Your_UserName_Here
password=Your_Password_Here
```

When the user and password in the web interface are left empty, the app will automatically fall back to the default_user configuration file. This will allow you to avoid sending your credentials through a non-secure connection.

This app should be used as a distribution method of coursera courses, we will not be liable for the wrongful use of this app. It was designed for personal use only.
