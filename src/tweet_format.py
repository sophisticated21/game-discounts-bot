import random

def format_tweet(info):
    d = info["discount"]
    game = info["name"]
    final = info["price"]
    currency = info["currency"]
    original = info["original"]
    link = f"https://store.steampowered.com/app/{info['app_id']}/?cc=br&l=portuguese"

    if d >= 50:
        templates = [
            "Boa queda no preço de {game}!\nAgora por {final} {currency} ({discount}% off)\n{link}",
            "Oferta bem forte para {game} hoje.\n{discount}% off → {final} {currency}\n{link}",
            "{game} ficou bem mais barato agora.\n{final} {currency} ({discount}% off)\n{link}",
        ]
    elif d >= 20:
        templates = [
            "Bom desconto em {game}.\nAgora por {final} {currency} ({discount}% off)\n{link}",
            "Preço caiu um pouco em {game}.\n{discount}% off → {final} {currency}\n{link}",
            "{game} está com um preço melhor hoje.\nAgora por {final} {currency}\n{link}",
        ]
    else:
        templates = [
            "Pequeno desconto em {game}.\n{discount}% off → {final} {currency}\n{link}",
            "{game} está um pouco mais barato hoje.\nAgora por {final} {currency}\n{link}",
            "Desconto leve em {game}.\n{final} {currency} ({discount}% off)\n{link}",
        ]

    t = random.choice(templates)
    return t.format(
        game=game,
        discount=d,
        final=final,
        currency=currency,
        original=original,
        link=link,
    )