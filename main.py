import os
import urllib
import aiohttp
import asyncio
import shutil
from concurrent.futures import ProcessPoolExecutor

# baseurl = "https://vod-archives.castr.com/episodes/edge/64f59b2cecee14426658ed29/live_d92b9a500d2111efa998d755bcac0f4f/archive-1715495854-13098.mp4"
# baseurl = "https://vod-archives.castr.com/episodes/edge/64f59b2cecee14426658ed29/live_7fa423800d2111efb3a155268b354167/archive-1715480938-14766.mp4"
baseurl = "https://vod-archives.castr.com/episodes/edge/64f59b2cecee14426658ed29/live_01f5c2e00d2111efba7ded1836f3657e/archive-1715463918-16837.mp4"
track = "tracks-v1a1"
outdir = "out"


async def get_file(url, fname, outdir=outdir):
    print(f"DOWNLOAD `{url}` TO `{outdir}/{fname}`")
    with open(f"{outdir}/{fname}", "wb") as f:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                f.write(await res.read())
                print(f"DOWNLOADED `{fname}`")


async def main():
    await get_file("/".join([baseurl, "index.m3u8"]), "index.m3u8")
    await get_file("/".join([baseurl, track, "mono.m3u8"]), "mono.m3u8")
    if os.path.isfile(f"{outdir}/mono.m3u8"):
        with open(f"{outdir}/mono.m3u8") as f:
            tasks = []
            while l := f.readline():
                if not l.startswith("#"):
                    if os.path.isfile(f"{outdir}/{l}"):
                        print(f"skipped {l}")
                        continue
                    # task = asyncio.create_task(
                    #     get_file("/".join([baseurl, track, l]), l)
                    # )
                    # await task
                    # print(f"run {l}")
                    tasks.append(get_file("/".join([baseurl, track, l]), l))
                    if len(tasks) > 10:
                        await asyncio.gather(*tasks)
                        del tasks
                        tasks = []
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    shutil.rmtree(outdir)
    os.mkdir(outdir)
    asyncio.run(main())
