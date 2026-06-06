# swarm/test01/memo.md

### docker swarm 클러스터 구성하기

```bash
# master node (mgmt) 에서 실행
docker swarm init --advertise-addr 172.16.8.200

# worker node 로 설정하고 싶은 노드 (rocky01, rocky02) 에서 실행
docker swarm join --token SWMTKN-1-0ck5gq9s6ri7g6qjb8wokwe8q2gs89tpkdgghorijps8oriorh-9cgjs3vhlzelsdwm1suy41txk 172.16.8.200:2377

# 클러스터 상태 조회
docker node ls

# 클러스터에 테스트로 nginx 컨테이너 3개 배포하기
docker service create --name my-web --replicas 1 -p 8080:80 nginx

# 서비스 확인
docker service ls

# 어디에 떠 있는지 확인
docker service ps my-web

# 서비스에서 돌아가는 컨테이너의 갯수를 동적으로 늘리거나 줄이기
docker service scale my-web=3
docker service scale my-web=1

# 서비스 제거
docker service rm my-web

# 조인 토큰 정보 다시 확인하기
docker swarm join-token worker

```