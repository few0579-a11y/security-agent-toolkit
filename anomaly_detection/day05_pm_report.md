# 4과목 Day 5 도커 컴포즈로 서버 두 대 켜기 · 웹 서버 로그 만들기 · 오후 (유지민 · 2026-11-06(금))

> **쓰는 법**
> - 문제를 풀 때마다 그 문제 제목 아래 질문에 답합니다.
> - 질문마다 `쓸 내용:` 에 무엇을 쓰면 되는지 적혀 있습니다. 그대로 `답:` 뒤에 씁니다.
> - 출력이나 코드를 붙여 넣는 질문은 `답:` 아래 빈 코드 상자에 붙여 넣고, 설명은 `답:` 뒤에 씁니다.
> - 「왜」를 묻는 질문은 한 단어로 끝내지 말고, 내 화면에서 본 값이나 배운 내용을 근거로 이유까지 씁니다.
> - 🔍 는 이 교시에서 꼭 알아야 할 핵심 질문입니다. 답을 못 찾았으면 「모름 — 막힌 곳: …」 이라고 씁니다. 🔍 가 없는 질문도 못 적으면 같은 말을 씁니다.

---

## 5교시 · 도커 복습 · 컴포즈로 서버 두 대 한 번에 켜기

### 문제 5-1 · 서버 한 대를 복습하고 컴포즈로 두 대 켜기

- (가) 5교시 순서의 서버 켜기 · 확인 명령(`docker images` 부터 `curl` 까지)과 그 결과를 친 순서대로 붙여 넣고, 서비스 이름 두 개와 각 서비스의 포트를 적어 주세요.
  - 쓸 내용: ① 명령과 결과를 친 순서대로(코드 상자에 붙여 넣기): `docker images` · `docker run` · `docker ps` · `docker stop` · `docker compose up -d` · `docker compose ps` · `curl` 두 개 (`docker pull` 은 받았을 때만, `pwd` · `touch` · `ls` 는 붙이지 않아도 됩니다) ② 서비스 이름 두 개 ③ 각 서비스의 포트
  - 답: 서비스 이름 web1 · web2. 포트는 web1 = 8090(원래 8080 이지만 이 PC 에서 Oracle 리스너 TNSLSNR 이 8080 을 쓰고 있어 8090 으로 바꿈), web2 = 8081. 두 서버 모두 docker compose ps 에서 Up, curl 결과 200.
  - 막힌 곳: docker run -p 8080:80 이 `bind: Only one usage of each socket address` 로 실패. docker ps 에는 8080 을 쓰는 컨테이너가 없었고, netstat · PowerShell(Get-NetTCPConnection) 로 찾아보니 Oracle TNSLSNR(PID 6572)이 8080 을 쓰고 있었다. 오라클 서비스는 끄지 않고 compose 파일의 web1 왼쪽 번호만 8090 으로 바꿨다.

```
$ docker images nginx:1.28
IMAGE        ID             DISK USAGE   CONTENT SIZE   EXTRA
nginx:1.28   146adea4768b        240MB         65.8MB
$ docker run -d --rm -p 8080:80 --name web-run nginx:1.28
1392ac4cf62c277f7ca9a286d5eed4c379e397fb223fae4aed85ed1d3b16f069
docker: Error response from daemon: ports are not available: exposing port TCP 0.0.0.0:8080 -> 127.0.0.1:0: listen tcp 0.0.0.0:8080: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.
(→ 8080 은 Oracle TNSLSNR(PID 6572)이 사용 중이라 8090 으로 바꿔 다시 진행)
$ docker ps --filter publish=8090
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
$ docker run -d --rm -p 8090:80 --name web-run nginx:1.28
a7ceb336839117ddf8ce947220a6e950ee773c1b57ebd682aafeb1cceed78617
$ docker ps
CONTAINER ID   IMAGE        COMMAND                   CREATED        STATUS        PORTS                                     NAMES
a7ceb3368391   nginx:1.28   "/docker-entrypoint.…"   1 second ago   Up 1 second   0.0.0.0:8090->80/tcp, [::]:8090->80/tcp   web-run
$ docker stop web-run
web-run
$ docker compose up -d
[+] up 3/3
 ✔ Network anomaly_detection_default  Created     0.0s
 ✔ Container anomaly_detection-web2-1 Started     0.9s
 ✔ Container anomaly_detection-web1-1 Started     0.6s
$ docker compose ps
NAME                       IMAGE        COMMAND                   SERVICE   CREATED         STATUS         PORTS
anomaly_detection-web1-1   nginx:1.28   "/docker-entrypoint.…"   web1      3 seconds ago   Up 2 seconds   0.0.0.0:8090->80/tcp, [::]:8090->80/tcp
anomaly_detection-web2-1   nginx:1.28   "/docker-entrypoint.…"   web2      3 seconds ago   Up 2 seconds   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp
$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8090
200
$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8081
200
```

