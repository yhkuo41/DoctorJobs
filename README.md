# Doctor Jobs

...

## Run FastAPI application
```
uvicorn main:app --reload
```

## Instructions to build Python environment

### Linux, using Python 3.10, virtualenv

Install system packages

    sudo apt-get install python3 python3-pip python3-virtualenv

Install remaining packages in virtualenv

    virtualenv -p `which python3` venv
    ./venv/bin/pip3 install -r requirements.txt

### Run tests in command line

Run from root directory.

    python -m unittest discover tests

or

    ./venv/bin/python3 -m unittest discover tests

### Run tests in PyCharm

If you PyCharm project is the repository, then mark root directory as sources root (in Project panel, in the
context menu of directory "Mark Directory As" -> "Sources Root").