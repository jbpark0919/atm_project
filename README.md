# ATM Project
## 프로젝트 설명
ATM 기본 동작 흐름을 테스트 가능한 형태로 구현
Mock 기반 ATM Controller

## 흐름
Insert Card => PIN number => Select Account => See Balance/Deposit/Withdraw

## 폴더 구조
```
atm_project/
├── atm/
│   ├── models.py         # Card, Account 클래스
│   ├── atm_controller.py # ATM 로직
│   └── bank.py           # Mock BankService, CashBin
├── tests/
│   └── test_atm_controller.py  # 테스트 케이스
└── README.md
```

## 실행 방법
### 1. 프로젝트 클론
```bash
git clone https://github.com/jbpark0919/atm_project.git
cd atm_project
```
### 2. 테스트 실행
```bash
python -m unittest discover -s tests
```
