# -*- coding: utf-8 -*-
import threading
import time
from mcdreforged.plugin.server_interface import *
from mcdreforged.api.decorator import *
from mcdreforged.api.command import *

PERMISSIONS = {
    'help': 0,
    'join': 1,
    'left': 1,
    'start': 1,
    'stop': 2,
}

Prefix= '!!hac'
HelpMessage='''
-------------躲猫猫插件v0.0.1---------------
§7{0} §6显示此帮助界面
§7{0} help §6显示此帮助界面
§7{0} start §6开始游戏
§7{0} stop §6强制停止开始游戏（需管理员）
§7{0} teamlist §6显示可加入队伍
§7{0} join §6加入某个队伍
§7{0} left §6退出某个队伍*如果在游戏中无法退出
§f---------------------------------------------
'''.strip().format(Prefix)

PLUGIN_METADATA = {
    'id': 'has',
    'version': '0.0.1',
    'name': 'HAS',
    'description': 'A Hide And Seek Game Plugin',
    'author': 'Sky_Dynamic',
    'link': 'https://github.com/SkyDynamic/Hide_And_Seek_Game_Plugin'
}

on = 0

def dmm_start(src: CommandSource):
    server=src.get_server()
    server.execute(f'title @a[team=cat] title "§3游戏即将开始 §2你是躲藏者，坚持5分钟"')
    server.execute(f'title @a[team=hunter] title "§3游戏即将开始 §2你是猎人，5分钟内击杀所有躲藏者"')
    on + 1

def game_stop(src: CommandSource):
    on - 1
    server=src.get_server()
    server.execute(f'effect clear @a')
    server.execute(f'clear @a')
    server.execute(f'title @a title 游戏结束')

def join_cat(src: CommandSource):
    server=src.get_server()
    server.execute(f"team add cat")
    server.execute(f"team join cat {src.player}")
    src.reply('§4你已加入躲藏者')

def join_hunter(src: CommandSource):
    server=src.get_server()
    server.execute(f"team add hunter")
    server.execute(f"team join hunter {src.player}")
    src.reply('§4你已加入追捕者')

def left(src: CommandSource):
    server=src.get_server()
    if on == 0:
        server.execute(f"team leave {src.player}")
        src.reply('§4你已退出所有队伍')
    else:
        src.reply('§4游戏正在进行！无法退出队伍')

def cheakon(src: ServerInterface):
    if on == 1:
        src.reply('游戏已经开始，无需再次输入')
    else:
        src.reply('开始游戏')
        dmm_start()

def stop(src: ServerInterface):
    if on == 0:
        src.reply('游戏还没开始')
    else:
        src.reply('游戏被强制结束')
        game_stop()

def on_load(server: ServerInterface, old):
    server.register_help_message('!!hac help', '显示躲猫猫插件帮助')
    
    server.register_command(
        Literal(Prefix).runs(lambda src: src.reply(HelpMessage)).
            then(
                Literal('help').runs(lambda src: src.reply(HelpMessage))
            ).
            then(
                Literal('join').
                    requires(lambda src: src.has_permission(PERMISSIONS['join'])).
                        then(
                            Literal('cat').runs(join_cat)
                        ).
                        then(
                            Literal('hunter').runs(join_hunter)
                        )
            ).
            then(
                Literal('left').
                    requires(lambda src: src.has_permission(PERMISSIONS['left'])).runs(left)
            ).
            then(
                Literal('start').
                    requires(lambda src: src.has_permission(PERMISSIONS['start'])).runs(cheakon)
            ).
            then(
                Literal('stop').
                    requires(lambda src: src.has_permission(PERMISSIONS['stop'])).runs(stop)
            )
        )
