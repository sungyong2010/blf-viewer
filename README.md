# BLF Viewer

BLF(Binary Logging Format) 파일을 사람이 읽을 수 있는 텍스트 로그 파일로 변환하는 도구입니다.

## 📋 개요

BLF Viewer는 바이너리 형태의 CAN 통신 로그 파일(.blf)을 읽기 쉬운 텍스트 형식(.log)으로 변환해주는 Python 기반 GUI 애플리케이션입니다.

### 변환 예시

**변환 전 (BLF 파일):**
```
LOGG?  똟M <江     횞?    ?    ?  
   2 ??  
     ?팍?    *  L                                                           LOBJ  c? 
```

**변환 후 (LOG 파일):**
```
Time            Channel    ID         Type            Dir   DLC   Data                                              
--------------------------------------------------------------------------------------------------------------
00:00:00.000    CAN 0      102        CAN FD Frame    Rx    48    AA 0E 7D FD 01 02 00 00 00 00 64 00 02 00 00 10 00 00 A0 00 00 EC 0F 00 00 00 00 00 90 D1 FF 00 00 20 A6
00:00:00.125    CAN 0      1A3        CAN Frame       Tx    8     12 34 56 78 9A BC DE F0
00:00:00.250    CAN 1      2B4        CAN FD Frame    Rx    16    FF EE DD CC BB AA 99 88 77 66 55 44 33 22 11 00
```

## ✨ 주요 기능

- 🔄 **BLF to LOG 변환**: 바이너리 CAN 로그를 텍스트 형식으로 변환
- 📊 **CAN/CAN FD 지원**: 일반 CAN 및 CAN FD 프레임 모두 지원
- ⏱️ **상대 시간 표시**: 첫 메시지를 기준으로 한 상대 시간 계산
- 📡 **채널 정보**: CAN 채널 정보 표시
- 🎯 **메시지 상세 정보**: ID, 방향(Rx/Tx), DLC, 데이터 등 상세 정보 제공
- 🖥️ **GUI 인터페이스**: 사용하기 쉬운 파일 선택 대화상자
- 📈 **진행률 표시**: 실시간 변환 진행 상황 표시
- 🚀 **빠른 파일 열기**: 변환 완료 후 바로 파일 열기 가능

## 📊 출력 형식

변환된 로그 파일은 다음과 같은 형식으로 저장됩니다:

| 필드 | 설명 |
|------|------|
| **Time** | 시작 시간 기준 상대 시간 (HH:MM:SS.mmm) |
| **Channel** | CAN 채널 번호 (예: CAN 0, CAN 1) |
| **ID** | CAN 메시지 ID (16진수) |
| **Type** | 프레임 타입 (CAN Frame / CAN FD Frame) |
| **Dir** | 방향 (Rx: 수신, Tx: 송신) |
| **DLC** | 데이터 길이 (바이트) |
| **Data** | 메시지 데이터 (16진수, 공백으로 구분) |

## 🚀 설치 및 실행

### 필수 요구사항

- Python 3.7 이상
- python-can 라이브러리

### 설치 방법

1. 저장소 클론:
```bash
git clone https://github.com/yourusername/blf-viewer.git
cd blf-viewer
```

2. 필수 패키지 설치:
```bash
pip install python-can
```

### 실행 방법

#### Python 스크립트 실행
```bash
python blf-viewer.py
```

#### 실행 파일 빌드 (선택사항)
PyInstaller를 사용하여 독립 실행 파일(.exe)을 생성할 수 있습니다:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --name="BLF_Viewer" blf-viewer.py
```

빌드된 실행 파일은 `dist` 폴더에 생성됩니다.

## 💻 사용법

1. **프로그램 실행**: `blf-viewer.py` 또는 빌드된 실행 파일을 실행
2. **파일 선택**: 파일 선택 대화상자에서 변환할 BLF 파일 선택
3. **변환 대기**: 진행률 창에서 변환 진행 상황 확인
4. **완료**: 변환 완료 후 'Open' 버튼으로 결과 파일 확인

변환된 파일은 원본 BLF 파일과 같은 위치에 `.log` 확장자로 저장됩니다.

예시:
- 입력: `Airbag.blf`
- 출력: `Airbag.log`

## 📁 프로젝트 구조

```
blf-viewer/
├── blf-viewer.py          # 메인 애플리케이션
├── BLF_Viewer.spec        # PyInstaller 빌드 설정
├── README.md              # 프로젝트 문서
├── *.blf                  # 샘플 BLF 파일들
├── *.log                  # 변환된 로그 파일들
└── build/                 # 빌드 디렉토리
    └── BLF_Viewer/        # 빌드 아티팩트
```

## 🔧 기술 스택

- **Python 3**: 핵심 프로그래밍 언어
- **python-can**: CAN 버스 데이터 처리 라이브러리
- **tkinter**: GUI 프레임워크
- **PyInstaller**: 실행 파일 빌드 도구

## 🎯 사용 사례

- 🚗 자동차 CAN 통신 분석
- 🔍 CAN 메시지 디버깅
- 📊 통신 로그 분석 및 리포팅
- 🧪 테스트 데이터 검증
- 📝 통신 프로토콜 문서화

## ⚠️ 주의사항

- Windows 환경에 최적화되어 있습니다
- 대용량 BLF 파일 변환 시 시간이 소요될 수 있습니다
- 변환 중 프로그램을 종료하지 마세요

## 🤝 기여

버그 리포트, 기능 제안, Pull Request 환영합니다!

## 📧 문의

개발자: shaun.hong@lge.com

## 📄 라이선스

이 프로젝트는 자유롭게 사용 가능합니다.

---

**Made with ❤️ for CAN Bus Engineers**
