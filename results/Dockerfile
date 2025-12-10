FROM python:3.11-slim
WORKDIR .
COPY requirements.txt db_redacted_results.sqlite ./
RUN pip install --no-cache-dir -r requirements.txt


RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*


COPY print_education_level.py ./
COPY generate_frustration_figure.py ./
COPY generate_changed_strategy_figure.py ./ 
COPY generate_perceived_time_change.py ./
COPY run_all_scripts.sh ./

CMD ["bash", "run_all_scripts.sh"]
