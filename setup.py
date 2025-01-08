from setuptools import setup, find_packages
from projectfastapi.main import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup( 
	name="create-app-fastapi", 
	version= version, 
	author="Ravishnu", 
	author_email="ravishnu60@gmail.com", 
	packages=find_packages(), 
    url="https://github.com/ravishnu60/create-app-fastapi.git",
	description="Library for initializing FastAPI projects - create-app-fastapi", 
	long_description_content_type="text/markdown",	
	long_description= long_description, 
	python_requires='>=3.9', 
	install_requires=[],
	entry_points ={ 
		'console_scripts': [ 
			'create-app-fastapi=projectfastapi.main:main'
		] 
	},
    keywords=['fastapi', 'fastapi project','project structure','api structure', 'python fastapi project structure']
) 
