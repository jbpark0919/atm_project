class Card:
    def __init__(self, card_number: str):
        self.card_number = card_number

class Account:
    def __init__(self, account_id: str, balance: int): # int로만 수행
        self.account_id = account_id
        self.balance = balance # mock 데이터 초기값 설정을 위해 생성자에서 잔액 설정 -> 실제 서비스에서는 계좌 번호에 해당되는 잔액을 조회해서 잔액 설정을 해야 함