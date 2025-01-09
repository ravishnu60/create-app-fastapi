# **create-app-fastapi**  

A simple CLI tool for generating FastAPI projects with a predefined structure, including APIs, database setup, models, schemas, and configuration files, enabling a quick start to development.

### **Installation**
To install this package, use the following command:  
```bash
pip install create-app-fastapi
```

### **Usage**
After installation, create a new FastAPI project by running:  
```bash
create-app-fastapi project-name
```
Navigate to the project directory
```bash
cd project-name
```
Start the development server
```bash
fastapi dev main.py
```
Your FastAPI is now up and running on port 8000! 🚀

### **Output**
The generated project will have the following structure:

```
root-folder/
|- APIs/
|  |- __init__.py
|  |- api.py
|- models/
|  |- __init__.py
|  |- model.py
|- schemas/
|  |- __init__.py
|  |- schema.py
|- settings/
|  |- __init__.py
|  |- auth.py
|  |- config.py
|  |- db.py
|- testcase/
|  |- __init__.py
|  |- test_main.py
|- venv/
|-.gitignore
|- main.py
|- requirements.txt
```


### Features

* Predefined project structure for FastAPI applications.
* Includes APIs, models, schemas, and settings files.
* Ready-to-use database connection file (db.py).
* Simplifies setting up new FastAPI projects.


    ------- Happy Coding! 🎉  --------
