def transform_phone_number(phone_number):
    if phone_number.startswith("0"):
        transformed_number = "+233" + phone_number[1:]
        return transformed_number
    else:
        return phone_number