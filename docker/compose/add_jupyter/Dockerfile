FROM jupyter/scipy-notebook:latest

USER jovyan

# Copy requirements và cài đặt Python packages
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

# Tạo thư mục work
WORKDIR /home/jovyan/work