- (나) 🔍 서버 두 대를 `docker run` 으로 켜는 것과 `compose.yaml` 과 `docker compose up -d` 로 켜는 것을 비교해, 컴포즈가 더 나은 점을 두 가지 적어 주세요.
  - 쓸 내용: ① 컴포즈가 더 나은 점 두 가지
  - 답: ① 긴 옵션(이미지 버전 · 포트 · 재시작 설정)을 파일에 적어 두어서 누가 켜도 같은 서버가 켜지고, 한 군데 틀릴 일이 없다. ② docker compose up -d 한 줄로 두 대를 한 번에 켜고 끌 수 있고, 파일을 저장소에 올리면 설정 기록이 남는다. `(B/C — 정답 요지)`

- (다) 🔍 보안 사고가 난 뒤 감사팀이 「사고 당시와 같은 구성으로 서버를 다시 켜 보라」고 요청했습니다. 팀원 한 명은 3주 전에 긴 `docker run` 명령을 직접 쳐서 서버를 켰는데 그 명령을 기억하지 못합니다. 다른 팀은 `compose.yaml` 을 깃허브에 올려 두었습니다. 두 팀이 같은 구성을 다시 켤 수 있는지 비교하고, 파일에 `nginx:1.28` 처럼 버전을 적어 두는 것이 이런 재현에 왜 중요한지 적어 주세요.
  - 쓸 내용: ① 두 팀의 차이 ② 버전을 적어 두는 것이 재현에 중요한 이유
  - 답: docker run 팀은 3주 전 명령을 기억하지 못하면 포트 · 이름 · 이미지 버전을 알 수 없어 같은 구성을 다시 켤 수 없고 기록도 없다. compose 팀은 깃허브의 compose.yaml 로 docker compose up -d 한 줄이면 같은 구성을 다시 켤 수 있다. 버전(nginx:1.28)을 적어 두면 몇 주 뒤에도 같은 버전으로 켜서 사고 당시와 같은 환경이 되지만, nginx 처럼 이름만 적으면 최신 버전을 받아 동작이 달라져 재현 결과를 믿기 어렵다. `(B/C — 정답 요지)`

- (라) 🔍 팀원 세 명이 같은 `compose.yaml` 로 서버를 켰는데 한 명의 PC 에서만 `8081` 번 포트를 다른 프로그램이 쓰고 있어서 `web2` 가 켜지지 않았습니다. 이 사람이 파일의 어느 줄을 어떻게 바꾸면 되는지 적고, 바꿔도 서버 안에서는 여전히 `80` 번 포트로 동작하는 이유를 적어 주세요. 이 사람이 `curl` 로 확인할 때 달라지는 점도 적어 주세요.
  - 쓸 내용: ① 바꿀 줄과 바꾼 모양 ② 서버 안은 그대로 80 인 이유 ③ curl 주소의 달라지는 점
  - 답: 실제로 내 PC 에서 겪은 일이다. 8080 을 Oracle 리스너가 쓰고 있어서 web1 의 `- "8080:80"` 을 `- "8090:80"` 으로 왼쪽 숫자만 바꿨다(8081 이 막힌 경우라면 web2 의 `- "8081:80"` 의 왼쪽을 빈 번호로 바꾼다). 콜론 왼쪽은 내 컴퓨터의 포트, 오른쪽은 서버(컨테이너) 안의 포트라서 왼쪽만 바꾸면 서버 안은 그대로 80 이다. curl 은 바꾼 왼쪽 번호로 쳐야 한다: http://localhost:8090 (다른 팀원은 그대로 8080). `(B — 실제 겪은 일을 Claude 가 정리)`

