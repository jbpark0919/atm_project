import unittest
from atm.atm_controller import ATMController
from atm.models import Card, Account
from atm.bank import BankService, CashBin


class TestATMController(unittest.TestCase):
    def setUp(self):
        # BankService Mock 데이터 세팅
        self.bank_service = BankService()
        self.bank_service.accounts["test-account"] = Account("test-account", 500)
        self.bank_service.card_to_accounts["1111-2222-3333-4444"] = ["test-account"]
        self.bank_service.valid_pins["1111-2222-3333-4444"] = "1234"

        # CashBin 초기 현금
        self.cash_bin = CashBin(available_cash=1000)

        # ATM Controller 준비
        self.controller = ATMController(self.bank_service, self.cash_bin)

        # 테스트용 카드
        self.card = Card("1111-2222-3333-4444")

    # 비밀번호 맞게 입력했는지 확인
    def test_insert_card_and_verify_pin_success(self):
        self.controller.insert_card(self.card)
        self.assertTrue(self.controller.verify_pin("1234"))

    # 비밀번호 틀리게 입력했는지 확인
    def test_verify_pin_fail(self):
        self.controller.insert_card(self.card)
        self.assertFalse(self.controller.verify_pin("9999"))

    # 카드번호에 대응하는 계좌가 올바르게 반환되는지 확인
    def test_get_accounts(self):
        self.controller.insert_card(self.card)
        accounts = self.controller.get_accounts()
        self.assertEqual(accounts, ["test-account"])

    # 계좌 잔액조회가 올바르게 이루어지는지 확인
    def test_select_account_and_get_balance(self):
        self.controller.insert_card(self.card)
        self.controller.verify_pin("1234")
        self.controller.select_account("test-account")
        self.assertEqual(self.controller.get_balance(), 500)

    # 입금 후, 잔액이 올바르게 적용되는지 확인
    def test_deposit(self):
        self.controller.insert_card(self.card)
        self.controller.verify_pin("1234")
        self.controller.select_account("test-account")
        self.controller.deposit(200)
        self.assertEqual(self.controller.get_balance(), 700)

    # 출금이 올바르게 수행되는지, 출금 이후 잔액이 올바르게 적용되는지 확인
    def test_withdraw_success(self):
        self.controller.insert_card(self.card)
        self.controller.verify_pin("1234")
        self.controller.select_account("test-account")
        result = self.controller.withdraw(300)
        self.assertTrue(result)
        self.assertEqual(self.controller.get_balance(), 200)

    # 계좌 잔액보다 많은 금액은 출금할 수 없는지 확인
    def test_withdraw_fail_insufficient_funds(self):
        self.controller.insert_card(self.card)
        self.controller.verify_pin("1234")
        self.controller.select_account("test-account")
        result = self.controller.withdraw(600)  # 500밖에 없음
        self.assertFalse(result)

    # ATM 기계에 남아있는 현금보다 많은 금액은 출금할 수 없는지 확인
    def test_withdraw_fail_cash_bin_empty(self):
        # 현금통을 일부러 부족하게 만들기
        self.cash_bin.available_cash = 100
        self.controller.insert_card(self.card)
        self.controller.verify_pin("1234")
        self.controller.select_account("test-account")
        result = self.controller.withdraw(300)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
