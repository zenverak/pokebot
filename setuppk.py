import discord
from discord.ext import commands
import asyncio
import globals
import logging
import db
from discord.utils import get
import utils



        


class SetupPk(commands.Cog):

    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def newpk(self, ctx):
        trainer = str(ctx.message.author.id)
        message = ctx.message.content.replace('$newpk','').lstrip(' ')
        ints = ['DEF','ATK','HP','SPDEF','SPATK','SPEED']
        pokemon = {}
        parameters = message.split('\n')
        print('lets remove empty space')
        if parameters[0] == '':
            parameters.pop(0)
        print("removed empty space if there was any")   
        for param in parameters:
            start = param.find(':')
            key = param[0:start]
            value = param[start+1::].lstrip(' ')
            if key in ints:
                try:
                    value = int(value)
                except:
                    await ctx.message.channel.send('Please ensure that {} is an interger and not a string'.format(key))
                    return False, 'Stats need to be an integer'                  
            pokemon[key] = value      
        print(pokemon)
        exist, error = db.get_pokemon(trainer,pokemon['NAME'])
        if error != '':
            await ctx.message.channel.send('We had an error when trying to verify if pokemon existed: {}'.format(error))
            return False, error
        if len(exist) > 0:
            await ctx.message.channel.send("This pokemon already exists")
            return False, 'already exists'
        result, error = db.create_pokemon(trainer, pokemon['NAME'], pokemon['SPECIES'], pokemon['HP'], pokemon['ATK'], pokemon['DEF'], \
              pokemon['SPATK'], pokemon['SPDEF'], pokemon['SPEED'], pokemon['ATTACK1'], pokemon['ATTACK2'], pokemon['ATTACK3'], \
              pokemon['ATTACK4'], pokemon['ABOUT'])
        if error != '':
            await ctx.message.channel.send('Could not create pokemon: {}'.format(error))
            return False, error
        
        await ctx.message.channel.send("{} has been created".format(pokemon['NAME']))
        return True, ''



    async def newpk2(self, ctx, silence=False):
        trainer = str(ctx.message.author.id)
        message = ctx.message.content.replace('$newpk','').lstrip(' ')
        ints = ['DEF','ATK','HP','SPDEF','SPATK','SPEED']
        pokemon = {}
        parameters = message.split('\n')
        print('lets remove empty space')
        if parameters[0] == '':
            parameters.pop(0)
        print("removed empty space if there was any")   
        for param in parameters:
            start = param.find(':')
            key = param[0:start]
            value = param[start+1::].lstrip(' ')
            if key in ints:
                try:
                    value = int(value)
                except:
                    await ctx.message.channel.send('Please ensure that {} is an interger and not a string'.format(key))
                    return False, 'Stats need to be an integer'                  
            pokemon[key] = value      
        print(pokemon)
        exist, error = db.get_pokemon(trainer,pokemon['NAME'])
        if error != '':
            await ctx.message.channel.send('We had an error when trying to verify if pokemon existed: {}'.format(error))
            return False, error
        if len(exist) > 0:
            await ctx.message.channel.send("This pokemon already exists")
            return False, 'already exists'
        result, error = db.create_pokemon(trainer, pokemon['NAME'], pokemon['SPECIES'], pokemon['HP'], pokemon['ATK'], pokemon['DEF'], \
              pokemon['SPATK'], pokemon['SPDEF'], pokemon['SPEED'], pokemon['ATTACK1'], pokemon['ATTACK2'], pokemon['ATTACK3'], \
              pokemon['ATTACK4'], pokemon['ABOUT'])
        if error != '':
            await ctx.message.channel.send('Could not create pokemon: {}'.format(error))
            return False, error
        if not silence:
            await ctx.message.channel.send("{} has been created".format(pokemon['NAME']))
            return True, ''
        return True, ''
        
        
    async def newtrainer(self, ctx):
        pass


    @commands.command(pass_context=True)        
    async def updatepk(self, ctx, *args):
        trainer = str(ctx.message.author.id)
        arg1 = args[0]
        print(arg1)
        result, error1 =  db.delete_pk(trainer, arg1)
        print("I was able to delete: {}".format(result))
        if error1 != '':
            await ctx.message.channel.send("Failed to delete pokemon: {}".format(error1))
            return False
        result,error2 = await self.newpk2(ctx, True)
        if result:
            await ctx.message.channel.send('Pokemon {} has been updated'.format(arg1))
        else:
            await ctx.message.channel.send("we had an error: {}".format(error2))
            await ctx.message.channel.send('Could not update {}. If you see this, please run $newpk with the same template you just used.'.format(arg1))
        
        


  
       


    
    
def setup(bot):
    bot.add_cog(SetupPk(bot))
