FROM python:3.10
WORKDIR /app/Mountain-Peaks
COPY ./mountain_peaks ./mountain_peaks
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#CMD ["uvicorn", "mountain_peaks.main:app", "--host", "0.0.0.0", "--port", "80"]