from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

DATABASE_CONN = "mysql+mysqlconnector://root:1234@127.0.0.1:3306/test_db2"


engine = create_engine(DATABASE_CONN, poolclass=QueuePool, 
                       pool_size=10, max_overflow=0)

try:
    conn = engine.connect()
    print(conn)
except SQLAlchemyError as e:
    print(e)
finally:
    conn.close()
