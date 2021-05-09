import discord
from discord.ext import commands
import asyncio
import globals
import logging
import db
from discord.utils import get
import utils



        


class Battle(commands.Cog):

    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)      
    async def startbattle(self,ctx):
        room = ctx.message.channel_mentions[0]
        inuse, error1 = db.room_in_use(str(room.id))
        if error1 != '':
            await ctx.message.channel.send('Something went wrong with the database lookup: {}'.format(error1))
            return False
        if len(inuse) == 2:
            await ctx.message.channel.send('Room {} is in use'.format(room.mention))
            return False, ''
        result, error2 = db.start_battle(str(ctx.message.author.id), str(room.id))
        if error2 != '':
            await ctx.message.channel.send('Something went wrong with the database insert: {}'.format(error2))
            return False
        await ctx.message.channel.send('Room {} is ready for battle. Ensure that your challenger also starts the battle'.format(room.mention))

    @commands.command(pass_context=True)        
    async def ichooseu(self,ctx, arg1=''):
        if arg1 == '':
            await ctx.message.channel.send("You did not specify a pokemon")
            return False
        result, error1 = db.right_room(str(ctx.message.author.id),str(ctx.message.channel.id))
        if error1 != '':
            await ctx.message.channel.send('Data errored on verifying if you are in the right room: {}'.format(error1))
            return False
        if len(result) == 0:
            await ctx.message.channel.send('You are not in the right room. Please choose your pokemon in the right room')
            return False
        result, error2 = db.choose_pokemon(str(ctx.message.author.id),arg1)
        if error2 != '':
            await ctx.message.channel.send('Database error in choosing pokemon: {}'.format(error2))
            return False
        await ctx.message.channel.send('{} has sent out {}! Prepare for BATTLE!!'.format(ctx.message.author.mention, arg1))        

    @commands.command(pass_context=True)
    async def endbattle(self, ctx):
        result, error = db.end_battle(str(ctx.message.author.id))
        if error != '':
            await ctx.message.channel.send('Failed to end battle')
            return False
        else:
            await ctx.message.channel.send('Battle ended')
        
    @commands.command(pass_context=True)
    async def dmg(self, ctx, arg1, arg2):
        trainer = str(ctx.message.author.id)
        print ('About to do damage')
        pokemon, error1 = db.get_battle_pokemon(trainer,arg1)
        if error1 != '':
            await ctx.message.channel.send('Something went wrong with verifying pokemon is in battle: {}'.format(error1))
            return False     
        if len(pokemon) == 0:
            await ctx.message.channel.send('{} is not in battle to damage'.format(pokemon[1]))
            return False
        pokemon = pokemon[0]
        curr_hp = pokemon[3]
        new_hp = int(curr_hp) - int(arg2)
        result, error2 = db.update_stat(trainer, arg1, 'HP', new_hp, True)
        if error2 != '':
            await ctx.message.channel.send('Something went wrong with setting damage: {}'.format(error2))
            return False
        msg1 = '{} now has {} hp.'.format(arg1, new_hp)
        if new_hp < 1:
            msg1 += 'They have been defeated'
        await ctx.message.channel.send(msg1)
             
    @commands.command(pass_context=True)
    async def status(self, ctx, arg1, arg2):
        pass
    
        
    
    
        
        
        

def setup(bot):
    bot.add_cog(Battle(bot))
 