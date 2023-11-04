FROM python:3.12

WORKDIR /app

COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["/bin/bash"]
