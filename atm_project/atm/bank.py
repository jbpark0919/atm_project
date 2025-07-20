from typing import List, Optional
from .models import Account


class BankService:
    def __init__(self):
        # 카드 -> 계좌 ID 목록 (Mock)
        self.card_to_accounts = {
            "1111-2222-3333-4444": ["account1", "account2"],
            "1234-5678-9012-3456": ["account3"]
        }

        # 계좌 ID -> 계좌 객체 (Mock)
        self.accounts = {
            "account1": Account("account1", 1000),
            "account2": Account("account2", 500),
            "account3": Account("account3", 300)
        }

        # 카드 번호 -> PIN (Mock)
        self.valid_pins = {
            "1111-2222-3333-4444": "1234",
            "1234-5678-9012-3456": "0000"
        }

    # 비밀 번호 확인 (카드 번호에 맞는 pin 번호를 입력했는지)
    def verify_pin(self, card_number: str, pin: str) -> bool:
        expected_pin = self.valid_pins.get(card_number)
        return expected_pin == pin # PIN 자체 반환 X, 맞는지 틀렸는지만 확인

    # 카드 번호에 해당되는 계좌 불러옴
    def get_accounts_by_card(self, card_number: str) -> List[str]:
        return self.card_to_accounts.get(card_number, [])

    # 계좌 이름과 남은 잔액 불러옴
    def get_account(self, account_id: str) -> Optional[Account]:
        return self.accounts.get(account_id)

    # 해당 계좌에 입금
    def deposit(self, account_id: str, amount: int):
        account = self.get_account(account_id)
        # BankService에서 있는 계좌인지 한 번 더 확인
        if account:
            account.balance += amount
            self.accounts[account_id] = account

    # 해당 계좌에서 출금
    def withdraw(self, account_id: str, amount: int):
        account = self.get_account(account_id)
        if account:
            account.balance -= amount
            self.accounts[account_id] = account

# ATM 기계 남은 현금
class CashBin:
    def __init__(self, available_cash: int):
        self.available_cash = available_cash

    def can_dispense(self, amount: int) -> bool:
        return self.available_cash >= amount

    def dispense(self, amount: int):
        if self.can_dispense(amount):
            self.available_cash -= amount
