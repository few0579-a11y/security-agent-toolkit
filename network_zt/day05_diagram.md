# day05 경보 판단

## 이상한 줄
- 줄 번호(여러 개면 모두):
2  03:12  192.0.2.7    → DB  3306   permit
3  03:13  192.0.2.7    → DB  3306   permit

- 이유:
DB는 INSIDE 구역에 있으므로 인터넷에서
  DB의 3306 포트로 직접 접근해서는 안 된다.
  하지만 해당 접속이 permit으로 허용되었다.

## 고친 구성도
```
INTERNET ──── FW ──┬── DMZ    : WEB (443 open)
                   └── INSIDE : DB  (3306 from WEB only)
```
