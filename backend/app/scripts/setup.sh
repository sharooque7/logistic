#!/bin/bash
# backend/app/scripts/setup.sh

echo "Waiting for database..."
sleep 5

echo "Inserting mock data..."
cd /app/app/scripts/mock
python3 insert_route_metadata.py route_data.json
python3 insert_actual_sequence_data.py actual_sequences.json

echo "Data insertion complete!"