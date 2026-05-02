# use official Python image as base
FROM python:3.11-slim

# set working directory inside the container
WORKDIR /app

# copy requirements file first (for faster builds)
COPY requirements.txt .

# install all libraries
RUN pip install --no-cache-dir -r requirements.txt

# download spacy model
RUN python -m spacy download en_core_web_sm

# copy all project files into the container
COPY . .

# tell the container which port to listen on
EXPOSE 8000

# command to start the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]