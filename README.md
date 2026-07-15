# README.md
# LogGen Bank — 금융거래 TR 로그 생성기

## 개요

금융거래(TR) 시스템의 UDP 로그를 다양한 테스트 시나리오로 생성하여 전송하는 PyQt6 기반 데스크탑 도구입니다.

## 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 실행
python main.py
```

## 주요 기능

- **5명 Person** 라운드로빈 순환 전송 (Person 편집 가능)
- **4종 전신** (WITHDRAW / DEPOSIT / CARD_APPROVAL / CARD_CANCEL) 순환
- **UDP / TCP 전송** 선택 (코드 1줄 교체)
- **날짜 오프셋** 실시간 적용 (+/- 토글)
- **전송 간격** 동적 변경 (1 – 99999 ms)
- **로그 파일 자동 저장** (`logs/loggen_YYYYMMDD_HHMMSS.txt`, EUC-KR)
- **미리보기 500건 제한** 자동 클리어

## 프로젝트 구조

```
LogGen_bank/
├── main.py                        # 진입점 (qasync)
├── domain/                        # 엔티티, VO, Port 인터페이스
├── application/                   # UseCase, Service
├── infrastructure/                # Sender, Fixture
└── presentation/                  # PyQt6 UI + ViewModel
```

## TCP으로 전환

`presentation/view_models/main_view_model.py` 의 `_build_loop()` 내
`UdpSender()` → `TcpSender()` 한 줄만 교체하면 됩니다.
