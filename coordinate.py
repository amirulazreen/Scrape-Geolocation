from geopy.geocoders import GoogleV3
import sqlite3 
import key

geolocator = GoogleV3(api_key=key.api_key)

def coor():
    conn = sqlite3.connect('subway.db')
    cursor = conn.cursor()

    adds = [
        '''
        ALTER TABLE store
        ADD COLUMN latitude REAL;
        ''',
        '''
        ALTER TABLE store
        ADD COLUMN longitude REAL;
        '''
    ]

    for add in adds:
        cursor.execute(add)

    cursor.execute("SELECT name, address FROM store")
    rows = cursor.fetchall()

    for row in rows:
        address = row[1] if row[1] else row[0]  
        location = geolocator.geocode(address)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            cursor.execute("UPDATE store SET latitude = ?, longitude = ? WHERE address = ?", (latitude, longitude, row[1]))
    
    conn.commit()
    conn.close()
    print("Coordinate added")













