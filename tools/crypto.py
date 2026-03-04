import requests
from langchain.tools import tool

@tool
def get_crypto_price(coin: str) -> str:
    """
    Get the current price of any cryptocurrency in USD and EUR.
    Input should be the coin name like 'bitcoin', 'ethereum', or 'solana'.
    Also returns 24h price change percentage.
    """

    try:
        # Normalize input
        coin_id = coin.lower().strip()

        url = "https://api.coingecko.com/api/v3/simple/price"
        response = requests.get(url, params={
            "ids": coin_id,
            "vs_currencies": "usd,eur",
            "include_24hr_change": "true"
        })
        data = response.json()

        if coin_id not in data:
            return (
                f"Coin '{coin}' not found. "
                f"Try full names like 'bitcoin', 'ethereum', 'solana', 'cardano'."
            )

        coin_data = data[coin_id]
        usd_price = coin_data.get("usd", "N/A")
        eur_price = coin_data.get("eur", "N/A")
        change_24h = coin_data.get("usd_24h_change", 0)

        trend = "📈" if change_24h > 0 else "📉"

        return (
            f"{coin.capitalize()} Price:\n"
            f"💵  USD: ${usd_price:,.2f}\n"
            f"💶  EUR: €{eur_price:,.2f}\n"
            f"{trend}  24h Change: {change_24h:.2f}%"
        )
    except Exception as e:
        return f"Error fetching crypto price: {str(e)}"