
class Settings () :
	""" 设置类 """
	def __init__ (self) :
		""" 初始化游戏的静态设置 """

		# 屏幕设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		# 飞船的设置
		self.ship_limit = 3


		# 子弹设置
		self.bullet_width = 5
		self.bullet_height = 10
		self.bullet_color = (60, 60, 60)

		# 未消失的最大子弹数
		self.bullets_allowed = 10


		# 外星人设置
		self.fleet_drop_speed = 10


		# 以怎样的速度加快游戏节奏
		self.speedup_scale = 1.1

		# 外星人分值的提高速度
		self.score_scale = 1.5

		self.initialize_dynamic_settings()



	def initialize_dynamic_settings(self) :
		""" 初始化游戏的动态设置 """

		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 2
		self.alien_speed_factor = 1

		# 1 表示右移, -1 表示左移
		self.fleet_direction = 1

		# 记分
		self.alien_point = 50

	def increase_speed(self) :
		""" 提高速度设置和外星人分值 """

		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

		# 提高外星人分值
		self.alien_point = int(self.alien_point * self.score_scale)
		# print (self.alien_point)