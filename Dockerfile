FROM python:3.10-slim

WORKDIR /phonebook

# Copy requirements, upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./phonebook /phonebook
