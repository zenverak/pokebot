import discord 

def OLD_create_pk_embed(pokemon):
    embed=discord.Embed(title=pokemon[2], color=0xde1717)
    embed.add_field(name='Species: {}'.format(pokemon[3]), value='\u200b', inline=False)
    embed.add_field(name='HP: {}'.format(pokemon[4]), value='\u200b', inline=False)
    embed.add_field(name='ATK: {}'.format(pokemon[5]), value='\u200b', inline=False)
    embed.add_field(name='DEF: {}'.format(pokemon[6]), value='\u200b', inline=False)
    embed.add_field(name='SPATK: {}'.format(pokemon[7]), value='\u200b', inline=False)
    embed.add_field(name='SPDEF: {}'.format(pokemon[8]), value='\u200b', inline=False)
    embed.add_field(name='SPEED: {}'.format(pokemon[9]), value='\u200b', inline=False)
    embed.add_field(name='ATTACK1: {}'.format(pokemon[10]), value='\u200b', inline=False)
    embed.add_field(name='ATTACK2: {}'.format(pokemon[11]), value='\u200b', inline=False)
    embed.add_field(name='ATTACK3: {}'.format(pokemon[12]), value='\u200b', inline=False)
    embed.add_field(name='ATTACK4: {}'.format(pokemon[13]), value='\u200b', inline=False)
    embed.add_field(name='ABOUT: {}'.format(pokemon[14]), value='\u200b', inline=False)
    return embed
    
    
    
def create_pk_embed(pokemon):
    embed=discord.Embed(title=pokemon[2], color=0xde1717)
    embed.add_field(name='Species:', value=pokemon[3], inline=False)
    embed.add_field(name='HP:', value=pokemon[4], inline=True)
    embed.add_field(name='ATK:', value=pokemon[5], inline=True)
    embed.add_field(name='DEF:', value=pokemon[6], inline=True)
    embed.add_field(name='SPATK:', value=pokemon[7], inline=True)
    embed.add_field(name='SPDEF:', value=pokemon[8], inline=True)
    embed.add_field(name='SPEED:', value=pokemon[9], inline=True)
    embed.add_field(name='ATTACK1:', value=pokemon[10], inline=False)
    embed.add_field(name='ATTACK2:', value=pokemon[11], inline=False)
    embed.add_field(name='ATTACK3:', value=pokemon[12], inline=False)
    embed.add_field(name='ATTACK4:', value=pokemon[13], inline=False)
    embed.add_field(name='ABOUT:', value=pokemon[14], inline=False)
    return embed      
    
def create_pk_battle_embed(pokemon):
    embed=discord.Embed(title='{} in battle'.format(pokemon[1]), color=0xde1717)
    embed.add_field(name='Species:', value=pokemon[2], inline=False)
    embed.add_field(name='HP:', value=pokemon[3], inline=True)
    embed.add_field(name='ATK:', value=pokemon[4], inline=True)
    embed.add_field(name='DEF:', value=pokemon[5], inline=True)
    embed.add_field(name='SPATK:', value=pokemon[6], inline=True)
    embed.add_field(name='SPDEF:', value=pokemon[7], inline=True)
    embed.add_field(name='SPEED:', value=pokemon[8], inline=True)
    embed.add_field(name='ATTACK1:', value=pokemon[9], inline=False)
    embed.add_field(name='ATTACK2:', value=pokemon[10], inline=False)
    embed.add_field(name='ATTACK3:', value=pokemon[11], inline=False)
    embed.add_field(name='ATTACK4:', value=pokemon[12], inline=False)
    embed.add_field(name='ABOUT:', value=pokemon[13], inline=False)
    return embed        