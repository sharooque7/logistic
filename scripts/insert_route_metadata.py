import json
import psycopg2
from psycopg2.extras import execute_batch
import sys
from typing import List, Dict, Any
import math

# Database configuration - UPDATE THESE!
DB_CONFIG = {
    'host': 'localhost',
    'database': 'rytle',
    'user': 'ainzson',
    'password': 'ainzson123',
    'port': '5434'
}

def parse_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Parse the JSON file and extract route and stop data"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_stops = []
    
    for route_data in data:
        # Each route_data is a dict with single key (route_id)
        for route_id, route_info in route_data.items():
            
            # Extract route metadata
            route_metadata = {
                'route_id': route_id,
                'station_code': route_info.get('station_code'),
                'date': route_info.get('date_YYYY_MM_DD'),
                'departure_time': route_info.get('departure_time_utc'),
                'executor_capacity': route_info.get('executor_capacity_cm3'),
                'route_score': route_info.get('route_score')
            }
            
            # Extract stops
            stops = route_info.get('stops', {})
            for stop_code, stop_info in stops.items():
                stop_record = {
                    'route_id': route_id,
                    'stop_code': stop_code,
                    'latitude': stop_info.get('lat'),
                    'longitude': stop_info.get('lng'),
                    'stop_type': stop_info.get('type'),
                    'zone_id': stop_info.get('zone_id')
                }
                all_stops.append(stop_record)
    
    return all_stops

def create_database_tables(conn):
    """Create the necessary tables if they don't exist"""
    cur = conn.cursor()
    
    # Create routes table first (since stops references it)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS routes (
        route_id VARCHAR(100) PRIMARY KEY,
        station_code VARCHAR(20),
        date_YYYY_MM_DD DATE,
        departure_time_utc TIME,
        executor_capacity_cm3 NUMERIC(12, 2),
        route_score VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Create stops table (you have two definitions - using the second one)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stops (
        stop_id SERIAL PRIMARY KEY,
        route_id VARCHAR(100),
        stop_code VARCHAR(10),
        lat NUMERIC(9, 6),
        lng NUMERIC(9, 6),
        type VARCHAR(20),
        zone_id VARCHAR(20),
        FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    cur.close()
    print("✅ Tables created/verified successfully")

def insert_routes(conn, file_path: str):
    """Insert route data into routes table"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cur = conn.cursor()
    
    for route_data in data:
        for route_id, route_info in route_data.items():
            # Check if route already exists
            cur.execute("SELECT route_id FROM routes WHERE route_id = %s", (route_id,))
            if not cur.fetchone():
                insert_query = """
                INSERT INTO routes 
                (route_id, station_code, date_YYYY_MM_DD, departure_time_utc, executor_capacity_cm3, route_score)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                cur.execute(insert_query, (
                    route_id,
                    route_info.get('station_code'),
                    route_info.get('date_YYYY_MM_DD'),
                    route_info.get('departure_time_utc'),
                    route_info.get('executor_capacity_cm3'),
                    route_info.get('route_score')
                ))
    
    conn.commit()
    cur.close()
    print(f"✅ Routes inserted successfully")

def insert_stops(conn, stops_data: List[Dict[str, Any]]):
    """Insert stop data in batches"""
    cur = conn.cursor()
    
    # Prepare batch insert
    insert_query = """
    INSERT INTO stops (route_id, stop_code, lat, lng, type, zone_id)
    VALUES (%(route_id)s, %(stop_code)s, %(latitude)s, %(longitude)s, %(stop_type)s, %(zone_id)s)
    """
    
    # ON CONFLICT (route_id, stop_code) DO NOTHING

    
    # Batch insert (100 records at a time)
    batch_size = 100
    for i in range(0, len(stops_data), batch_size):
        batch = stops_data[i:i + batch_size]
        execute_batch(cur, insert_query, batch)
        conn.commit()
        print(f"✅ Inserted batch {i//batch_size + 1}/{(len(stops_data)-1)//batch_size + 1}")
    
    cur.close()

def main():
    # Get file path
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = input("Enter JSON file path: ").strip()
    
    try:
        # Parse JSON file
        print("📂 Parsing JSON file...")
        stops_data = parse_json_file(json_file)
        print(f"📊 Found {len(stops_data)} stops in the JSON file")
        
        # Connect to database
        print("🔗 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        
        # Create tables
        # create_database_tables(conn)
        
        # Insert routes
        # insert_routes(conn, json_file)
        
        # Insert stops
        insert_stops(conn, stops_data)
        
        # Show summary
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM routes")
        route_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM stops")
        stop_count = cur.fetchone()[0]
        
        print("\n" + "="*50)
        print("✅ DATA INSERTION COMPLETE")
        print("="*50)
        print(f"Total routes inserted: {route_count}")
        print(f"Total stops inserted: {stop_count}")
        print(f"Average stops per route: {stop_count/route_count if route_count > 0 else 0:.1f}")
        
        # Show sample data
        cur.execute("SELECT route_id, stop_code, lat, lng, type FROM stops LIMIT 5")
        sample_stops = cur.fetchall()
        print("\n📋 Sample stops:")
        for stop in sample_stops:
            print(f"  {stop[0]}: {stop[1]} ({stop[2]}, {stop[3]}) - {stop[4]}")
        
        cur.close()
        conn.close()
        
    except FileNotFoundError:
        print(f"❌ Error: File '{json_file}' not found!")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format - {e}")
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()