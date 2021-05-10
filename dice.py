import discord
from discord.ext import commands
import asyncio
import globals
import logging
import db
from discord.utils import get
import utils
import random
import os
import math


class Dice(commands.Cog):
## This class is used for things that can be used in and out of battle. We have one functiont that does both.
##

    def __init__(self, bot):
        self.bot = bot

    
        
    @commands.command(pass_context=True)
    async def roll(self, ctx, arg1, silence=False, adv=False):
        dice_point = arg1.find('d')
        adjustment = 0
        plus_point = arg1.find('+')
        minus_point = arg1.find('-')
        adjust = False
        sign = '+'
        if plus_point != -1 or minus_point != -1:
            adjust = True       
        if dice_point == -1:           
            if not silence:
                await ctx.message.channel.send("You didn't include a d in your dice roll")
            return False, "You didn't include a d in your dice roll"
        try:
            num_dice = int(arg1[0:dice_point])
        except Exception as e:
            msg = "Error when verifying number of dice for roll **{}** : {}".format(arg1, e)
            if not silence:
                await ctx.message.channel.send(msg)
            return False, msg
        if not adjust:
            try:
                dice_size = int(arg1[dice_point+1::])
                adjustment_point = -1
            except Exception as e:
                msg = "Error when verifying size of dice for roll **{}** : {}".format(arg1, e)
                if not silence:
                    await ctx.message.channel.send(msg)
                return False, msg
        else:
            if plus_point == -1:
                adjustment_point = minus_point
                sign = '-'
            else:
                adjustment_point = plus_point
            try:
                dice_size = int(arg1[dice_point+1:adjustment_point])
            except Exception as e:
                msg = "Error when verifying size of dice for roll **{}** : {}".format(arg1, e)
                if not silence:
                    await ctx.message.channel.send(msg)
                return False, msg
            try:
                adjustment = int(arg1[adjustment_point+1::])
            except Exception as e:
                msg = "Error when verifying adjustment for roll **{}** : {}".format(arg1, e)
                if not silence:
                    await ctx.message.channel.send(msg)
                return False,msg
        rolls = []
        start = 1
        random.seed(os.urandom(128))
        while start < num_dice+1:
            rolls.append(random.randint(1,dice_size))        
            start += 1
        message = ":game_die: {} rolled `{}`d`{}`".format(ctx.message.author.mention, num_dice, dice_size)
        if adjustment_point != -1:
            message += '{}\n'.format(arg1[adjustment_point::])
        else:
            message += '\n'
        rlen = len(rolls)
        for i in range(0, rlen):
            message += 'Roll-{}: **{}**'.format(i+1, rolls[i])
            
            if i+1 == rlen and adjustment != 0:               
                message += '{}`{}`\n'.format(sign,adjustment)
            else:
                message += '\n'
        if sign == '+':
            total = sum(rolls) + adjustment
        else:
            total = sum(rolls) - adjustment      
        message += "`Total:` __**{}**__".format(total)
        if not silence:
            await ctx.message.channel.send(message)
        return total, ''
            
    @commands.command(pass_context=True)
    async def dcalc(self, ctx, arg1, arg2, arg3, arg4, arg5):
        base_damage, r_msg = await self.roll(ctx, arg1, True)
        if r_msg != '':
            await ctx.message.channel.send(r_msg)
            return False, ''            
        try:
            type_mult = float(arg2)
        except exception as e:
            msg = 'cannot convert type multiplier into floating number due to: {}'.format(e)
            await ctx.message.channel.send(msg)
            return False, msg
        try:
            stab = int(arg3)
        except exception as e:
            msg = 'cannot convert stab into int due to: {}'.format(e)
            await ctx.message.channel.send(msg)
            return False, msg
        try:
            atk_stat = int(arg4)
        except exception as e:
            msg = 'cannot convert attack stat into int due to: {}'.format(e)
            await ctx.message.channel.send(msg)
            return False, msg
        try:
            enemy_def = int(arg5)
        except exception as e:
            msg = 'cannot convert type multiplier into floating number due to: {}'.format(e)
            await ctx.message.channel.send(msg)
            return False, msg
            
        result = (base_damage * type_mult) + stab + atk_stat - enemy_def
        message = "You rolled a base damage of **{}**.\n{}'s pokemon did __**{}**__ damage!".format(base_damage, ctx.message.author.mention, math.ceil(result))
        await ctx.message.channel.send(message)
        return True

        



def setup(bot):
    bot.add_cog(Dice(bot))