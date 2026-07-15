# docs/03_work_breakdown.md

# 작업 분할 (Work Breakdown)

## 마일스톤 개요

| 마일스톤 | 내용 | 선행 조건 |
|---|---|---|
| M1 | 포맷 명세 확정 및 Domain 정리 | 없음 |
| M2 | Person 마스터 + 토큰 치환 시스템 | M1 |
| M3 | 전송 루프 엔진 | M2 |
| M4 | UI 골격 + Fluent 테마 | M1 |
| M5 | UI-ViewModel 연결 + 통합 | M3, M4 |
| M6 | 안정성 처리 + 최종 정리 | M5 |

---

## M1 — 포맷 명세 확정 및 Domain 정리

- [ ] 4개 전문 엔티티 필드 길이 최종 검증 (샘플 파일 대조)
- [ ] `LogHeader.to_raw()` 단위 테스트 작성
- [ ] `LogCommonBody.to_raw()` 단위 테스트 작성
- [ ] 각 개별부 `to_raw()` 단위 테스트 작성 (EUC-KR byte 길이 기준)
- [ ] `TelegramType` StrEnum 확정
- [ ] `DateOffset` Value Object 구현
- [ ] `SessionSequence` Value Object 구현 (overflow 리셋 포함)

## M2 — Person 마스터 + 토큰 치환 시스템

- [ ] `Person` 엔티티 dataclass 구현 (전체 필드)
- [ ] `person_fixture.py` 5명 데이터 작성 (모두 고유값)
- [ ] `TokenResolver` 서비스 구현
  - [ ] Person 고정값 토큰 주입
  - [ ] SessionSequence 토큰 주입
  - [ ] DateOffset 토큰 주입
  - [ ] 미등록 토큰 오류 처리
  - [ ] 길이 초과 오류 처리
- [ ] `PersonToTelegramMapper` 구현 (4종 전문별 매핑 함수)
- [ ] `GenerateLogUseCase` 리팩토링 (Person 기반)

## M3 — 전송 루프 엔진

- [ ] `UdpSender` 구현 (`asyncio.DatagramProtocol` 기반)
- [ ] `SendLogUseCase` UDP 방식으로 전환
- [ ] `TransmissionLoop` 서비스 구현
  - [ ] `asyncio.Event` 기반 pause/resume
  - [ ] 5명 × 4케이스 Round-robin 순회 로직
  - [ ] 전송 간격 동적 변경 지원
  - [ ] 통계(건수, 실패수) 누적 관리
  - [ ] 안전한 Task cancel 처리 (`CancelledError` 핸들링)

## M4 — UI 골격 + Fluent 테마

- [ ] Fluent 라이트 글로벌 stylesheet 작성
- [ ] `ControlPanel` 위젯 개선
  - [ ] Host/Port 입력
  - [ ] 날짜 오프셋 (+/- 토글 + QSpinBox)
  - [ ] 전송 간격 QSpinBox (50~5000ms)
- [ ] `TransmissionControlWidget` 구현
  - [ ] 전송/중지 토글 버튼 (상태 연동)
  - [ ] 복사 버튼
  - [ ] 클리어 버튼
- [ ] `LogPreview` 위젯 개선
  - [ ] 최근 500건 제한 로직
  - [ ] Byte 길이 표시 (EUC-KR 기준)
- [ ] `StatsPanel` 위젯 구현
  - [ ] 현재 Person 이름 표시
  - [ ] 현재 전문 타입 표시
  - [ ] 누적 전송 건수 / 실패 건수
  - [ ] 현재 상태 (`IDLE` / `RUNNING` / `PAUSED`) 색상 표시
- [ ] `AppStatusBar` 개선 (성공/실패 색상)

## M5 — UI-ViewModel 연결 + 통합

- [ ] `MainViewModel` 전면 재설계
  - [ ] `TransmissionLoop` 통합
  - [ ] 모든 UI 이벤트 Signal/Slot 연결
  - [ ] 통계 데이터 pyqtSignal 정의 및 연결
- [ ] `MainWindow` DI 조립 최종 정리
- [ ] 전송 토글 버튼 ↔ Loop 상태 동기화 검증
- [ ] 날짜 오프셋 변경 → 실시간 토큰 반영 검증

## M6 — 안정성 처리 + 최종 정리

- [ ] UDP 예외 전체 케이스 처리 (`OSError`, `Network unreachable` 등)
- [ ] 시퀀스 overflow 안전 처리 검증
- [ ] 미리보기 500건 초과 시 자동 클리어 검증
- [ ] 창 종료 시 asyncio Task 안전 cancel 처리
- [ ] `requirements.txt` 최종 버전 고정
- [ ] `README.md` 실행 방법 및 구조 설명 업데이트
