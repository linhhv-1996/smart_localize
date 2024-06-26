import json
import asyncio
import aiohttp
import pprint

google_play_url = 'https://play.google.com'
hlgl = '&hl=en_GB&gl=us'

def get_or_default(obj, indices, fallback='', post=lambda x: x):
    i = 0
    try:
        for i in range(len(indices)):
            obj = obj[indices[i]]
        if obj is not None:
            return post(obj)
    except Exception as e:
        print(f"at i={i} in {indices}", e, '\nin obj:', obj)
    return fallback


async def get_play_store(package_name):
    url = f"{google_play_url}/store/apps/details?id={package_name}{hlgl}"
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(url) as response:
            content = await response.text()

    parts = content.split('AF_initDataCallback({')[1:]
    parts = [v.split('</script>')[0] for v in parts]
    if not parts:
        return {}

    data_string = [s for s in parts if f'["{package_name}"],' in s][0].strip()
    no_data_string = data_string[data_string.index('data:') + 5:]
    arr_string = no_data_string.split('sideChannel:')[0].strip()
    arr_string = arr_string[:-1]

    json_data = json.loads(arr_string)

    fallback = 'Varies with device'

    result = {
        "name": get_or_default(json_data, [1, 2, 0, 0], fallback),
        "category": get_or_default(json_data, [1, 2, 79, 0, 0, 0], fallback),
        "publisher": get_or_default(json_data, [1, 2, 37, 0], fallback),
        "store": f"{google_play_url}{get_or_default(json_data, [1, 2, 68, 1, 4, 2], '')}{hlgl}",
        "email": get_or_default(json_data, [1, 2, 69, 1, 0], fallback),
        "installs": get_or_default(json_data, [1, 2, 13, 0], fallback),
        "totalinstalls": get_or_default(json_data, [1, 2, 13, 2], fallback, lambda n: f"{n:,}"),
        "shortinstalls": get_or_default(json_data, [1, 2, 13, 3], fallback),
        "version": get_or_default(json_data, [1, 2, 140, 0, 0, 0], fallback),
        "updated": get_or_default(json_data, [1, 2, 145, 0, 0], fallback),
        "targetandroid": get_or_default(json_data, [1, 2, 140, 1, 0, 0, 1], fallback),
        "targetsdk": get_or_default(json_data, [1, 2, 140, 1, 0, 0, 0], fallback),
        "android": get_or_default(json_data, [1, 2, 140, 1, 1, 0, 0, 1], fallback),
        "minsdk": get_or_default(json_data, [1, 2, 140, 1, 1, 0, 0, 0], fallback),
        "rating": get_or_default(json_data, [1, 2, 51, 0, 0], fallback),
        "floatrating": get_or_default(json_data, [1, 2, 51, 0, 1], fallback),
        "numrating": get_or_default(json_data, [1, 2, 51, 2, 0], fallback),
        "friendly": get_or_default(json_data, [1, 2, 9, 0], fallback),
        "published": get_or_default(json_data, [1, 2, 10, 0], fallback)
    }
    
    return result


# get_play_store('com.lilithgame.roc.gp')
