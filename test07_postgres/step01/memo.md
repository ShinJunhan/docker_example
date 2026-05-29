# test07_postgres/step01/memo.md

### postgres db 컨테이너 만들기

```bash
# 컨테이너가 실행 시에 주입되는 환경변수를 -e 옵션으로 주입해 줄 수 있다
# postgres:15 이미지를 만든 사람이 설정한 대로 환경변수를 주입해주면 알아서 동작한다
# 컨테이너 실행 시에 정해진 환경변수 값이 존재한다면 그 값에 따라서 동작이 준비된다
docker run -d \
    -p 5432:5432 \
    -e POSTGRES_USER=scott \
    -e POSTGRES_PASSWORD=tiger \
    -e POSTGRES_DB=scott_db \
    --name my-postgres \
    postgres:15

# 실행 중인 container 에 -it (인터렉티브하게) 접속해서 bash 로 들어가기
docker exec -it my-postgres /bin/bash

# container 안에 설정된 환경변수 확인해보기
echo $POSTGRES_USER
echo $POSTGRES_PASSWORD
echo $POSTGRES_DB

# DB 접속하기 (컨테이너 내부에서 접속할 때는 비밀번호를 물어보지 않는다; 이미 충분한 권한이 있다고 가정됨)
psql -U scott -d scott_db

# 접속해서 table 만들고 sample data 를 넣은 다음 외부(dbeaver) 에서 접속 테스트를 한다
CREATE TABLE member (num SERIAL PRIMARY KEY, name VARCHAR(20), addr TEXT);

INSERT INTO member (name, addr) VALUES ('kim', 'seoul');

# DB 와 container 에서 빠져나온다
scott_db=# \q 
root@6adc3551740d:/# exit

# container 정지
docker container stop my-postgres
# 정지 후에 접속 테스트를 하면 fail!

# container 다시 start 한 후에 다시 dbeaver 로 접속해서 select 하면 data 가 유지된 걸 확인할 수 있다
docker container start my-postgres

# container 를 삭제 후에 다시 run 해본다
docker container rm -f my-postgres 

# 재실행
docker run -d \
    -p 5432:5432 \
    -e POSTGRES_USER=scott \
    -e POSTGRES_PASSWORD=tiger \
    -e POSTGRES_DB=scott_db \
    --name my-postgres \
    postgres:15

# 재실행 후 DBeaver 로 접속해보면 table 이 없는 것을 알 수 있다


# 외부 volume 의 필요성이 느껴진다
# 외부 volume 만들기
docker volume create pgdata

# 만들어진 volume 목록 확인하기
docker volume ls

# 만들어진 volume 을 사용하는 container 를 다시 run 하기
docker run -d \
    -p 5432:5432 \
    -e POSTGRES_USER=scott \
    -e POSTGRES_PASSWORD=tiger \
    -e POSTGRES_DB=scott_db \
    -v pgdata:/var/lib/postgresql/data \
    --name my-postgres \
    postgres:15

# case 1 
# 처음 pgdata volume 을 만들었기 때문에 비어있는 상태
# volume 을 연결하면 container 의 /var/lib/postgresql/data 안에 있는 정보가 pgdata로 복사된다

# case 2
# cotainer 를 삭제 후 다시 run 하면 pgdata 안에 있는 정보가
# /var/lib/postgresql/data 안으로 덮어쓰기 된다

# 1. volume 을 사용하는 컨테이너에 -it 하게 접속해서 scott 계정으로 postgres db 에 들어간 다음
# 2. member table 을 만들고 sample 데이터를 insert 하고
# 3. 컨테이너를 빠져 나와서 컨테이너를 삭제 후에
# 4. 다시 동일한 volume 을 사용하는 컨테이너를 실행한다음
# 5. postgres db 에 접속해서 sample data 가 유지 되는지 확인해 해보세요.
<!--
[user1@mgmt test07_postgres]$ docker run -d \
>     -p 5432:5432 \
>     -e POSTGRES_USER=scott \
>     -e POSTGRES_PASSWORD=tiger \
>     -e POSTGRES_DB=scott_db \
>     -v pgdata:/var/lib/postgresql/data \
>     --name my-postgres \
>     postgres:15
433dd2b326c288cc23389378fa89c19dbf09ee48aac7f949856f6eacce6612d3
[user1@mgmt test07_postgres]$ docker exec -it my-postgres /bin/bash
root@433dd2b326c2:/# psql -U scott -d scott_db
psql (15.18 (Debian 15.18-1.pgdg13+1))
Type "help" for help.

scott_db=# CREATE TABLE member (num SERIAL PRIMARY KEY, name VARCHAR(20), addr TEXT);
CREATE TABLE
scott_db=# INSERT INTO member (name, addr) VALUES ('shin', 'daejeon');
INSERT 0 1
scott_db=# select * from member;
 num | name |  addr   
-----+------+---------
   1 | shin | daejeon
(1 row)

scott_db=# \q
root@433dd2b326c2:/# exit
exit
[user1@mgmt test07_postgres]$ docker container rm -f my-postgres
my-postgres
[user1@mgmt test07_postgres]$ docker run -d \
>     -p 5432:5432 \
>     -e POSTGRES_USER=scott \
>     -e POSTGRES_PASSWORD=tiger \
>     -e POSTGRES_DB=scott_db \
>     -v pgdata:/var/lib/postgresql/data \
>     --name my-postgres \
>     postgres:15
d0d0bb5deb72020a967d162359593787a54e4bb67f5cf0185a5a6bfd78408587
[user1@mgmt test07_postgres]$ docker exec -it my-postgres /bin/bash
root@d0d0bb5deb72:/# psql -U scott -d scott_db
psql (15.18 (Debian 15.18-1.pgdg13+1))
Type "help" for help.

scott_db=# select * from member;
 num | name |  addr   
-----+------+---------
   1 | shin | daejeon
(1 row)
-->

# db container 에 다른 container 가 접근 해서 data 를 insert, update, delete, select 하기 위해서는 network 설정이 필요하다

# 컨테이너를 삭제하고
docker container rm -f my-postgres

# network 를 추가로 구성하기
docker network create my-net

# network 목록 검색하기
docker network ls

# network 정보 자세히 검색하기
docker network inspect my-net

# 다시 run 하기
# 동일한 네트워크로 컨테이너가 묶이면 서로 ip 주소 대신에 컨테이너 이름으로 연결할 수 있다.
docker run -d \
    -p 5432:5432 \
    -e POSTGRES_USER=scott \
    -e POSTGRES_PASSWORD=tiger \
    -e POSTGRES_DB=scott_db \
    -v pgdata:/var/lib/postgresql/data \
    --network my-net \
    --name my-postgres \
    postgres:15

# 실행된 container 의 자세한 정보 확인해보기
docker container inspect my-postgres

# ip 주소만 따로 출력해보기
docker container inspect my-postgres | grep IPAddress
# ip 주소사 my-net network 대역의 ip 주소인 것을 알 수 있다
```