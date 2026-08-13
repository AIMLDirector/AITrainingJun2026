
def calculate_intrinsic_value(eps, growth_rate=0.10, pe=20):

    future_eps = eps * (1 + growth_rate) ** 5

    intrinsic_value = future_eps * pe

    return round(intrinsic_value, 2)