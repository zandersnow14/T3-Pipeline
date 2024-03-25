FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY database.py .
COPY filters.py .
COPY main.py .
COPY visualisations.py .
COPY .streamlit/config.toml /.streamlit/

CMD streamlit run main.py --server.port=1243

