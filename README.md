# CAG_SE2022 - Zube Analysis

# Senior Project -  Group (# Syntax Error #)

*Team Members:*  
`Sujoy paul dakkumalla`  
`Uma Devi Bontha`  
`Pranavi Guttikonda`     
`Sai Kaushik Peesari`    
`Sai Vineeth Venkatratna`


### Program description ###

1. Required tools & platforms:
   - Windows 10 Preferred
   - Python (Latest) 
      - Install `Python`(Latest) using below link
              
            https://www.python.org/downloads/
     
        ![Python version check image](relative/path/to/img.jpg?raw=true "Title")
      <br><br>
      - Install `Visual Studio` Code
   
            https://code.visualstudio.com/download
     <br>
   
2. Required Python modules (Can refer to `requirements.txt` for full list)

   - cryptography==38.0.1
   - Flask==2.2.2
   - Jinja2==3.1.2
   - matplotlib==3.5.3
   - numpy==1.23.4
   - pandas==1.4.4
   - pandas-profiling==3.3.0
   - PyJWT==2.6.0
   - requests==2.28.1
   - seaborn==0.11.2
   - Werkzeug==2.2.2
<br> <br>
3. Download the `<Need to add the parent folder name>` folder and make sure `FlaskAPI`, `secrets`, `main.py` is in the same path/folder.
 <br> <br>
4. Now; open the above downloaded folder in VS-Code; 

            Go to File >>> `Open Folder` & select the downloaded project folder.

5. Create Python environment
   - Go to VS-Code &ensp; >>> &ensp;  Click on `view` &ensp; >>> &ensp; CLick on `Terminal`,
   - Run `dir` command to see the list of folders anf files mentioned in the `step-3`
     - if you are not able to see it, then navigate to the folder where those files locate using `cd` command
   - Run below highlighted command to create your python environment.
   
         python -m venv <env-name>
   
   - then, activate the environment using below command:
      
         .\<env-name>\Scripts\activate
   - Now; you should see the created python environment prompt on your terminal.
   - Once activate; here you can install required python packages from `step-2`
   
         pip install -r requirements.txt

### Execution Steps ###

1. To start this Web-App; you need to execute the `main.py` using python command
       
       python ./main.py
       
   *[**Note:** you will see the Flask App running on the local host with default port 5000*


![Flask output image](relative/path/to/img.jpg?raw=true "Title")


2. Now, Click on the shown http link (*ctrl + left click*)

**End Of File**