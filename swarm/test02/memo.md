# swarm/test02/memo.md

### cluster 환경에 배포할 이미지는 docker container 레지스트리(docker hub 등) 에 미리 등록이 되어 있어야 한다.

```bash

# 클러스터에 사용할 이미지를 빌드해서
docker build -t junhanshin/swarm-fastapi:1.0 .

# docker hub 에 미리 올려 놓기
docker push junhanshin/swarm-fastapi:1.0

```

### docker stack 실행하기

```bash
# 배포하기
docker stack deploy -c docker-stack.yaml my-app

# 거부 사유 확인
docker service ps --no-trunc my-app_swarm-fastsapi

# 서비스가 정말 잘 돌아가고 있는지 확인
docker service ls
docker service ps my-app_swarm-fastsapi | grep Running


# 버전 up 이미지 빌드하기
docker build -t junhanshin/swarm-fastapi:1.1 .

# 버전 up 된 것 docker hub 에 push
docker push junhanshin/swarm-fastapi:1.1

# 새로운 버전으로 다시 배포하기
docker stack deploy -c docker-stack.yaml my-app

```