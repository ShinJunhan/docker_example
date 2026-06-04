# compose05/memo.md

### test07_postgres/step02 폴더 안의 내용을 가져와서 동일한 동작을 하는 docker-compose.yaml 파일을 만들어서 테스트

```bash

# docker compose 환경에서 exec 실행하기
# docker compose exec -T <서비스명> <실행명령>
docker compose exec -T my-postgres psql -U scott -d scott_db <<-EOF
    CREATE TABLE member(num SERIAL PRIMARY KEY, name VARCHAR(20), addr TEXT);
    INSERT INTO member (name, addr) VALUES ('kim', 'seoul');
    INSERT INTO member (name, addr) VALUES ('shin', 'daejeon');
EOF

docker compose exec -T my-postgres psql -U scott -d scott_db <<-EOF
    SELECT * FROM member;
EOF

# 간단한 모니터링을 할 수 있는 컨테이너 (portainer) 띄우기
docker run -d -p 8001:8000 -p 9001:9000 --name portainer --restart=always \
   -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data \
   portainer/portainer-ce:latest

# 실행 후에 외부 웹브라우저에서 아래의 주소로 요청하기
http://<node ip>:9001
http://172.16.8.200:9001


```