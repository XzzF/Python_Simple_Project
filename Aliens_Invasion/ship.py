import pygame
from pygame.sprite import Sprite

class Ship (Sprite) :
	def __init__(self, ai_settings, screen) :
		""" 初始化飞船并设置其初始位置 """

		super(Ship, self).__init__()
		
		self.screen = screen
		self.ai_settings = ai_settings

		# 加载飞船图像并获取其外接矩形
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# 将初始化的新飞船放在屏幕底部中央
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		# 定义飞船的center属性,并使其存储小数
		self.center = float(self.rect.centerx)

		# 移动标志
		self.moving_right = False
		self.moving_left = False

	def update(self) :
		""" 根据移动标志调整位置 """
		# 更新飞船的center值,而不是rect
		if (self.moving_right == True and self.rect.right < self.screen_rect.right) :
			self.center += self.ai_settings.ship_speed_factor
		if (self.moving_left == True and self.rect.left > 0) :
			self.center -= self.ai_settings.ship_speed_factor

		self.rect.centerx = self.center

	def blitme(self) :
		# 绘制飞船
		self.screen.blit(self.image, self.rect)


	def center_ship(self) :
		""" 让飞船在屏幕中央 """

		self.center = self.screen_rect.centerx