from bots.common.risk import risk_sizing

def test_risk_sizing():
    size = risk_sizing(1000, 0.01, 50000, lot=0.0001)
    assert size >= 0
