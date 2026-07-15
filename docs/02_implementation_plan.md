# docs/02_implementation_plan.md

# 구현 상세 계획

## 1. Person 마스터 엔티티

### 설계 원칙
- Person은 4가지 전문 타입이 요구하는 모든 필드를 **전부 고유값**으로 보유
- 전문 생성 시 `PersonToTelegramMapper`가 Person에서 필요한 속성만 추출해 params dict 생성
- 5명은 `infrastructure/data/person_fixture.py`에 하드코딩 픽스처로 관리

### Person 보유 필드 목록

| 분류 | 필드명 | 설명 | 예시 |
|---|---|---|---|
| 기본 | `name` | 성명 | 홍길동 |
| 기본 | `rrn` | 주민번호 13자리 | 0106151057326 |
| 뱅킹 | `log_pk` | 로그 PK 식별코드 (9자) | 00603REN |
| 뱅킹 | `entr_cod` | 업체코드 | SE_C00OD |
| 뱅킹 | `server_id` | 서버 IP | 211.168.15.3 |
| 뱅킹 | `instance_id` | WAS ID | 542EE |
| 뱅킹 | `bank_cod` | 은행코드 2자리 | A1 |
| 뱅킹 | `bank_cod_3` | 은행코드 3자리 | 001 |
| 뱅킹 | `bank_resp_cod` | 은행응답코드 | 0400 |
| 뱅킹 | `dfmt_actnum` | 출금계좌번호 15자리 | 110568666777333 |
| 뱅킹 | `bbk_pwd` | 통장비밀번호 | 0415 |
| 뱅킹 | `pwd_mrk` | 복기부호 | 555555 |
| 뱅킹 | `dps_act` | 입금계좌번호 15자리 | 110568666777444 |
| 뱅킹 | `dps_bank_cod` | 입금은행코드 2자리 | 03 |
| 뱅킹 | `dps_bank_cod_3` | 입금은행코드 3자리 | 951 |
| 뱅킹 | `dpsr_nm` | 입금인성명 (20자) | 홍길동_삼촌용돈 |
| 뱅킹 | `bank_tlgrm_num` | 은행전문번호 15자리 | 777888999444555 |
| 카드 | `card_number` | 카드번호 원본 | 2114587458745874587 |
| 카드 | `card_expiry` | 유효기간 YYMM | 2802 |
| 카드 | `track` | Track-II 조합값 42자 | 2114587458745874587=2802... |
| 카드 | `tid_prefix` | TID 증권번호 12자리 | 741902568942 |
| 카드 | `br_num` | 가맹점번호 | 9716010001 |
| 카드 | `trs_amt` | 거래금액 | 1500 |

---

## 2. 토큰 치환 시스템

### 토큰 규칙
- 구분자: `${TOKEN_NAME}` 형태
- `TokenResolver`가 3가지 공급자에서 값 수집 후 일괄 치환
- 미등록 토큰 사용 시 `TokenResolutionError` 발생
- 필드 길이 초과 시 `FieldLengthError` 발생

### 토큰 공급자 우선순위
```
1. SessionSequence (매 건 증가값)
2. DateOffset      (날짜 오프셋 연산값)
3. Person          (고정 마스터값)
```

### 세션 증가형 토큰

| 토큰 | 형식 | 규칙 |
|---|---|---|
| `${TLGRM_NUM}` | 6자리 숫자 zero-padding | 세션 시작 시 `000001`부터 1씩 증가, overflow 시 `000001` 리셋 |
| `${INQ_NUM}` | 6자리 숫자 | 동일 규칙 |
| `${LOG_PK_SEQ}` | 3자리 숫자 suffix | Person별 개별 관리 |
| `${TID_SEQ}` | 2자리 숫자 `01`~`99` | 카드 TID SeqNumber 부분 |

### 날짜 오프셋 토큰

| 토큰 | 형식 | 설명 |
|---|---|---|
| `${LOG_DATE}` | YYYYMMDD | today + offset_days |
| `${LOG_TIME}` | HHMMSS | 현재 시각 실시간 |
| `${TRMS_YMD}` | YYYYMMDD | LOG_DATE와 동일 정책 |
| `${TRMS_HMS}` | HHMMSS | LOG_TIME과 동일 |
| `${INQ_YMD}` | YYYYMMDD | LOG_DATE와 동일 정책 |
| `${TRS_YMD_MMDD}` | MMDD | LOG_DATE의 월일 부분만 |

---

## 3. 날짜 오프셋 UI

- `[+/-] 토글버튼` + `숫자 입력칸 (QSpinBox, 0~999)` 조합
- 기본값: `+0` (오늘 날짜)
- 오프셋 적용 대상: `log_date`, `trms_ymd`, `inq_ymd` 전부 동일하게 적용
- 시각(HHMMSS)은 항상 현재 시각 실시간 사용

---

## 4. 전송 루프 엔진

### 순회 방식
- 5명 × 4케이스 = **20조합을 순차 Round-robin**으로 영구 반복
- 순서: `Person1-케이스1 → Person1-케이스2 → ... → Person5-케이스4 → Person1-케이스1 → ...`

### 루프 제어
```python
async def _transmission_loop(self):
    while True:
        await self._run_event.wait()   # PAUSED 상태면 여기서 대기
        person, telegram_type = self._next_combo()
        log = self._generate(person, telegram_type)
        await self._send(log)
        self._update_stats()
        await asyncio.sleep(self._interval_seconds)
```

### 전송 간격
- UI에서 실시간 조정 가능 (50ms ~ 5000ms)
- 기본값: **500ms**

---

## 5. UDP 전송 구현

- `asyncio.DatagramProtocol` 기반 비동기 UDP 소켓
- 기본 대상: `host:514`
- 페이로드: TR 본문 raw bytes (syslog envelope 없음)
- 인코딩: **EUC-KR** (금융 레거시 시스템 호환)
- "성공" 정의: 로컬 송신 호출이 OSError 없이 완료됨
- 예외(OSError, `Network unreachable` 등)는 `stats_panel`에 실패 카운트로 표시

---

## 6. UI 설계

### 테마
- **라이트 Fluent 계열** — Windows 11 앱 스타일
- 배경: `#F3F3F3 / #FFFFFF`, 포인트 컬러: `#0078D4` (Microsoft Blue)
- 입력창: `border-radius: 4px`, `border: 1px solid #D0D0D0`
- 버튼: `border-radius: 4px`, 호버 시 배경색 변화
- 폰트: `Segoe UI` (Windows 기본), fallback `Arial`

### 레이아웃

```
┌─────────────────────────────────────────────────────┐
│  상단: 전송 대상(Host/Port) | 날짜 오프셋 | 전송 간격 │
├───────────────────────┬─────────────────────────────┤
│  로그 미리보기 (좌)    │  Stats 패널 (우)            │
│  - QTextEdit ReadOnly │  - 현재 Person               │
│  - 고정폭 폰트        │  - 현재 케이스               │
│  - 최근 500건 유지    │  - 누적 전송 건수            │
│                       │  - 실패 건수                 │
│                       │  - 현재 상태 (IDLE/RUN/PAUSE)│
├───────────────────────┴─────────────────────────────┤
│  하단: [전송/중지 토글] [복사] [클리어] (우측 정렬)   │
├─────────────────────────────────────────────────────┤
│  상태바: 최근 전송 결과 메시지 (색상 표시)            │
└─────────────────────────────────────────────────────┘
```
