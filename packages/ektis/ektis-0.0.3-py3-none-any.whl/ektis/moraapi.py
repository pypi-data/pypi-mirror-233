import aiohttp, json, discord
from .embed import Embed

BaseApi = 'https://mora-bot.kr/api/'

class VA:
    async def weather(area:str, title:str, simple=True, ctx:discord.ApplicationContext=None):
        """
        ## 원하는 지역의 날씨 정보를 조회합니다\n
        area : 날씨를 검색할 지역\n
        title : 임배드에 넣을 제목(simple=False일땐 기입 X)\n
        simple : \n
            True : 임배드 반환\n
            False : 딕셔너리 반환
        """
        if not title:
            title = f"{area} 날씨"

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{BaseApi}v2/weather?area={area}') as resp:
                if resp.status != 200:
                    return Embed.Red(title=f"| Error | api에서 오류가 났습니다 : {resp.status}에러")
                response = await resp.json()
                
                if simple == True:
                    embed = Embed.default(ctx, title=title)
                    embed.add_field(name=f"| 온도 | {response['Temperature']}도", value="ㅤ", inline=False)
                    embed.add_field(name=f"| 체감온도 | {response['windchilltemperature']}도", value="ㅤ", inline=False)
                    embed.add_field(name=f"| 풍량 | {response['wind']}", value="ㅤ", inline=False)
                    embed.add_field(name=f"| 습도 | {response['Humidity']}", value="ㅤ", inline=False)
                    
                    return embed
                
                else:
                    return response

    async def nsfw(simple=True):
        """
        ## waifu의 사진을 가져옵니다\n
        simple : \n
            True : 임배드 반환\n
            False : 딕셔너리 반환
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{BaseApi}v3/nsfw') as resp:
                if resp.status != 200:
                    return Embed.Red(title=f"| Error | api에서 오류가 났습니다 : {resp.status}에러")
                response = await resp.json()
                
                if simple == True:
                    embed = Embed.default()
                    embed.set_image(url=response['img'])
                    return embed
                else:
                    return response
    
    async def qr_code(url:str, simple=True):
        """
        ## 입력한 링크를 QR코드로 변환합니다\n
        url : QR코드로 변환할 링크
        simple : \n
            True : 임배드 반환\n
            False : 딕셔너리 반환
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{BaseApi}v2/qr?url={url}') as resp:
                if resp.status != 200:
                    return Embed.Red(title=f"| Error | api에서 오류가 났습니다 : {resp.status}에러")
                response = await resp.json()
                
                if simple == True:
                    embed = Embed.default()
                    embed.set_image(url=response['Image'])
                    return embed
                
                else:
                    return response