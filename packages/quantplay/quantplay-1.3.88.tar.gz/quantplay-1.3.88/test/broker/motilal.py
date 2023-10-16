from quantplay.broker.motilal import Motilal

motilal = Motilal()


def test_account_summary():
    summary = motilal.account_summary()
    assert "pnl" in summary
    assert "margin_used" in summary
    assert "margin_available" in summary


def test_place_order():
    pass
    # motilal.place_order(
    #     tradingsymbol="GAIL",
    #     exchange="NSE",
    #     quantity=1,
    #     order_type="LIMIT",
    #     transaction_type="BUY",
    #     tag="testing",
    #     product="CNC",
    #     price=112,
    # )


def test_get_lot_size():
    assert motilal.get_lot_size("NSE", "SBIN") == 1
    assert motilal.get_lot_size("NFO", "BANKNIFTY23DEC44000CE") == 15
    assert motilal.get_lot_size("BFO", "SENSEX23DEC66000CE") == 10


def test_get_ltp():
    assert motilal.get_ltp("NFO", "BANKNIFTY23DEC44000CE") > 0
    assert motilal.get_ltp("NSE", "SBIN") > 0
    assert motilal.get_ltp("BFO", "SENSEX23DEC66000CE")
