'''
icodeapi tools.

need aiofiles.
'''

import os, zipfile, shutil, json, aiofiles, asyncio, time
from . import *

async def DownloadWork(workId : str, path : str, api : AsyncIcodeAPI = AsyncIcodeAPI()):
    '''
    Download a work to your pc.
    '''
    def zipDir(dirpath, outFullName):
        """
        这段代码是CSDN上抄的毕竟我懒.
        压缩指定文件夹
        :param dirpath: 目标文件夹路径
        :param outFullName: 压缩文件保存路径+xxxx.zip
        :return: 无
        """
        zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(dirpath):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(dirpath, '')
    
            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()
    if path[-1] != '\\':
        path += '\\'
    dt = await api.getWorkDetail(workId)
    title = dt.get('title')
    code = json.loads(dt.get('code'))
    path += f'{title}\\'
    if os.path.exists(path):
        shutil.rmtree(path)
    if os.path.exists(path[:0-(len(title)+1):] + f'{title}.zip'):
        os.remove(path[:0-(len(title)+1):] + f'{title}.zip')
    if os.path.exists(path[:0-(len(title)+1):] + f'{title}.sb3'):
        os.remove(path[:0-(len(title)+1):] + f'{title}.sb3')
    os.makedirs(path)
    async with aiofiles.open(path + "project.json", 'w', encoding = 'utf-8') as f:
        await f.write(dt.get('code'))
    for i in code['targets']:
        for j in i.get('costumes'):
            if j.get('dataFormat') == 'svg':
                async with aiofiles.open(path + j.get('md5ext'), 'w', encoding ='utf-8') as f:
                    fileData = await api.getScratchAsset(j.get('md5ext'))
                    await f.write(fileData.decode('utf-8'))
            else:
                async with aiofiles.open(path + j.get('md5ext'), 'wb') as f:
                    fileData = await api.getScratchAsset(j.get('md5ext'))
                    await f.write(fileData)
        for k in i['sounds']:
            async with aiofiles.open(path + k.get('md5ext'), 'wb') as f:
                fileData = await api.getScratchAsset(k.get('md5ext'))
                await f.write(fileData)
    zipDir(path, path[:0-(len(title)+1):] + f'{title}.zip')
    shutil.rmtree(path)
    os.chdir(path[:0-(len(title)+1):])
    os.rename(path[:0-(len(title)+1):] + f'{title}.zip', f'{title}.sb3')

async def ViewNumMaker(workId : str, num : int = 5000, api : AsyncIcodeAPI = AsyncIcodeAPI(timeout = 15)):
    '''
    Let your work's viewNum become more and more!!
    '''
    tasks = [asyncio.create_task(api.getWorkDetail(workId)) for i in range(num)]
    await asyncio.wait(tasks)

def SingSong(workId : str, songWords : str, api : IcodeAPI):
    '''
    Sing a song in a work forever.

    The songWords should use "\n" to split.

    Example:
    ```python
    from icodeapi import *
    from icodeapi.tools import *
    import time
    user = IcodeAPI(input('Cookie: '))
    times = int(input('Sing times: '))
    num = 0
    while num < times:
        for i in SingSong('a1f09b5eb34a48dfbdc8dee59d130ec6',
            """You say that we will always be,
            without you I fell lost at see.
            Through the darkness you'd hide with me,
            like a wind we'd be wild and free.
            You~~~
            said you follow me anywhere.
            But your e ~ yes,
            tell me you won't be there.
            I've gotta learn how to love without you!
            I've gotta carry me cross without you~
            Stuck in the riddle and I'm just about to-----
            figure out without you!
            And I'm done sitting home without you!
            Fuck I'm going out without you!
            I'm going to tear this city without you,
            I'm going Bonnie and Clyde without you~~~
            deng deng, deng deng deng, deng deng deng deng deng deng, deng deng deng~
            deng deng, deng deng deng, deng deng deng deng deng deng deng deng deng deng~~~~""",
            user
        ):
            if i == 'Finish one time':
                num += 1
            time.sleep(5.1)
    ```
    '''
    words = songWords.split('\n')
    while True:
        for i in words:
            yield api.comment(workId, i)
        yield 'Finish one time'