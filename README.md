# AI Hackathon Lean Toolkit v2.0

> **목적:** 3시간 안팎의 실무형 AI 과제에서 `요구사항 파악 → 데이터 검사 → 업무 규칙 → 최소 기능 개발 → 독립 검증 → 실행·제출`을 빠뜨리지 않도록 돕는 **사전 준비용 공개 보조 도구**.
>
> **정답, 시험 과제, 회사 데이터, 사전 완성된 업무 앱은 포함하지 않습니다.** 공식 과제 지시/README/대회 규정이 이 문서보다 우선합니다.

## 핵심 결론: 전체를 읽지 마세요

- **시험 시작:** `QUICK_START.md`만 먼저 읽습니다. AI에게 `AGENTS.md`를 **명시적으로 읽히고**, 필요할 때 `PROMPTS.md`의 해당 역할만 복사합니다.
- **알고리즘 고민 시에만:** `ALGORITHM_GUIDE.md`.
- **검증 단계에서:** `VALIDATION_GUIDE.md`.
- **명령이 기억 안 날 때:** `COMMAND_CHEATSHEET.md`.
- **문서가 실제로 필요할 때만:** `templates/`의 해당 양식을 과제 프로젝트에 **복사**합니다. **양식 3개를 모두 생성할 필요는 없습니다.**
- **CSV가 있을 때만:** `scripts/profile_csv.py`를 실행합니다. CSV가 아니면 사용하지 않습니다.

## 디렉터리 구조 (13개 파일, 하위 폴더 2개)

```text
ai-hackathon-toolkit/
├── README.md                    # 전체 지도·사용 원칙·각 파일의 역할
├── AGENTS.md                    # AI에게 적용할 공통 실행·품질·보안 규칙
├── QUICK_START.md               # 시험 시작 10분 행동 순서와 타임박스
├── PROMPTS.md                   # Bash 1/2/3 역할 및 단계별 복사용 프롬프트
├── ALGORITHM_GUIDE.md          # 문제 정식화·Solver/휴리스틱·선택 기준
├── VALIDATION_GUIDE.md         # 데이터·업무 제약·API/UI·독립 검증
├── COMMAND_CHEATSHEET.md       # Bash/Git/Python/서버·Docker 명령 참고
├── templates/
│   ├── TASK_PLAN.md             # 요구사항, 가정, 결정, P0/P1/P2 계획
│   ├── REVIEW_REPORT.md         # QA의 독립 검증, 오류, 재검증 근거
│   └── HANDOFF.md               # 실행법, 입력·출력, 완료 상태, 제한사항
├── scripts/
│   └── profile_csv.py           # 표준 라이브러리 전용·원본 읽기 전용 CSV 점검
├── .gitignore                   # 캐시·임시 산출물·비밀정보 Git 추적 방지
└── LICENSE                      # Toolkit 자체의 MIT 라이선스
```

**이 저장소의 문서는 참고용이며 과제의 필수 제출물 자체가 아닙니다.** 생성할 결과물의 이름·위치는 공식 요구사항과 기존 과제 구조가 정합니다.

## 시험 작업 환경에서의 안전한 도입

가능하면 **과제 폴더와 Toolkit 폴더를 분리**하세요. 아래 `WORKSPACE`와 저장소 주소는 예시일 뿐, 실제 경로/URL이 아닙니다.

```bash
pwd
ls -la
# 네트워크·권한이 허용되고 과제 폴더의 상위 디렉터리로 이동 가능할 때만:
cd /workspace
# <PUBLIC_REPO_URL>에는 직접 생성한 공개 GitHub 저장소의 URL 입력
git clone <PUBLIC_REPO_URL> ai-hackathon-toolkit
```

> **주의:** `git clone`이 허용돼도 외부 네트워크나 Git 설치가 보장되지는 않습니다. 정책이 허용하면 시험 전에 ZIP/문서를 오프라인으로 준비할 수 있습니다. 시험 중 다운로드가 금지되거나 제한된다면 시도하지 마세요.

과제의 실제 작업 디렉터리로 돌아와 Codex를 사용합니다. **Toolkit 디렉터리에서 과제 코드를 작성하지 않습니다.** AI 세션에 예를 들어 다음과 같이 말합니다.

```text
현재 과제 작업 디렉터리를 유지해. Toolkit은 /workspace/ai-hackathon-toolkit 에 있다.
가능하면 해당 AGENTS.md를 읽고 적용하되 공식 과제 지시가 최우선이다.
QUICK_START.md의 1단계대로 기존 README/실행환경/제출 조건을 먼저 조사해.
아직 과제 코드를 수정하지 마. 근거 파일 경로와 미확인 사항을 알려줘.
```

**AGENTS.md 자동 적용을 가정하지 마세요.** Codex 설정/실행 위치/권한에 따라 읽히지 않을 수 있으므로 명시적으로 파일 읽기를 요청하거나 핵심 지침을 붙여 넣습니다. 다른 세션의 대화 맥락도 자동 공유되지 않습니다.

