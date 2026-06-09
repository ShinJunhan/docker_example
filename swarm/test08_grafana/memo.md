# swarm/test08_grafana/memo.md

### docker swarm 환경에서 prometheus 와 grafana 사용하기

```bash
# prometheus.yaml & docker-stack-monitor.yaml 파일 생성
tree
.
├── docker-stack-monitor.yaml
├── memo.md
└── prometheus.yaml

# monitor-app 이라는 이름으로 배포하기
docker stack deploy -c docker-stack-monitor.yaml monitor-app

# portainer 확인 (admin/admin11111111)
http://172.16.8.200:9443

# grafana 확인 (admin/admin)
http://172.16.8.200:3000

```