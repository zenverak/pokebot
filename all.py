import discord
from discord.ext import commands
import asyncio
import globals
import logging
import db
from discord.utils import get
import utils





class Any(commands.Cog):
## This class is used for things that can be used in and out of battle. We have one functiont that does both.
##

    def __init__(self, bot):
        self.bot = bot
  
    @commands.command(pass_context=True)
    async def showpk(self, ctx, *args):
        trainer = str(ctx.message.author.id)
        trainer_name = ctx.message.author.name
        name = '' 
        if len(args) == 2: 
            trainer = str(ctx.message.mentions[0].id)
            trainer_name = ctx.message.mentions[0].name
            name = args[1]
        else:
            name = args[0]
        result, error1 = db.get_battle_pokemon(trainer,name)
        if error1 != '':
            await ctx.message.channel.send('Something went wrong with verifying pokemon is in battle: {}'.format(error1))
            return False
        if len(result) == 0:       
            pokemon,error2 = db.get_pokemon(trainer, name)
            if error2 != '':
                await ctx.message.channel.send('Something went wrong Getting pokemon: {}'.format(error2))
            if len(pokemon) == 0:
                await ctx.message.channel.send("Trainer {} has no pokemon named {}".format(trainer_name, name))
                return False
            print(pokemon)
            embed = utils.create_pk_embed(pokemon[0])
            await ctx.message.channel.send(embed=embed)
        else:
            pokemon = result             
            if len(pokemon) == 0:
                await ctx.message.channel.send("Trainer {} has no pokemon named {} in battle".format(trainer_name, name))
                return False
            print(pokemon)
            embed = utils.create_pk_battle_embed(pokemon[0])
            await ctx.message.channel.send(embed=embed)

    @commands.command(pass_context=True)    
    async def listpk(self, ctx, arg1=''):
    ##used to list all pokemon from a specific trainer 
        if arg1 != '':
            trainer = str(ctx.message.mentions[0].id)
            tname = ctx.message.mentions[0].name
        else:
            trainer = str(ctx.message.author.id)
            tname = ctx.message.author.name
        pokemon, error = db.list_pk(trainer)
        if error != '':
            await ctx.message.channel.send('Could not get pokemon due to error: {}'.format(error))
            return False
        embed = utils.create_list_pk(pokemon,tname)
        await ctx.message.channel.send(embed=embed)
        
    
    @commands.command(pass_context=True)    
    async def updatestat(self, ctx, arg1, arg2, arg3):
        stats = ['hp','def','spatk','spdef','speed','atk']
        if arg2.lower() not in stats:
            await ctx.message.channel.send('Stat {} does not exist'.format(arg2))
            return False
        trainer = str(ctx.message.author.id)
        pokemon, error1 = db.get_battle_pokemon(trainer,arg1)
        if error1 != '':
            await ctx.message.channel.send('Something went wrong with verifying pokemon is in battle: {}'.format(error1))
            return False
        if len(arg3) < 2:
            await ctx.message.channel.send('Ensure that your stat value has a + or - and at least one number: {} did not'.format(arg3))
            return False
        sign = arg3[0]
        try:
            num = int(arg3[1::])
        except:
            await ctx.message.channel.send('Ensure that your stat value has a + or - and then a number: {} did not'.format(arg3))
            return False
        if sign == '-':
            num = -1 * num
        if len(pokemon) == 0:
            indexes = globals.STAT_LOC
            pokemon, error = db.get_pokemon(trainer,arg1)
            idx = indexes[arg2.lower()]
            current_val = pokemon[0][idx]
            new_val = current_val + num
            result, error2 = db.update_stat(trainer, arg1, arg2, new_val)
            if error2 != '':
                await ctx.message.channel.send('could not update stat due to error: {}'.format(error2))
                return False
            await ctx.message.channel.send("{}'s {} stat is now permanently {}".format(arg1, arg2, new_val))                           
        else:
            indexes = globals.STAT_LOC_BATTLE
            idx = indexes[arg2.lower()]
            current_val = pokemon[0][idx]
            new_val = current_val + num
            result, error2 = db.update_stat(trainer, arg1, arg2, new_val, True)
            if error2 != '':
                await ctx.message.channel.send('could not update stat due to error: {}'.format(error2))
                return False
            await ctx.message.channel.send("{}'s {} stat is now {} for this battle".format(arg1, arg2, new_val))
             

def setup(bot):
    bot.add_cog(Any(bot))
 