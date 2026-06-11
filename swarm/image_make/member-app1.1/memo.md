# /swarm/image_make/memo.md

### Restful API

#### 요청방식
- GET       -> 컨텐츠를 가져오기 위한 목적
- POST      -> 컨텐츠를 전송하기 위한 목적
- PATCH     -> 컨텐츠를 일부 수정하기 위한 목적
- PUT       -> 컨텐츠를 전체 수정하기 위한 목적
- DELETE    -> 컨텐츠를 삭제하기 위한 목적

#### 요청 방식과 요청 경로를 같이 조합해서 정리
GET     /members    -> 회원 전체 목록 가져오기 요청
GET     /members/1  -> 1번 회원정보 가져오기 요청
POST    /members    -> 회원 정보 추가하기
PATCH   /members/1  -> 1번 회원정보 일부 수정하기 요청
PUT     /members/1  -> 1번 회원정보 전체 수정하기 요청
DELETE  /members/1  -> 1번 회원정보 삭제하기 요청

```bash
# 이미지를 빌드하고 docker hub 에 올리기
docker build -t junhanshin/member-app:1.1 .

docker push junhanshin/member-app:1.1
```