# use a minimal base image with Python 3.9 installed
FROM python:3.9-slim

# set the working directory inside the container to /app
WORKDIR /app

# copy all files from the current directory on the host to the container's /app directory
COPY . .

# install Python dependencies listed in requirements.txt
RUN pip3 install -r requirements.txt

# define the command to run the Streamlit app on port 8501 and make it accessible externally
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
