import sys

import pygame

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats 
from button import Button
from scoreboard import Scoreboard 

import game_functions as gf

bg_color = (230, 230, 230)

def run_game() :
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alines Invasion")

	# 创建 Play 按钮
	play_button = Button(ai_settings, screen, "Play")

	# 创建一个存储游戏信息的实例
	stats = GameStats(ai_settings)

	# 创建一个记分板
	sb = Scoreboard(ai_settings, screen, stats)

	# 创建一艘飞船
	ship = Ship(ai_settings, screen)

	# 创建一个用于存储子弹的编组
	bullets = Group()

	"""
	# 创建一个外星人
	alien = Alien(ai_settings, screen)
	"""

	aliens = Group()

	#创建外星人群
	gf.create_fleet(ai_settings, screen, ship, aliens)

	while (True) :

		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

		if (stats.game_active) :
			ship.update()

			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()