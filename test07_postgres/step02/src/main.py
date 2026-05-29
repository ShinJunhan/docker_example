# ~/docker_example/test07_postgres/step02/src/main.py

# app.py
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

"""
    환경 변수에 있는 값을 os.getenv() 를 이용해서 얻어낼 수 있다.

    os.getenv(<환경변수명>, <해당 환경변수가 없을 때 default 로 사용할 값)

    개발환경에서는 환경변수 없이 개발환경에 맞는 db 접속 url 을 기본 값으로 넣어서 사용하면 된다

    docker container 를 실행할 때 아래와 같은 형식으로 환경변수를 전달할 예정
    (예시) docker run -e DB_URL = postgresql://scott:tiger@<db 컨테이너명>:5432/scott_db
    (실례) docker run -e DB_URL = postgresql://scott:tiger@my-postgres:5432/scott_db
"""

# 5432 포트로 뚫어놓은 도커 DB 매핑
DB_URL = os.getenv("DB_URL", "postgresql://scott:tiger@localhost:5432/scott_db")

@app.get("/members")
def get_members():
    # 데이터베이스 장부 연결 및 커서 개설 (딕셔너리 형태로 변환 래핑)
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # member 레코드 긁어오기
    cursor.execute("SELECT * FROM member;")
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return {"status": "success", "data": rows}
