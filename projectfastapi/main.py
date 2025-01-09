import os, platform, sys, subprocess, threading, time, argparse, requests, shutil
from .source import getFileData

version= '0.1.6'

def main():
    try:
        parser = argparse.ArgumentParser(prog ='create-app-fastapi', description="Create fastapi project") 
        parser.add_argument('name', metavar ='NAME', type = str, help ='create a project in this name')
        parser.add_argument('-v','--version',action='version',
                        version='%(prog)s '+version, help ="show program's version number and exit")
        args = parser.parse_args()

        curdir= os.getcwd()
        platformOS= platform.system()
        threadStop= False

        # terminal color code
        RED = "\033[31m"
        GREEN = "\033[32m"
        RESET = "\033[0m"
        
        # display loading
        def loading():
            load= 0
            symbol=['*   ',' *  ','  * ','   *']
            while True:
                print("\r", end="")
                print("Setup virtual environment and installing dependencies", end="")
                print(GREEN,symbol[load],RESET, end="")
                load +=1
                time.sleep(0.5)
                if load >= 3:   load= 0
                if threadStop:    
                    print()
                    break

                # create folders and files
        def create_dir(folderName, base= False):
            fullFolderName= folderName if base else os.path.join(name, folderName)
            files= {'settings':['auth.py','config.py','db.py'], 'models':['model.py'],'schemas':['schema.py'],'APIs':['api.py'],'testcase':['test_main.py']}
            try:
                if os.path.exists(fullFolderName):
                    exit(RED + f"Folder {fullFolderName} already exists" + RESET)
                os.mkdir(fullFolderName)

                # create files inside folder
                if files.get(folderName):
                    for file in files[folderName]:
                        with open(f"{fullFolderName}/{file}", 'w') as f:
                            f.writelines(fileData[file])
                if not base:
                    with open(fullFolderName+'/__init__.py','w') as f:
                        pass
            except Exception as err:
                exit(err)

        # execute system cmd using subprocess
        def run(cmd):
            status= subprocess.run(cmd, shell=True,cwd=os.path.join(curdir, name),capture_output=True)
            if status.returncode != 0:
                raise Exception(status.stderr.decode('utf-8'))
        
        # function to delete project if error
        def errorExit(error):
            try:
                shutil.rmtree(os.path.join(curdir, name))
                # run(f"rm -rf {os.path.join(curdir, name)}")
            except:
                pass
            exit(F"{error}\n")

        # thread for display loading same time of execute cmd
        thread= threading.Thread(target=loading)

        # validate latest version
        data= requests.get("https://pypi.org/pypi/create-app-fastapi/json")
        if version != data.json()['info']['version']:
            print(RED + "Please update the latest version to access new features" + RESET)
            print("To upgrade use "+GREEN + "pip install create-app-fastapi --upgrade" + RESET)
            stop= input("Do you want to continue with older ? (y/n): ")
            if (stop=='' or stop.lower() != 'y'):
                exit(RED+"Error: Cancelled, because of older version "+RESET)

        # Inputs
        name= args.name
        virENV= input("Virtual environment name (default 'venv'): ")
        db_data={}
        db_input= input("Continue with database setup ? (y/n): ")
        default_credentials=[{"name":"postgres", "port":"5432"}, {"name":"root", "port": '3306'}]
        if db_input and db_input.lower() == 'y':
            print(f"""{GREEN}You can update Database details later in .env file!{RESET}""")
            db= input("Database (mysql or postgresql, default 'postgresql'): ")
            index= 0
            if db and db.lower() == 'mysql':
                index= 1
            db_data.update( {
                'db': db if db else 'postgresql',
                'database':input(f"Database name (default '{default_credentials[index]['name']}'): "),
                'dbuser':input(f"Database user (default '{default_credentials[index]['name']}'): "),
                'password':input(f"Database password (default '{default_credentials[index]['name']}'): "),
                'host':input("Database host (default 'localhost'): "),
                'port':input(f"Database port (default '{default_credentials[index]['port']}'): "),
            })

        virENV= virENV if virENV else 'venv'
        dependencies= ['fastapi[standard]','pydantic_settings','sqlalchemy','SQLAlchemy-Utils','pytest']
        if db_data.get('db'):
            dependencies.append('psycopg2') if db_data.get('db').lower()=='postgresql' else dependencies.append('mysql-connector-python')

        # get file data
        fileData= getFileData(name, virENV, db_data)


        # create project directory
        create_dir(name, base= True)

        # Start loading thread for show loading while install dependencies
        thread.start()
        err= False

        try:
            if platformOS == 'Linux':
                run(f"{sys.executable} -m venv {virENV}")
                run(f"{virENV}/bin/pip install {' '.join(dependencies)}")
                run(f"{virENV}/bin/pip freeze > requirements.txt")

            elif platformOS == 'Windows':
                run(f"{sys.executable} -m venv {virENV}")
                run(f"{virENV}\\Scripts\\pip.exe install {' '.join(dependencies)}")
                run(f"{virENV}\\Scripts\\pip3.exe freeze > requirements.txt")
        except Exception as error:
            err=error

        # Stop the thread after istall dependencies
        threadStop= True
        thread.join()
        
        if err:
            print(RED+'\nError while creating virtual environment'+RESET)
            errorExit(err)

        # project folders
        project_dirs= ['settings', 'models', 'schemas', 'APIs', 'testcase']

        # loop for creating folders
        for dir in project_dirs:
            create_dir(dir)
        # creating base files
        base_files= ['main.py', '.gitignore','.env']
        for file in base_files:
            with open(f'{name}/{file}','w') as f:
                f.writelines(fileData[file])

        print(f"""{GREEN}Project created successfully!{RESET}

        Note: activate virtual environment before run source {GREEN}main.py{RESET}
        Run API service : fastapi dev main.py
        Run testcase : pytest -v
        {GREEN}Have a nice day! {RESET}
        """)

        openvs= input("Open project in VS Code? (y/n): ")
        if openvs.lower() == 'y':
            run("code .")
        return
    except KeyboardInterrupt:
        threadStop= True
        try: 
            thread.join()
        except: 
            pass
        errorExit("\n"+RED+"Error: Cancelled by user"+RESET)
        pass
    except Exception as error:
        print(error)
        threadStop= True
        try: 
            thread.join()
        except: 
            pass
        errorExit(error)
        pass