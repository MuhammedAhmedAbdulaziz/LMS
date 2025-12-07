import psycopg2

print("🔍 CHECKING DATABASE TABLES...")
print("=" * 50)

try:
    conn = psycopg2.connect(
        host="localhost",
        database="library",
        user="postgres", 
        password="password",
        port="5432"
    )
    cursor = conn.cursor()
    
    print("✅ Connected to PostgreSQL!")
    print()
    
    # Check all tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    
    print("📊 TABLES IN DATABASE:")
    if tables:
        for table in tables:
            print(f"   ✅ {table[0]}")
    else:
        print("   ❌ No tables found!")
        print("   💡 Run: python database.py to create tables")
    
    print()
    
    # Check if admin user exists
    cursor.execute("SELECT username, role FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    if admin:
        print(f"✅ Admin user exists: {admin[0]} (Role: {admin[1]})")
    else:
        print("❌ No admin user found!")
        
    # Count records in each table
    for table in ['users', 'books', 'transactions']:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   {table}: {count} records")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 50)