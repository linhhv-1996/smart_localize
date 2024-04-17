import json
import asyncio
import aiohttp


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
    url = f"https://play.google.com/store/apps/details?id={package_name}"
    async with aiohttp.ClientSession() as session:
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
        "name": get_or_default(json_data, [1, 2, 0], fallback),
        "installs": get_or_default(json_data, [1, 2, 13, 0], fallback),
        "totalinstalls": get_or_default(json_data, [1, 2, 13, 2], fallback, lambda n: f"{n:,}"),
        "shortinstalls": get_or_default(json_data, [1, 2, 13, 3], fallback),
        "version": get_or_default(json_data, [1, 2, 140, 0, 0], fallback),
        "updated": get_or_default(json_data, [1, 2, 145, 0, 0], fallback),
        "targetandroid": get_or_default(json_data, [1, 2, 140, 1, 0, 0, 1], fallback),
        "targetsdk": get_or_default(json_data, [1, 2, 140, 1, 0, 0, 0], fallback),
        "android": get_or_default(json_data, [1, 2, 140, 1, 1, 0, 0, 1], fallback),
        "minsdk": get_or_default(json_data, [1, 2, 140, 1, 1, 0, 0, 0], fallback),
        "rating": get_or_default(json_data, [1, 2, 51, 0, 0], fallback),
        "floatrating": get_or_default(json_data, [1, 2, 51, 0, 1], fallback),
        "friendly": get_or_default(json_data, [1, 2, 9, 0], fallback),
        "published": get_or_default(json_data, [1, 2, 10, 0], fallback)
    }

    print(result)

    return result


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(get_play_store('com.intuit.turbotax.mobile'))

# get_play_store('com.lilithgame.roc.gp')