## 6교시 · 서버마다 접속 범위 정하기 · 설정 바꿔 적용하기

### 문제 6-1 · 서버마다 접속 범위를 정해 컴포즈 파일로 적용하기

- (가) 1번과 5번의 `docker compose ps` 출력을 붙여 넣고, 접속 범위가 바뀐 기존 서비스와 새로 추가된 서비스를 따로 적어 주세요.
  - 쓸 내용: ① 1번 출력(코드 상자에 붙여 넣기) ② 5번 출력(코드 상자에 붙여 넣기) ③ 접속 범위가 바뀐 기존 서비스 ④ 새로 추가된 서비스
  - 답: 1번 출력(5교시 상태)은 web1 · web2 모두 `0.0.0.0:` 으로 시작했고, 5번 출력에서는 web1 만 `0.0.0.0:8090` 그대로이고 web2 · web3 은 `127.0.0.1:` 로 시작한다. ③ 접속 범위가 바뀐 기존 서비스: web2 (0.0.0.0:8081 → 127.0.0.1:8081) ④ 새로 추가된 서비스: web3 (127.0.0.1:8082, logs 폴더 볼륨 연결). curl 세 번 모두 200.
  - 참고: 아래 코드 상자의 up -d 출력이 세 서버 모두 `Running` 인 것은, 약 50분 전에 이미 한 번 적용(그때 web2 Recreated · web3 Created)한 뒤 같은 명령을 다시 쳤기 때문이다. 설정이 바뀌지 않았으니 모두 그대로 둔 것. 첫 적용 때의 출력은 남겨 두지 못했다.

1번 출력 (5교시 `docker compose ps`, 적용 전):

```
NAME                       IMAGE        COMMAND                   SERVICE   CREATED         STATUS         PORTS
anomaly_detection-web1-1   nginx:1.28   "/docker-entrypoint.…"   web1      3 seconds ago   Up 2 seconds   0.0.0.0:8090->80/tcp, [::]:8090->80/tcp
anomaly_detection-web2-1   nginx:1.28   "/docker-entrypoint.…"   web2      3 seconds ago   Up 2 seconds   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp
```

5번 출력 (적용 후, 다시 실행한 명령 포함):

```
$    docker compose ps
   docker compose -f compose.secure.yaml up -d
   docker compose -f compose.secure.yaml ps
   curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8090
   curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8081
   curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8082
NAME                       IMAGE        COMMAND                   SERVICE   CREATED             STATUS             PORTS
anomaly_detection-web1-1   nginx:1.28   "/docker-entrypoint.…"   web1      About an hour ago   Up About an hour   0.0.0.0:8090->80/tcp, [::]:8090->80/tcp
anomaly_detection-web2-1   nginx:1.28   "/docker-entrypoint.…"   web2      51 minutes ago      Up 50 minutes      127.0.0.1:8081->80/tcp
anomaly_detection-web3-1   nginx:1.28   "/docker-entrypoint.…"   web3      51 minutes ago      Up 51 minutes      127.0.0.1:8082->80/tcp
[+] up 3/3
 ✔ Container anomaly_detection-web1-1 Running                                                                                                     0.0s
 ✔ Container anomaly_detection-web2-1 Running                                                                                                     0.0s
 ✔ Container anomaly_detection-web3-1 Running                                                                                                     0.0s
NAME                       IMAGE        COMMAND                   SERVICE   CREATED             STATUS             PORTS
anomaly_detection-web1-1   nginx:1.28   "/docker-entrypoint.…"   web1      About an hour ago   Up About an hour   0.0.0.0:8090->80/tcp, [::]:8090->80/tcp
anomaly_detection-web2-1   nginx:1.28   "/docker-entrypoint.…"   web2      51 minutes ago      Up 51 minutes      127.0.0.1:8081->80/tcp
anomaly_detection-web3-1   nginx:1.28   "/docker-entrypoint.…"   web3      51 minutes ago      Up 51 minutes      127.0.0.1:8082->80/tcp
200
200
200
```

