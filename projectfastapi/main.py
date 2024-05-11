import os, platform, sys, subprocess, threading, time, argparse
from source import getFileData

def main():
    try:
        parser = argparse.ArgumentParser(prog ='create-app-fastapi', description="Create fastapi project") 
        parser.add_argument('name', metavar ='NAME', type = str, help ='create a project in this name')
        parser.add_argument('-v','--version',action='version',
                        version='%(prog)s 0.0.6', help ="show program's version number and exit")
        args = parser.parse_args()

        curdir= os.getcwd()
        platformOS= platform.system()
        threadStop= False

        # terminal color code
        RED = "\033[31m"
        GREEN = "\033[32m"
        RESET = "\033[0m"

        # Inputs
        name= args.name
        virENV= input("Virtual environment name (default 'venv'): ")
        virENV= virENV if virENV else 'venv'
        dependencies= ['fastapi[all]','sqlalchemy','pytest']

        # get file data
        fileData= getFileData(name, virENV)

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

        # execute system cmd using subprocess
        def run(cmd):
            status= subprocess.run(cmd, shell=True,cwd=os.path.join(curdir, name),capture_output=True)
            if status.returncode != 0:
                raise Exception(status.stderr.decode('utf-8'))
        
        # function to delete project if error
        def errorExit(error):
            run(f"rm -rf {os.path.join(curdir, name)}")
            exit(F"{error}\n")

        # thread for display loading same time of execute cmd
        thread= threading.Thread(target=loading)

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
                run(f"{virENV}\Scripts\pip.exe install {' '.join(dependencies)}")
                run(f"{virENV}\Scripts\pip3.exe freeze > requirements.txt")
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
        thread.join()
        errorExit(RED+"Error: Cancelled by user"+RESET)
    except Exception as error:
        print(error)
        threadStop= True
        thread.join()
        errorExit(error)
main()