python3 src/call_api.py
spark-submit --master "local[*]" --py-files src/congestion_model.py src/main.py