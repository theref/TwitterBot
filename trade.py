import bitmex
import settings
import json

products = settings.products

bitmex_client = bitmex.bitmex(
    test=False,
    api_key=settings.BITMEX_PUBLIC_KEY,
    api_secret=settings.BITMEX_PRIVATE_KEY,
)


def get_position(product, client):
    response = client.Position.Position_get(
        filter=json.dumps({"symbol": product + "USD"})
    ).result()[0]
    if response == []:
        return 0
    else:
        return response[0]["currentQty"]
    return response


def get_status():
    status = {p: get_position(p, bitmex_client) for p in products}
    return status


def main():
    print(get_status())


if __name__ == "__main__":
    main()
