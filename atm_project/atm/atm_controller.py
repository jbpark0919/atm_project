from typing import List
from .models import Account, Card
from .bank import BankService, CashBin


class ATMController:
    def __init__(self, bank_service: BankService, cash_bin: CashBin):
        self.bank_service = bank_service
        self.cash_bin = cash_bin
        self.inserted_card: Card = None
        self.selected_account: Account = None

    # 카드 삽입
    def insert_card(self, card: Card):
        self.inserted_card = card

    # 비밀 번호 확인 (카드 번호에 맞는 pin 번호를 입력했는지)
    def verify_pin(self, pin: str) -> bool:
        if not self.inserted_card:
            raise Exception("No card inserted")
        return self.bank_service.verify_pin(self.inserted_card.card_number, pin)

    # 카드 번호에 해당되는 계좌 불러옴
    def get_accounts(self) -> List[str]:
        if not self.inserted_card:
            raise Exception("No card inserted")
        return self.bank_service.get_accounts_by_card(self.inserted_card.card_number)

    # 계좌 선택
    def select_account(self, account_id: str):
        if not self.inserted_card:
            raise Exception("No card inserted")
        account = self.bank_service.get_account(account_id)
        if not account:
            raise Exception("Account not found")
        self.selected_account = account

    # 선택된 계좌의 잔액을 불러옴
    def get_balance(self) -> int:
        if not self.selected_account:
            raise Exception("No account selected")
        return self.selected_account.balance

    # 선택된 계좌에 입금
    def deposit(self, amount: int):
        if not self.selected_account:
            raise Exception("No account selected")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.bank_service.deposit(self.selected_account.account_id, amount)

    # 선택된 계좌에서 출금 (남은 잔액보다 많은 양 출금 시도 예외 처리, ATM 기계에 남은 현금보다 많은 양 출금 시도 예외 처리)
    def withdraw(self, amount: int) -> bool:
        if not self.selected_account:
            raise Exception("No account selected")
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")

        account_id = self.selected_account.account_id
        current_balance = self.bank_service.get_account(account_id).balance

        if current_balance < amount:
            return False
        if not self.cash_bin.can_dispense(amount):
            return False

        self.bank_service.withdraw(account_id, amount)
        self.cash_bin.dispense(amount)
        return True
