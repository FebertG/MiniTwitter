import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-AIA4RDO;'
        'DATABASE=MiniTwitter;'
        'Trusted_Connection=yes;'
    )
    print("Database connection successful.")
    return conn
