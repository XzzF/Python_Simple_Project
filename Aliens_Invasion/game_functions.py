import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, stats, ship, bullets) :
	"""响应按键"""

	# 左右移动
	if (event.key == pygame.K_RIGHT) :
		ship.moving_right = True
	elif (event.key == pygame.K_LEFT) :
		ship.moving_left = True

	# 空格键发射子弹
	elif (event.key == pygame.K_SPACE) :
		fire_bullet(ai_settings, screen, ship, bullets)	

	# q 退出游戏
	elif (event.key == pygame.K_q) :
		write_high_score(stats)
		sys.exit()

def check_keyup_events(event, ship) :
	if (event.key == pygame.K_RIGHT) :
		ship.moving_right = False
	elif (event.key == pygame.K_LEFT) :
		ship.moving_left = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y) :
	""" 在单击 Play 按钮是开始新游戏 """

	button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
	if (button_click and (not stats.game_active)) :

		# 重置游戏设置
		ai_settings.initialize_dynamic_settings()

		# 隐藏光标
		pygame.mouse.set_visible(False)

		# 重置游戏统计信息

		stats.reset_stats()
		stats.game_active = True

		# 重置记分板图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		# 清空外星人和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建一群新的外星人, 并让飞船居中
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets) :
	# 监视键盘和鼠标事件
	for event in pygame.event.get() :
		if (event.type == pygame.QUIT) :
			write_high_score(stats)
			sys.exit()

		elif (event.type == pygame.KEYDOWN) :
			check_keydown_events(event, ai_settings, screen, stats, ship, bullets)

		elif (event.type == pygame.KEYUP) :
			check_keyup_events(event, ship)

		elif (event.type == pygame.MOUSEBUTTONDOWN) :
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
			

# ----------------------------------------------------------------------- #


def fire_bullet (ai_settings, screen, ship, bullets) :
	# 创建一颗子弹,并将其加入到 bullets 编组中
	# 如果没达到限制, 就发射一颗子弹
	if (len(bullets) < ai_settings.bullets_allowed) : 
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)



def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button) :
	"""更新屏幕上的图像"""

	# 每次循环都重绘屏幕
	screen.fill(ai_settings.bg_color)

	# 重绘所有子弹
	for blt in bullets.sprites() :
		blt.draw_bullet()

	# 绘制飞船
	ship.blitme()

	# 绘制外星人群
	aliens.draw(screen)
	"""    
	# 三种方法都可以, 
	for aln in aliens.sprites() :
		aln.blitme();
	for aln in aliens :
		aln.blitme()
	"""

	# 显示得分
	sb.show_score()

	# 如果游戏处于非活动状态, 就显示 Play 按钮
	if (not stats.game_active) :
		play_button.draw_button()

	# 让最近绘制的屏幕可见
	pygame.display.flip();


def check_high_score(stats, sb) :
	""" 检查是否产生了新的最高分 """
	if (stats.score > stats.high_score) :
		stats.high_score = stats.score
		sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets) :
	""" 响应子弹和外星人的碰撞 """

	# 检查是否有子弹击中了外星人
	# 如果有, 则删除相应的子弹和外星人
	# 第一个 True 表示要删除发生碰撞的 bullet  (False 则不删除)
	# 第二个 True 表示要删除发生碰撞的 alien   (False 则不删除)
	collosions = pygame.sprite.groupcollide(bullets, aliens, True, True)

	if (collosions) :
		for alns in collosions.values() :
			stats.score += ai_settings.alien_point * len(alns)
			sb.prep_score()

		# 检查是否出现最高分
		check_high_score(stats, sb)

	# 整群外星人被消灭
	if (len(aliens) == 0) :
		# 删除现有子弹, 并新建一群外星人, 还加快游戏节奏
		bullets.empty()
		ai_settings.increase_speed()

		# 提高一个等级
		stats.level += 1
		sb.prep_level()

		create_fleet(ai_settings, screen, ship, aliens)


def update_bullets (ai_settings, screen, stats, sb, ship, aliens, bullets) :
	""" 更新子弹的位置, 并删除已消失的子弹"""

	# 自动对编组内的每个子弹调用 bullets.update()
	bullets.update()

	# 删除已消失的子弹
	for blt in bullets.copy() :
		if (blt.rect.bottom <= 0) :
			bullets.remove(blt)
	# print (len(bullets))

	# 检查子弹和外星人的碰撞
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
	

# --------------------------------------------------------------------- #

def check_fleet_edges(ai_settings, aliens) :
	""" 有外星人到达边缘时采相应的措施 """

	for aln in aliens.sprites() :
		if (aln.check_edges()) :
			change_fleet_direction(ai_settings, aliens)
			break


def change_fleet_direction(ai_settings, aliens) :
	""" 将整群外星人下移, 并改变它们的方向 """

	for aln in aliens.sprites() :
		aln.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1


# ------------------------------------------------------------------- #

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets) :
	""" 响应被外星人撞到的飞船"""

	if (stats.ships_left > 0) :
		# 将 ship_left 减 1
		stats.ships_left -= 1

		# 更新记分板
		sb.prep_ships()

		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建一群新的外星人, 并将飞船放到屏幕底部的中央
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# 暂停
		sleep(0.5)

	else :
		stats.game_active = False
		# 游戏一结束就马上显示光标
		pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets) :
	""" 检查是否有外星人到达了屏幕底端 """

	screen_rect = screen.get_rect()
	for aln in aliens.sprites() :
		if (aln.rect.bottom >= screen_rect.bottom):
			# 像飞船被撞一样处理
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets) :
	""" 更新外星人群中所有外星人的位置 """

	check_fleet_edges(ai_settings, aliens)
	aliens.update()


	# 检查外星人和飞船之间的碰撞
	if (pygame.sprite.spritecollideany(ship, aliens)) :
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
		#print ("Ship hit !!!")

	# 检查是否有外星人到达屏幕底端
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

# ---------------------------------------------------------------------- #


def get_number_aliens_x(ai_settings, alien_width) :
	""" 计算每行可以容纳多少外星人 """

	available_space_x = ai_settings.screen_width - 2 * alien_width    #两边留空
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height) :
	""" 计算屏幕可以容纳多少行外星人 """

	available_space_y = (ai_settings.screen_height - (5 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number) :
	""" 创建一个外星人并将其放在当前行 """

	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	# 左上角的横纵坐标
	alien.rect.x = alien.x   
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens) :
	""" 创建外星人群 """

	# 先创建一个外星人,然后计算一行可以容纳多少外星人
	# 外星人间距为外星人宽度

	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	# 创建外星人群
	for row_number in range (number_rows) :
		for alien_number in range (number_aliens_x) :
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

		

	# print (len(aliens))




# --------------------------------------- #

def write_high_score(stats) :
	filename = 'highest.txt'

	with open(filename, 'w') as file_obj :
		file_obj.write(str(stats.high_score))