# COMMAND CHEATSHEET — 실제 환경/README 확인 후 사용

> **Bash shell**에 입력할 명령입니다. Codex 채팅 프롬프트 입력 창에 그대로 실행 명령처럼 입력하는 것과 구분하세요. Linux 예시이며 설치 유무·권한·프로젝트 기술 스택에 따라 달라집니다.

## A. 먼저 조사

| 하고 싶은 일 | 명령 예시 | 주의 |
|---|---|---|
| 현재 위치 | `pwd` | 과제 루트인지 확인 |
| 숨김 포함 파일 | `ls -la` | Toolkit/과제 폴더 구분 |
| 일부 파일 목록 | `find . -maxdepth 2 -type f \| head -80` | 별도 유틸 설치된 경우 |
| 파일 열기 | `cat README.md` | 경로·대소문자 확인 |
| 일부만 보기 | `head -60 README.md` | 큰 파일 전체 덤프 피함 |
| 파일 검색 | `find . -name 'README*'` | 기존 문서 찾기 |
| Git 변경 | `git status --short` | Git repo일 때만 |
| Git 차이 | `git diff --stat` / `git diff` | 변경 후 확인 |
| 커밋 이력 | `git log --oneline -5` | Git repo일 때만 |
| 파이썬 버전 | `python --version` | `python3`만 있을 수도 있음 |
| Node 버전 | `node --version` / `npm --version` | 해당 스택만 |

## B. 실행 및 검증 (실제 파일 확인 후)

```bash
python path/to/script.py                 # Python 프로그램
python -m pytest -q                    # pytest 설치 및 설정된 경우
node path/to/script.js                  # Node 스크립트
npm run                                # package.json의 사용 가능한 scripts 보기
npm run dev                            # dev 스크립트가 실제 존재할 때만
curl http://localhost:PORT/            # 실제 포트와 URL 확인 후
ss -lntp                               # Linux 리스닝 포트(지원 시)
ps aux                                 # 프로세스 목록
```

FastAPI나 Uvicorn은 과제에 실제로 설치/정의된 경우에만 예컨대 `python -m uvicorn module:app --host 0.0.0.0 --port 8000`처럼 실행합니다. **`module:app`, 포트 `8000`은 임의 예시이며 시험 환경의 정답이 아닙니다.**

## C. Docker (있다고 반드시 써야 하는 것은 아님)

```bash
docker --version                         # 설치 여부
docker ps -a                             # 컨테이너 목록
docker logs <CONTAINER_NAME_OR_ID>       # 로그 확인
docker compose config                    # compose 파일 있을 때 설정 확인
```

`Dockerfile`, `compose.yaml`, README에 명시된 방식대로 빌드/실행합니다. 컨테이너 포트 매핑을 실제 설정에서 확인합니다. 이미지/컨테이너/볼륨의 차이를 알고 **파괴적인 삭제 명령은 임의로 실행하지 않습니다.**

## D. Browser Preview 확인

1. 서버를 실제 실행하고 터미널에 뜬 로그/주소 확인.
2. 서버 호스트/포트/포워딩이 플랫폼에서 어떻게 제공되는지 확인.
3. Browser Preview 또는 CLI HTTP 요청으로 **실제 화면/응답** 확인.
4. 대표 입력 1건과 잘못된 입력 1건 처리 확인.
5. 정적 HTML만 있는 경우 서버가 필요한지/파일 미리보기가 가능한지 환경 확인.

## E. 파일 공유와 충돌 회피

```bash
# Bash 1 — 파일이 없음을 확인한 경우에만
test ! -e .shared_check.tmp && printf 'shared-check\n' > .shared_check.tmp
# Bash 2 — Bash 1과 동일 프로젝트 경로에서
cat .shared_check.tmp
# Bash 1 — 내용 확인 후 자기 임시 파일만 제거
rm .shared_check.tmp
```

`rm -rf`, `git reset --hard`, `git clean -fd`, 광범위 덮어쓰기 등은 실행하지 마세요. 원본 데이터나 기존 작업물을 잃을 수 있습니다.
