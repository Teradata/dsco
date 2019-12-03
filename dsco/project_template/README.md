# Data science development container  

## Dependencies  
Install:  
- docker: https://www.docker.com/products/docker-desktop  
- cookiecutter: `pip install cookiecutter`    

## Create project  
Initiate a project with:    
`cookiecutter git+https://github.td.teradata.com/Quality-Engineering/data_science_template`    

This will prompt you for a project name that will be used to create a directory 
that will contain your initial project structure.

The template will be downloaded and stored in ~/.cookiecutters.  
To initiate future projects you can just run:  
`cookiecutter data_science_template`    

## Quickstart  
From a bash shell in your newly created project directory run:    
`./bin/dscogo`  

This should result in a browser window opening with more directions.  
