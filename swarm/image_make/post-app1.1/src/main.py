from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

# 환경변수 매핑 (프록시 쓰기: 5432, 읽기: 5433)
WRITABLE_URL = os.getenv("WRITABLE_URL", "postgresql://scott:tiger@localhost:5432/scott_db")
READONLY_URL = os.getenv("READONLY_URL", "postgresql://scott:tiger@localhost:5433/scott_db")

# POST, PUT 요청으로 들어올 JSON 데이터 규격 정의
class PostCreate(BaseModel):
    writer: str
    title: str

@app.get("/")
def read_root():
    return {"message": "hello, fastapi!"}

# =====================================================================
# [READ] 전체 게시글 조회 (읽기 전용 DB)
# =====================================================================
@app.get("/posts")
def read_posts():
    conn = psycopg2.connect(READONLY_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * FROM posts ORDER BY num ASC;")
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return {"status": "success", "data": rows}

# =====================================================================
# [READ] 단일 게시글 조회 (읽기 전용 DB) - ★ 추가됨
# =====================================================================
@app.get("/posts/{num}")
def read_post(num: int):
    conn = psycopg2.connect(READONLY_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # %s 자리에 파라미터로 받은 num을 튜플 형태로 (num,) 쏙 넣습니다.
    cursor.execute("SELECT * FROM posts WHERE num = %s;", (num,))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    # 데이터가 없으면 404 에러 발생
    if not row:
        raise HTTPException(status_code=404, detail="해당 게시글을 찾을 수 없습니다.")
        
    return {"status": "success", "data": row}

# =====================================================================
# [CREATE] 게시글 등록 (쓰기 전용 DB)
# =====================================================================
@app.post("/posts")
def save_post(posts: PostCreate):
    conn = psycopg2.connect(WRITABLE_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute(
            "INSERT INTO posts (writer, title) VALUES (%s, %s) RETURNING *;",
            (posts.writer, posts.title)
        )
        new_post = cursor.fetchone()
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        
    return {"status": "success", "data": new_post}

# =====================================================================
# [UPDATE] 게시글 내용 수정 (쓰기 전용 DB) - ★ 추가됨
# =====================================================================
@app.put("/posts/{num}")
def update_post(num: int, posts: PostCreate):
    conn = psycopg2.connect(WRITABLE_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 조건에 맞는 레코드를 업데이트하고, 수정된 결과를 즉시 반환(RETURNING)
        cursor.execute(
            "UPDATE posts SET writer = %s, title = %s WHERE num = %s RETURNING *;",
            (posts.writer, posts.title, num)
        )
        updated_post = cursor.fetchone()
        
        # 수정하려는 대상이 없으면 404 에러 처리 후 롤백
        if not updated_post:
            conn.rollback()
            raise HTTPException(status_code=404, detail="수정할 게시글을 찾을 수 없습니다.")
            
        conn.commit()
        
    except HTTPException:
        raise # 404 에러는 그대로 통과시킵니다.
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        
    return {"status": "success", "data": updated_post}

# =====================================================================
# [DELETE] 게시글 삭제 (쓰기 전용 DB) - ★ 추가됨
# =====================================================================
@app.delete("/posts/{num}")
def delete_post(num: int):
    conn = psycopg2.connect(WRITABLE_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 삭제된 레코드 정보를 리턴받아 어떤 데이터가 지워졌는지 확인 가능!
        cursor.execute(
            "DELETE FROM posts WHERE num = %s RETURNING *;",
            (num,)
        )
        deleted_post = cursor.fetchone()
        
        if not deleted_post:
            conn.rollback()
            raise HTTPException(status_code=404, detail="삭제할 게시글을 찾을 수 없습니다.")
            
        conn.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        
    return {"status": "success", "data": deleted_post}