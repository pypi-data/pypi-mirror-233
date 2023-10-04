import discord, datetime, os

class Embed(discord.Embed):
    def default(ctx=None | discord.ApplicationContext, title: str = None, description: str = None, **kwargs):
        embed = discord.Embed(**kwargs, colour=discord.Color.embed_background("dark"))
        if not title is None:
            embed.title = title

        if not description is None:
            embed.description = f"```css\n{description}```"

        try:
            try:
                name = ctx.author.global_name
            except:
                name = ctx.author.display_name
            embed.set_footer(text=f"{name} | {datetime.datetime.now().strftime('%m월 %d일 %H시 %M분')}", icon_url=ctx.author.display_avatar)
        except:
            pass
        
        return embed
    
    def Green(ctx=None, title: str = None, description: str = None, **kwargs):
        embed = discord.Embed(**kwargs, colour=discord.Colour.green())
        if not title is None:
            embed.title = title
        else:
            embed.title = f'**<:yes:1088400409741234246> 성공**'

        if not description is None:
            embed.description = f"```css\n{description}```"
        
        try:
            try:
                name = ctx.author.global_name
            except:
                name = ctx.author.display_name
            embed.set_footer(text=f"{name} | {datetime.datetime.now().strftime('%m월 %d일 %H시 %M분')}", icon_url=ctx.author.display_avatar)
        except:
            pass

        return embed
    
    def Red(ctx=None | discord.ApplicationContext, title: str = None, description: str = None, **kwargs):
        embed = discord.Embed(**kwargs, colour=discord.Colour.red())
        if not title is None:
            embed.title = title
        else:
            embed.title=f'**<:no:1049248679694974987>  실패**'
        if not description is None:
            embed.description = f"```css\n{description}```"
        
        try:
            try:
                name = ctx.author.global_name
            except:
                name = ctx.author.display_name
            embed.set_footer(text=f"{name} | {datetime.datetime.now().strftime('%m월 %d일 %H시 %M분')}", icon_url=ctx.author.display_avatar)
        except:
            pass
        
        return embed