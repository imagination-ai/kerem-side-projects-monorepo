def convert_turkish_number_to_us(price: str) -> float:
    us_number_convention = {",": ".", ".": ","}
    trans_table = price.maketrans(us_number_convention)
    price = price.translate(trans_table).replace(",", "")

    return float(price)
