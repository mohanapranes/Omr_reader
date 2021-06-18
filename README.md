Description: This is a omr reader takes the input of answer sheets and evalute with the normal one and will give you the results 

Status: Completed. 

Clone Repo: https://github.com/MOHANAPRANESWARAN/Omr_reader.git

# Then run the follwing to setup environment:

$ cd omrreader

$ sudo apt install uvicorn

$ python3 -m venv env

$ source env/bin/activate

$ pip3 install requirements.txt

# Start uvicorn server:

$ uvicorn main:app --reload  

# Openup your @ http://localhost:8000/

Note:This will take only certain pattern of omr types 
