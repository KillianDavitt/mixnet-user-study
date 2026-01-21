FROM python:3.11-slim
WORKDIR .
COPY requirements.txt db_redacted_results.sqlite ./


RUN apt-get update && apt-get install -y sqlite3 chromium chromium-driver  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY print_education_level.py ./
COPY generate_frustration_figure.py ./
COPY generate_changed_strategy_figure.py ./ 
COPY generate_perceived_time_change.py ./
COPY statistical_tests.py ./
COPY run_likert_stats.py ./
COPY run_all_scripts.sh ./

CMD ["bash", "run_all_scripts.sh"]
