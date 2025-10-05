import aiohttp
import asyncio

async def decode_func_signatures(*unique_selectors):
    """
    Asynchronously decodes 4-byte function selectors using the 4byte.directory API.

    Args:
        *selectors (str): One or more 4-byte hex selectors.

    Returns:
        dict[str, list[str] | None]: Map of selector → list of matching function signatures.
    """
    four_byte_url = "https://www.4byte.directory/api/v1/signatures/?format=json&hex_signature="
    async def async_fetch(url, session):
        async with session.request("GET", url=url, headers={"accept": "application/json"}) as response:
            if response.status != 200:
                return None
            json_response = await response.json()
            if json_response.get("count", 0) < 1:
                return None
            return [result.get("text_signature", "") for result in json_response.get("results", [])]

    async with aiohttp.ClientSession() as session:

        tasks = [asyncio.create_task(async_fetch(four_byte_url + selector, session)) for selector in unique_selectors]
        responses = await asyncio.gather(*tasks)
        signature_map = dict(zip(unique_selectors, responses))
        return signature_map


if __name__ == "__main__":
    """
    Example: 
        decoded_functions = asyncio.run(decode_func_signatures("3644e515","39509351"))
    """