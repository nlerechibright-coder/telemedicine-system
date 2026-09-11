from urllib.parse import quote_plus


class WhatsAppProviderError(ValueError):
    """Raised when a WhatsApp contact cannot be used safely."""


def normalize_whatsapp_number(number, default_country_code='234'):
    """Return a digits-only international WhatsApp number."""
    if not number:
        raise WhatsAppProviderError('A WhatsApp contact number has not been configured.')

    value = ''.join(character for character in str(number).strip() if character.isdigit())
    if str(number).strip().startswith('00'):
        value = value[2:]
    elif value.startswith('0'):
        value = default_country_code + value[1:]

    if not value.isdigit() or not 7 <= len(value) <= 15:
        raise WhatsAppProviderError('The WhatsApp contact number is invalid.')

    return value


def build_whatsapp_link(number, message=''):
    normalized_number = normalize_whatsapp_number(number)
    url = f'https://wa.me/{normalized_number}'
    if message:
        url += f'?text={quote_plus(message)}'
    return url