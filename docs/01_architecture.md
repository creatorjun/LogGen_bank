# docs/01_architecture.md

# LogGen_bank 아키텍처 설계

## 핵심 원칙

> 고정 포맷 명세는 **Domain**이 소유한다.  
> 토큰 해석, 전송 루프 조율은 **Application**이 담당한다.  
> UDP 송신은 **Infrastructure**가 구현한다.  
> Qt6 UI와 ViewModel은 **Presentation**만 알고 있다.  
> 의존성 방향은 단방향 — `Presentation → Application → Domain` ← `Infrastructure`

---

## 계층 구조

```
loggen_bank/
├── domain/                     # 순수 비즈니스 규칙, 외부 의존성 Zero
│   ├── entities/
│   │   ├── log_header.py           # 헤더 고정 포맷 엔티티
│   │   ├── log_common_body.py      # 뽅킹(A1) 전용 공통부 101byte
│   │   ├── card_common_body.py     # 카드(C3) 전용 공통부 57byte [신규]
│   │   ├── telegram_type.py        # 전문 타입 StrEnum (4종)
│   │   ├── person.py               # Person 마스터 데이터 엔티티
│   │   └── telegrams/
│   │       ├── banking_0100_100.py # 실시간송금   개별부 202byte
│   │       ├── banking_0400_100.py # 타행이체불능 개별부 116byte
│   │       ├── banking_0600_400.py # 성명조회     개별부 128byte
│   │       └── card_nit_0200.py    # 카드승인인증 개별부
│   ├── value_objects/
│   │   ├── date_offset.py          # 날짜 오프셋 Value Object
│   │   └── session_sequence.py     # 세션 단위 증가형 시퀀스 토큰 공급자
│   └── ports/
│       ├── log_builder_port.py     # 빌더 추상 인터페이스
│       └── log_sender_port.py      # 전송 추상 인터페이스
│
├── application/                # 유스케이스 오케스트레이션
│   ├── use_cases/
│   │   ├── generate_log_use_case.py    # Person + TelegramType → raw log
│   │   └── send_log_use_case.py        # raw log → UDP 전송
│   ├── services/
│   │   ├── transmission_loop.py        # 영구 실행 전송 루프 (asyncio.Event 기반)
│   │   └── token_resolver.py           # 토큰 치환 서비스
│   └── dto/
│       └── log_result_dto.py
│
├── infrastructure/
│   ├── builders/
│   │   └── log_builder.py          # 전문타입별 빌더 디스패치
│   ├── network/
│   │   ├── tcp_sender.py           # TCP 전송 구현체
│   │   └── udp_sender.py           # UDP 514 전송 구현체
│   └── data/
│       └── person_fixture.py       # Person 마스터 5명 픽스처
│
└── presentation/
    ├── main_window.py              # QMainWindow — DI 조립점
    ├── view_models/
    │   └── main_view_model.py      # pyqtSignal, async 브릿지
    └── widgets/
        ├── control_panel.py        # 전송 대상(Host/Port) / 날짜오프셋 / 전송간격 입력
        ├── log_preview.py          # 생성 로그 미리보기 (최근 500건)
        ├── transmission_control.py # 전송/중지 토글 버튼 + 전송간격 설정
        ├── stats_panel.py          # Person/케이스/건수/실패수 실시간 표시
        └── status_bar.py           # 전송 결과 색상 상태바
```

---

## 로그 포맷 구조

```
[헤더(83)] [공통부] 개별부(가변) @@
```

| 전문 ID | 헤더 | 공통부 | 개별부 | 공통부 클래스 | 종료 |
|---|---|---|---|---|---|
| A1-0100-100 (실시간송금) | 83 | 101 | 202 | `LogCommonBody` | `@@` |
| A1-0400-100 (타행이체불능) | 83 | 101 | 116 | `LogCommonBody` | `@@` |
| A1-0600-400 (성명조회) | 83 | 101 | 128 | `LogCommonBody` | `@@` |
| C3-NIT-0200 (카드승인) | 83 | 57 | 가변 | `CardCommonBody` | `@@` |

- 헤더 시작: `[`, 헤더 식별자(공통부 구분): `/`
- 공통부 종료: `]`
- 전문 최종 종료: `@@`

---

## 토큰 분류 체계

| 토큰 종류 | 예시 | 공급 주체 |
|---|---|---|
| Person 고정값 | `rrn`, `dfmt_actnum`, `track` | `Person` 엔티티 |
| 세션 증가값 | `tlgrm_num`, `inq_num`, `log_pk` 시퀀스 | `SessionSequence` Value Object |
| 날짜 오프셋값 | `log_date`, `trms_ymd`, `inq_ymd` | `DateOffset` Value Object |
| 전문 고정값 | `bank_cod`, `msg_cod`, `bz_sctn` | 각 전문 엔티티 상수 |

---

## 전송 루프 상태 머신

```
[IDLE] ──전송버튼──► [RUNNING] ──중지버튼──► [PAUSED]
                        ▲                        │
                        └────────전송버튼─────────┘
```

- 내부 구현: `asyncio.Event` — set 상태일 때 진행, clear 상태일 때 `await event.wait()` 대기
- Task는 프로그램 시작 시 단 1개 생성, 종료 시 cancel
- Person 순회: 5명 × 4케이스 = 20조합을 순차 Round-robin
