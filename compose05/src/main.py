# ~/docker_example/compose05/src/main.py

from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time  # 시간 지연을 위해 추가

app = FastAPI()

# 환경 변수 로드
DB_URL = os.getenv("DB_URL", "postgresql://scott:tiger@localhost:5432/scott_db")

def get_db_connection():
    """DB가 준비될 때까지 재시도하며 연결을 시도하는 함수"""
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(DB_URL)
            return conn
        except psycopg2.OperationalError as e:
            print(f"DB 연결 실패 (남은 횟수: {retries}): {e}")
            retries -= 1
            time.sleep(3)  # 3초 대기 후 다시 시도
    raise Exception("DB 연결에 최종 실패했습니다.")

@app.get("/members")
def get_members():
    # 요청이 올 때마다 연결 확인 및 커서 생성
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("SELECT * FROM member;")
        rows = cursor.fetchall()
        return {"status": "success", "data": rows}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        conn.close()
