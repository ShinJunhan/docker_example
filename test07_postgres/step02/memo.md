# test07_postgres/step02/memo.md

### fastapi container 와 postgres container 를 동시에 만들어서 동일한 network 에서 동작하게 하기

```bash
docker network create my-net

docker volume create pgdata

docker run -d \
    -p 5432:5432 \
    -e POSTGRES_USER=scott \
    -e POSTGRES_PASSWORD=tiger \
    -e POSTGRES_DB=scott_db \
    -v pgdata:/var/lib/postgresql/data \
    --network my-net \
    --name my-postgres \
    postgres:15

# 생성된 container 에 접속해서 table 생성 및 sample 데이너 넣기
# docker exec -i my-postgres psql -U scott -d scott_db -c "실행할 sql 문"
docker exec -i my-postgres psql -U scott -d scott_db <<-EOF
    CREATE TABLE member(num SERIAL PRIMARY KEY, name VARCHAR(20), addr TEXT);
    INSERT INTO member (name, addr) VALUES ('kim', 'seoul');
    INSERT INTO member (name, addr) VALUES ('shin', 'daejeon');
EOF

# Dockerfile 을 이용해서 my-fastapi:1.0 이미지 만들기
docker build -t my-fastapi:1.0 .

# 빌드된 image 확인
docker image ls

# fast api 컨테이너 실행하기
docker run -d \
    -p 8000:8000 \
    -e DB_URL=postgresql://scott:tiger@my-postgres:5432/scott_db \
    --network my-net \
    --name my-fastapi \
    my-fastapi:1.0

# 현재 실행 중이거나 정지 중에 있는 모든 컨테이너 삭제하기
docker rm -f $(docker ps -aq)    
```