def risk_sizing(equity, r, price, lot=0.0001):
    raw = max(0.0, (equity*r)/max(price,1e-9))
    steps = int(raw/lot)
    return steps*lot

def kill_switch(day_R, threshold_R=-2.0):
    return day_R <= threshold_R