- (나) 🔍 `"8081:80"` 과 `"127.0.0.1:8081:80"` 은 누가 접속할 수 있는지가 어떻게 다른가요? 관리 화면이나 데이터베이스 서버를 이렇게 설정하는 이유도 적어 주세요.
  - 쓸 내용: ① 두 포트 줄에서 누가 접속할 수 있는지의 차이 ② 관리 화면 · 데이터베이스를 이렇게 설정하는 이유
  - 답: `"8081:80"` 은 앞에 주소가 없어서 0.0.0.0(모든 네트워크 카드)으로 열려, 같은 네트워크의 다른 PC 도 접속할 수 있다. `"127.0.0.1:8081:80"` 은 127.0.0.1(내 PC 자신)에서만 받으므로 내 PC 에서만 접속된다. 관리 화면 · 데이터베이스는 필요한 사람만 쓰는 서버라, 밖에 열어 두면 스캐너가 /phpmyadmin 같은 주소를 찾아 들어오려 할 수 있으므로 꼭 열어야 하는 서버만 열고 나머지는 127.0.0.1 로 제한한다. (실제로 이 PC 의 Oracle 리스너도 0.0.0.0:8080 으로 열려 있었다.) `(A — 처음 답이 반대여서 Claude 가 고쳐 씀, 막힌 곳 참고)`
  - 막힌 곳: 처음에 두 줄의 뜻을 반대로 이해했다("8081:80" 이 로컬 전용, 127 로 시작하는 쪽이 같은 네트워크까지 허용이라고 생각함). 주소를 안 적으면 0.0.0.0 = 모두에게 열림, 127.0.0.1 = 나 자신만 이라는 것을 ps 의 PORTS(0.0.0.0:8081 / 127.0.0.1:8081)로 확인했다.

- (다) 🔍 `up -d` 의 출력에서 `web1` 은 `Running`, `web2` 는 `Recreated`, `web3` 은 `Created` 였습니다. 서버마다 출력이 다른 이유와, 운영 중인 서비스의 설정을 바꿀 때 이것이 왜 도움이 되는지 적어 주세요.
  - 쓸 내용: ① 서버마다 출력이 다른 이유 ② 서버를 끊지 않고 바꿀 수 있는 것의 쓸모
  - 답: web1 은 compose.yaml 과 설정이 같아서 그대로 둔 것(Running), web2 는 포트 줄이 "127.0.0.1:8081:80" 으로 바뀌어 기존 컨테이너를 새 설정으로 다시 만든 것(Recreated), web3 은 파일에 새로 추가된 서버라 새로 만든 것(Created)이다. 설정을 바꿔도 바뀐 서버만 다시 만들어지고 web1 은 끊기지 않으므로, 운영 중인 서비스를 멈추지 않고 보안 설정을 고칠 수 있다. (같은 명령을 한 번 더 치면 이번엔 바뀐 게 없으니 세 서버 모두 Running 으로 나온다 — 내 두 번째 실행 결과가 그 모습이다.) `(B/C — 정답 요지)`

### 마무리 · 오늘 만든 것을 깃허브에 올리기

- (가) `git status` 를 쳤을 때 `.env` 나 `.venv` 가 보였는지, 보였다면 어떻게 했는지 적어 주세요.
  - 쓸 내용: ① `.env` · `.venv` 가 보였는지 ② 보였다면 한 조치
  - 답: git status 의 Untracked files 에 .env · .venv 는 보이지 않았다(오늘 만든 day05 파일 · compose 파일 2개 · json 3개 · logs/ 폴더만 보임). 그래서 .gitignore 는 고치지 않고 그대로 올렸다.
