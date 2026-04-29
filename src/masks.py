def get_mask_card_number(card_number: str) -> str:
    first_part = card_number[:6]
    last_part = card_number[-4:]
    masked = f"{first_part[:4]} {first_part[4:]}** **** {last_part}"
    return masked


def get_mask_account(account_number: str) -> str:
    last_four = account_number[-4:]
    masked = f"**{last_four}"
    return masked


if __name__ == "__main__":
    # Пример для карты
    card = "7000792289606361"
    print(f"{card}")
    print(f"{get_mask_card_number(card)}")

    print()

    # Пример для счёта
    account = "73654108430135874305"
    print(f"{account}")
    print(f"{get_mask_account(account)}")
