import json
import psycopg2
from psycopg2.extras import execute_batch
import sys

def insert_actual_sequences(file_path):
    """
    Parse JSON file with actual route data and insert into database.
    JSON format: [{"RouteID_uuid": {"actual": {"stop_code": sequence, ...}}}, ...]
    """
    
    # 1. Read JSON file
    print(f"📁 Reading file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Successfully loaded {len(data)} route entries")
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return
    
    # 2. Database connection
    try:
        conn = psycopg2.connect(
            dbname="rytle",      # Change this
            user="ainzson",        # Change this  
            password="ainzson123",    # Change this
            host="localhost",
            port="5434"
        )
        cursor = conn.cursor()
        print("✅ Connected to database")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # 3. Process each route in the JSON
    total_routes = 0
    total_stops = 0
    skipped_routes = []
    
    for route_item in data:
        for route_id_full, route_info in route_item.items():
            # Extract clean route_id (remove 'RouteID_' prefix if present)
            if route_id_full.startswith('RouteID_'):
                route_id = route_id_full
            else:
                route_id = route_id_full
            
            print(f"\n🔍 Processing route: {route_id}")
            
            # Check if route exists in routes table
            cursor.execute("SELECT 1 FROM routes WHERE route_id = %s", (route_id,))
            if not cursor.fetchone():
                print(f"   ⚠ Skipping: Route {route_id} not found in routes table")
                skipped_routes.append(route_id)
                continue
            
            # Get actual sequence data
            if 'actual' not in route_info:
                print(f"   ⚠ Skipping: No 'actual' data for route {route_id}")
                skipped_routes.append(route_id)
                continue
            
            actual_sequences = route_info['actual']
            
            # Prepare batch insert data
            batch_data = []
            for stop_code, sequence in actual_sequences.items():
                batch_data.append((route_id, stop_code, sequence))
            
            # 4. Insert into database
            if batch_data:
                try:
                    # Create table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS actual_route_sequence (
                            id SERIAL PRIMARY KEY,
                            route_id VARCHAR(50) REFERENCES routes(route_id) ON DELETE CASCADE,
                            stop_code VARCHAR(10) NOT NULL,
                            actual_sequence INTEGER NOT NULL,
                            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE (route_id, stop_code)
                        )
                    """)
                    
                    # Insert with conflict handling
                    execute_batch(cursor, """
                        INSERT INTO actual_route_sequence (route_id, stop_code, actual_sequence)
                        VALUES (%s, %s, %s)
                    """, batch_data)
                    
                    total_routes += 1
                    total_stops += len(batch_data)
                    print(f"   ✅ Inserted {len(batch_data)} stops for route {route_id}")
                    
                except Exception as e:
                    print(f"   ❌ Error inserting route {route_id}: {e}")
                    conn.rollback()
                    continue
            else:
                print(f"   ⚠ No stops to insert for route {route_id}")
    
    # 5. Commit and close
    conn.commit()
    cursor.close()
    conn.close()
    
    # 6. Print summary
    print("\n" + "="*50)
    print("📊 INSERTION SUMMARY")
    print("="*50)
    print(f"Total routes processed: {total_routes}")
    print(f"Total stops inserted: {total_stops}")
    
    if skipped_routes:
        print(f"\n⚠ Skipped routes ({len(skipped_routes)}):")
        for route in skipped_routes:
            print(f"  - {route}")
    
    print(f"\n✅ Database insertion completed!")

def main():
    """Main function to handle command line arguments"""
    
    if len(sys.argv) < 2:
        print("Usage: python insert_routes.py <json_file_path>")
        print("Example: python insert_routes.py actual_routes.json")
        return
    
    file_path = sys.argv[1]
    insert_actual_sequences(file_path)

if __name__ == "__main__":
    main()