class Aave(object):
    def __init__(
        self,
        name,
        symbol,
        network,
        deposit_apr,
        variable_borrow_apr,
        stable_borrow_apr,
        deposit_apy,
        variable_borrow_apy,
        stable_borrow_apy,
    ):
        self.name = name
        self.symbol = symbol
        self.network = network
        self.deposit_apr = deposit_apr
        self.variable_borrow_apr = variable_borrow_apr
        self.stable_borrow_apr = stable_borrow_apr
        self.deposit_apy = deposit_apy
        self.variable_borrow_apy = variable_borrow_apy
        self.stable_borrow_apy = stable_borrow_apy
