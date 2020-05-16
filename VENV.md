# Virtual Environment: Python 3
## Installing Python 3 Virtual Environment
1) Install **virtualenv**:
```
$ pip3 install virtualenv
```

2) Change directory to **project**:
```
$ cd <project>
```

3) Create Python 3 virtual environment for project:
```
$ virtualenv -p python3 venv
```

## Activate & Deactivate Virtual Environment
* Activating virtual environment:

	**Note:** Activation from project directory
```
$ source venv/bin/activate
```

* Deactivating virtual environment:
```
$(venv) deactivate
```

## Install Packages In Virtual Environment
1) Install package:

	**Note:** Virtual environment must be activated.
```
$(venv) pip install <package>
```

## Install requirements.txt In Virtual Environment
1) Install requirements.txt:

	**Note:** **requirements.txt** contains a list of all the packages needed to run the application.
```
$(venv) pip install -r requirements.txt
```

## Creating requirements.txt
1) Create requirements.txt:

	**Note:** Typically created after installing packages in personal virtual environment to share with the collaborators the list of all the packages needed to run the application.
```
$(venv) pip freeze > requirements.txt
```
