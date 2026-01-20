db="db_redacted_results.sqlite"
python3 generate_changed_strategy_figure.py $db
python3 generate_frustration_figure.py $db
python3 generate_perceived_time_change.py $db
python3 print_education_level.py $db
python3 statistical_tests.py $db
