from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool
from fastapi import status
from fastapi.exceptions import HTTPException


DATABASE_CONN = "mysql+mysqlconnector://root:1234@127.0.0.1:3306/blog_db2"

engine = create_engine(DATABASE_CONN, poolclass=QueuePool, 
                       pool_size=10, max_overflow=0)

def context_get_conn():
    conn = None

    try:
        conn = engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE ,
                            detail="오류가 발생했습니다.")
    finally:
        if conn:
            conn.close()