외부 폴더 접근이 금지되어 있다면 규정이 허용하는 작업 디렉터리 내부에 별도 Toolkit 폴더를 만들고, 제출 대상에 포함되지 않게 확인하세요. 개발 파일과 문서를 가져오더라도 과제 전체를 이 Toolkit으로 대체하지 마세요.

## 역할과 산출물: 실제 과제 폴더 기준

| 단계 | 주 담당 | 사용할 문서/도구 | 기대 산출물(과제 요구에 따라 선택) |
|---|---|---|---|
| 환경·제출 조건 확인 | Bash 1 | `QUICK_START`, `AGENTS`, `COMMAND_CHEATSHEET` | 읽은 근거 경로, 실행 명령 후보, 제출 체크리스트 |
| 요구사항·우선순위 | Bash 1, Bash 3(선택) | `PROMPTS`, `templates/TASK_PLAN` | 요구사항 ID·검증 기준·P0/P1/P2 계획 |
| 입력 데이터 검사 | Bash 1, Bash 2 | `profile_csv.py`, `VALIDATION_GUIDE` | 데이터 프로파일 JSON, 입력 품질 이슈/독립 확인 |
| 업무 규칙 확정 | Bash 1 + 현업 AI(있을 때) | `PROMPTS`, `ALGORITHM_GUIDE` | Hard/Soft/Objective/가정 목록, 결정 기록 |
| 핵심 기능 개발 | Bash 1 | `AGENTS`, `PROMPTS`, `ALGORITHM_GUIDE` | 과제별 소스코드, 실행 결과/화면, 결과 데이터 |
| 독립 검증·수정 | Bash 2 → Bash 1 | `VALIDATION_GUIDE`, `templates/REVIEW_REPORT` | 검증 코드(필요 시), 실제 테스트 결과, 오류 수정·재검증 |
| 실행 확인·제출 | Bash 1 + Bash 3(선택) | `COMMAND_CHEATSHEET`, `templates/HANDOFF` | 공식 형식의 README/HOW_TO_RUN 등, 제출 파일·검증 기록 |

`Bash 1/2/3`은 여기서 **담당 역할의 이름**이며, 실제 환경에서 Codex 세션이 3개 열려야 한다는 뜻은 아닙니다. 우선 단일 세션으로 시작해도 되고, 화면/협업 비용이 크면 **Bash 1 + Bash 2 두 역할**만 사용해도 됩니다. Bash 3은 필수가 아닙니다.

## CSV 분석 사용 예시

실제 경로·구분자·인코딩에 맞게 바꾸세요. **사람 이름/주소 등 개인정보가 담긴 샘플값을 공개 저장소에 커밋하면 안 됩니다.** 이 스크립트는 기본적으로 샘플값을 내보내지 않습니다.

```bash
python /workspace/ai-hackathon-toolkit/scripts/profile_csv.py ./data/input.csv \
  --out ./outputs/data_profile.json
# 스크립트 자체 동작 확인: 외부 패키지 불필요
python /workspace/ai-hackathon-toolkit/scripts/profile_csv.py --self-test
```

출력: 파일/행·열·헤더, 컬럼별 공백·고유값 하한, 행 중복 검출 하한, 열 개수 불일치 및 한계 정보. **업무 제약·키의 유일성·이상치·거리·시간의 타당성은 사람이 규칙을 정하고 추가 검증해야 합니다.** 큰 CSV에서는 고유값/행 중복 추적에 상한이 있어 일부 수치가 정확값이 아니라 하한입니다.

## 시험 규정과 보안

1. 공개된 AI Skill/MCP/Plugin/GitHub 코드 사용 가능 여부는 공식 규정 우선. 허용 범위를 벗어나 시험 자료를 저장소/외부 서비스로 전송하지 않습니다.
2. 외부 코드 전체를 그대로 제출물로 대체하지 않습니다. 사용한 라이브러리·코드의 출처·라이선스와 사용 범위를 기록합니다.
3. 회사·HR 정보, 문제 지문, 개인 데이터, 접근 토큰, 인증정보는 공개 GitHub에 업로드하지 않습니다.
4. 결과물이 동작한다는 AI의 진술만으로 완료 처리하지 않습니다. 실제 커맨드 로그, 생성 파일, Browser Preview를 확인합니다.
5. 불가능한 기능은 숨기지 않고 `미구현/미검증/가정`으로 명시합니다.

## 압축을 간소화하면서 보존한 범위

과거 `00~10` 단계 가이드 및 `5개 Skill`의 내용은 `AGENTS`, `QUICK_START`, `PROMPTS`, `ALGORITHM_GUIDE`, `VALIDATION_GUIDE`에 합쳤습니다. 11개 문서 템플릿은 중복을 제거해 3개로 통합했습니다. 예제 3개는 두 가이드와 템플릿 내 예시로 이동했고, 별도 프로젝트 목록 스크립트 및 `.pytest_cache`/`__pycache__` 등의 불필요한 파일은 제외했습니다.
