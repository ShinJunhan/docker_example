# test07_postgres/step03/memo.md

### postgres db 백업 및 복구 예제

```bash

# clear
docker container rm -f my-postgres 2>/dev/null
docker volume rm pgdata 2>/dev/null

# 외부 볼륨 생성
docker volume create pgdata

# container 실행
docker run -d \
    -p 5432:5432 \
    -e POSTGRES_USER=scott \
    -e POSTGRES_PASSWORD=tiger \
    -e POSTGRES_DB=scott_db \
    -v pgdata:/var/lib/postgresql/data \
    --name my-postgres \
    postgres:15


# sample data 적재
docker exec -i my-postgres psql -U scott -d scott_db <<-EOF
    CREATE TABLE member(num SERIAL PRIMARY KEY, name VARCHAR(20), addr TEXT);
    INSERT INTO member (name, addr) VALUES('kim', 'seoul');
    INSERT INTO member (name, addr) VALUES('lee', 'pusan');
EOF

# backup
docker exec -i my-postgres pg_dump -U scott -d scott_db > ./backup.sql

# container 와 volume 삭제
docker container rm -f my-postgres
docker volume rm pgdata

# 복구
# 볼륨 다시 만들고
docker volume create pgdata

# container 다시 실행
docker run -d \
    -p 5432:5432 \
    -e POSTGRES_USER=scott \
    -e POSTGRES_PASSWORD=tiger \
    -e POSTGRES_DB=scott_db \
    -v pgdata:/var/lib/postgresql/data \
    --name my-postgres \
    postgres:15

# 백업 장부를 밀어 넣기
docker exec -i my-postgres psql -U scott -d scott_db < ./backup.sql

# 확인
docker exec -i my-postgres psql -U scott -d scott_db -c "SELECT * FROM member;"
```