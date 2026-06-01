# compost01/memo.md

### docker compose 활용해보기

> vs code 에 container tool 을 설치하면 좀 더 편하게 작업할 수 있다

```bash
# docker-compose.yaml 파일을 만들고 해당 파일이 존재하는 폴더에서 아래의 명령어를 입력한다

docker compose up       # container 를 foreground 에서 실행
docker compose up -d   # container 를 detach 모드(background) 에서 실행

# 실행 중인 compose 목록 검색
docker compose ls

# 실행 중인 container 확인
docker container ls

# compose 실행 중지 (container, default network 가 삭제된다 )
docker compose down

# 변경된 소스코드를 반영하여 새로 빌드한 뒤 가동
docker compose up -d --build

# 컨테이너를 삭제하지 않고 일시정지 
docker compose stop

# 일시 정지 되었던 컨테이너를 다시 시작
docker compose start

# 서비스를 안전하게 껐다가 다시 켬(재부팅)
docker compose restart

# 컨테이너와 자동 생성된 네트워크를 파괴 및 철거
docker compose down

# volume 정도보 같이 제거
docker compose down -v

# 현재 폴더에 속한 컨테이너의 상태 확인
docker compose ps

# 로그 확인
docker compose logs

# compose 가 생성하거나 사용 중인 이미지 목록
docker compose images

# docker-compose.yaml 파일이 아닌 다른 파일 my-compose.yaml 등의 파일을 이용해서 up 또는 down 
docker compose up -f my-compose.yaml
docker compose down -f my-compose.yaml
docker compose stop -f my-compose.yaml
```