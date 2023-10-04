import discord
from discord.utils import MISSING
from typing import Optional

async def response(ctx:discord.ApplicationContext, content:Optional[str] = MISSING, embed: discord.Embed = MISSING, **kwargs):
    try:
        if content:
            return await ctx.respond(content, **kwargs)
        elif embed:
            return await ctx.respond(embed=embed, **kwargs)
    
    except Exception:
        if content:
            return await ctx.response.send_message(content, **kwargs)
        elif embed:
            return await ctx.response.send_message(embed=embed, **kwargs)
    
    except:
        try:
            if content:
                return await ctx.followup.send(content, **kwargs)
            elif embed:
                return await ctx.followup.send(embed=embed, **kwargs)
        except:
            if content:
                return await ctx.send(content, **kwargs)
            elif embed:
                return await ctx.send(embed=embed, **kwargs)