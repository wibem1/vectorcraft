"""Conservative text-request budget admission; provider billing remains authoritative."""
import json
import math
from decimal import Decimal, InvalidOperation

MAX_COMPLETION_TOKENS = 4000


def money(value):
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError('Ungültiger Kostenwert') from None
    if not amount.is_finite() or amount < 0:
        raise ValueError('Kosten müssen endlich und nicht negativ sein')
    return amount


def estimate(model, messages, output_tokens):
    # Image input rates are irrelevant only when both actual input and possible
    # output are confirmed text. Never waive unknown fees or image generation.
    if not all(isinstance(m.get('content'), str) for m in messages):
        raise ValueError('Kostenprüfung unterstützt ausschließlich Text')
    text_output = model.get('architecture', {}).get('output_modalities') == ['text']
    pricing = model.get('pricing', {})
    if not all(key in pricing for key in ('prompt', 'completion')):
        raise ValueError('Keine bestätigten Modellpreise: Anfrage gesperrt')
    prompt, completion = money(pricing['prompt']), money(pricing['completion'])
    # Reserve a separate full output allowance for internal reasoning as well.
    # Deliberately conservative even when the provider includes it in completion.
    completion += money(pricing.get('internal_reasoning', 0))
    if ':online' in model.get('id', ''):
        raise ValueError('Online-Modelle werden für lokale Konstruktionen nicht unterstützt')
    for key, value in pricing.items():
        # Validate even unused rates, so invalid catalog values still fail closed.
        amount = money(value)
        if key in ('image', 'audio', 'input_audio_cache') and text_output:
            continue
        # api_chat explicitly disables web plugin and never requests server tools.
        if key == 'web_search':
            continue
        # Cache discounts cannot increase the uncached estimate. All other fees fail closed.
        if key not in ('prompt', 'completion', 'request', 'input_cache_read', 'input_cache_write', 'internal_reasoning') and amount:
            raise ValueError('Zusatzpreis nicht unterstützt: '+key)
    if money(pricing.get('input_cache_write', 0)) > prompt:
        raise ValueError('Cache-Aufschlag nicht unterstützt')
    if type(output_tokens) is not int or not 1 <= output_tokens <= MAX_COMPLETION_TOKENS:
        raise ValueError('Ungültiges Ausgabelimit')
    if not all(isinstance(m.get('content'), str) for m in messages):
        raise ValueError('Kostenprüfung unterstützt ausschließlich Text')
    size = len(json.dumps(messages, ensure_ascii=False).encode('utf8'))
    if size > 60000:
        raise ValueError('Kontext zu groß für die Kostenprüfung')
    # Deliberately far above common token counts: UTF-8 bytes + generous framing, ×2.
    # This remains an estimate, not a server-enforced charge cap.
    input_bound = 2 * (size + 4096)
    context = model.get('context_length')
    if not isinstance(context, int) or input_bound + output_tokens > context:
        raise ValueError('Kontextlimit nicht bestätigt oder zu klein')
    return (prompt * input_bound + completion * output_tokens + money(pricing.get('request', 0))) * Decimal('1.20')


def admit(model, messages, output_tokens, spent_usd, budget_eur, usd_to_eur):
    budget, rate, spent = money(budget_eur), money(usd_to_eur), money(spent_usd)
    if budget <= 0 or rate <= 0:
        raise ValueError('Budget und Umrechnungskurs müssen positiv sein')
    reserve = estimate(model, messages, output_tokens)
    if (spent + reserve) * rate > budget:
        raise ValueError('Kostenbudget würde laut Vorabprüfung überschritten; Anfrage gesperrt')
    return float(reserve)
