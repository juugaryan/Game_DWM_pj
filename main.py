#сделать спавн в комнатах у двери
#exe-file
# +презентация + записка
import pygame
from pygame.locals import *
from pygame import mixer
from os import path
import worlds
import random

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

screen_width = 1600
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game')

#peremenn
cell_size = 100
clock = pygame.time.Clock()
FPS = 165
playing = 0
menu = 0
faded = False
audio_playing = True

#rr game peremenn
rr_game_st = 0
rr_game_slot = 0
rr_game_spin = 1
your_shoot = True
spin_button_clicked = False

#images:
#backgrounds
background = pygame.image.load("data/background.png")
menu_bg = pygame.image.load("data/menu_bg.png")
game_over_image = pygame.image.load("data/game_over.jpg")
#buttons
button_e_image = pygame.image.load("data/press_e_button.png")
button_r_image = pygame.image.load("data/press_r_button.png")
start_game_button_image = pygame.image.load("data/play_button.png")
settings_button_image = pygame.image.load("data/settings_button.png")
exit_button_image = pygame.image.load("data/exit_button.png")
menu_button_image = pygame.image.load("data/menu_button.png")
back_button_image = pygame.image.load("data/back_button.png")
audio_true_button_image = pygame.image.load("data/audio_button_true.png")
audio_false_button_image = pygame.image.load("data/audio_button_false.png")
info_button_image = pygame.image.load("data/info_button.png")
info_desk_image = pygame.image.load("data/info_desk.png")
#decor
key_image = pygame.image.load("data/key.png")
close_door_image = pygame.image.load("data/closed_door.png")
wardrobe_image = pygame.image.load("data/wardrobe.png")
candle_image = pygame.image.load("data/candle.png")
nps_1_image = pygame.image.load("data/main_room_hero.png")
nps_2_image = pygame.image.load("data/ded_nps.png")
nps_3_image = pygame.image.load("data/rr_hero.png")
gramophone_image = pygame.image.load("data/gramophone.png")
#rr game images
rr_game_fon_image = pygame.image.load("data/rr_game_fon.jpg")
rr_game_table_image = pygame.image.load("data/rr_game_table.png")
rr_game_revolver_image = pygame.image.load("data/rr_game_revolver.png")
rr_game_button_1_image = pygame.image.load("data/rr_button_1.png")
rr_game_button_2_image = pygame.image.load("data/rr_button_2.png")
rr_game_button_3_image = pygame.image.load("data/rr_button_3.png")
rr_game_button_4_image = pygame.image.load("data/rr_button_4.png")
rr_game_button_5_image = pygame.image.load("data/rr_button_5.png")
rr_game_button_6_image = pygame.image.load("data/rr_button_6.png")
rr_game_spin_button_image = pygame.image.load("data/rr_spin_button.png")
rr_game_shoot_button_image = pygame.image.load("data/rr_shoot_button.png")

#load sounds
pygame.mixer.music.load("data/fon_music.wav")
pygame.mixer.music.play(-1, 0.0, 5000)
pygame.mixer.music.set_volume(0.2)
bull_fx = pygame.mixer.Sound("data/bullet.wav")
bull_fx.set_volume(0.5)
spin_fx = pygame.mixer.Sound("data/drum.wav")
spin_fx.set_volume(0.5)
false_shoot_fx = pygame.mixer.Sound("data/false_shoot.wav")
false_shoot_fx.set_volume(0.5)
shoot_fx = pygame.mixer.Sound("data/shooot.wav")
shoot_fx.set_volume(0.8)
broke_box_fx = pygame.mixer.Sound("data/crush_box.wav")
broke_box_fx.set_volume(0.1)
broke_box_fx = pygame.mixer.Sound("data/crush_box.wav")
broke_box_fx.set_volume(0.1)
click_fx = pygame.mixer.Sound("data/clicked_button.wav")
click_fx.set_volume(0.2)
step_fx = pygame.mixer.Sound("data/step.wav")
step_fx.set_volume(0.1)
door_fx = pygame.mixer.Sound("data/door_fx.wav")
door_fx.set_volume(0.3)

def draw_grid():
	for line in range(0, 16):
		pygame.draw.line(screen, (255, 255, 255), (line * cell_size, 0), (line * cell_size, screen_height))
	for line in range(0, 9):
		pygame.draw.line(screen, (255, 255, 255), (0, line * cell_size), (screen_width, line * cell_size))

def dark():
	dark_surface = pygame.Surface(screen.get_size())
	dark_surface.set_alpha(0)  # начальная прозрачность
	dark_surface.fill((0, 0, 0))  # цвет: чёрный
	screen.blit(dark_surface, (0, 0))  # отображение затемненной поверхности
	pygame.display.flip()  # обновление экрана

	for i in range(0, 255, 5):  # увеличение прозрачности (затемнение)
		dark_surface.set_alpha(i)
		screen.blit(dark_surface, (0, 0))
		pygame.display.flip()
		pygame.time.delay(20)


def reset_world(world):
	nps_group.empty()
	nps2_group.empty()
	nps3_group.empty()
	gramophone_group.empty()
	door1_group.empty()
	door2_group.empty()
	door3_group.empty()
	door4_group.empty()
	destructible_box_group.empty()
	exit_group.empty()
	world_data = world
	world = World(world_data)
	world.draw()

	return world


class Player():
	def __init__(self, x, y):
		self.reset(x, y)
		self.box_count = 0
		self.audio_playing = audio_playing

	def update(self, playing):
		dx = 0
		dy = 0
		walk_kd = 20

		if menu == 1:
			#get key
			key = pygame.key.get_pressed()
			if key[pygame.K_a]:
				dx -= 2
				self.counter += 1
				self.dir_x = -1
				self.dir_y = 0
			if key[pygame.K_d]:
				dx += 2
				self.counter += 1
				self.dir_x = 1
				self.dir_y = 0
			if key[pygame.K_w]:
				dy -= 2
				self.counter += 1
				self.dir_y = 1
				self.dir_x = 0
			if key[pygame.K_s]:
				dy += 2
				self.counter += 1
				self.dir_y = -1
				self.dir_x = 0
			if key[pygame.K_a] == False and key[pygame.K_d] == False and key[pygame.K_w] == False and key[pygame.K_s] == False:
				self.counter = 0
				self.index = 0

			#animation
			if self.counter > walk_kd:
				step_fx.play()
				self.index += 1
				self.counter = 0
				if self.index >= len(self.images_down):
					self.index = 0
				if self.dir_x == 1:
					self.player_image = self.images_right[self.index]
				if self.dir_x == -1:
					self.player_image = self.images_left[self.index]
				if self.dir_y == 1:
					self.player_image = self.images_up[self.index]
				if self.dir_y == -1:
					self.player_image = self.images_down[self.index]

			# check collision
			for tile in world.tile_list:
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					dy = 0

			#check for collision with npsss:
			#nps 1
			if pygame.sprite.spritecollide(self, nps_group, False) and key[pygame.K_e]:
				if self.money_count < 20 and self.exit_key == False:
					task_1 = Task(50, 50, "Тебе нужен ключ от главной двери? Без денег я тебе его не дам, найдешь для меня 20 монет - получишь ключ.")
					task_1.draw_task()
				elif self.money_count == 20 or self.exit_key == True:
					task_1 = Task(50, 50, "Молодец! Ты собрал 20 монет, за это я даю тебе ключ.")
					task_1.draw_task()
					self.money_count = 0
					self.exit_key = True
			elif pygame.sprite.spritecollide(self, nps_group, False):
				button_e = Button(325, 150, button_e_image)
				button_e.draw_button()
				playing = 0
				if self.money_count < 20 and self.exit_key == False:
					task_1_text_1 = Task(50, 50, "Тебе нужен ключ от главной двери? Без денег я тебе его не дам, найдешь для меня 20 монет - получишь ключ.")
					task_1_text_1.draw_task()
				elif self.money_count == 20 or self.exit_key == True:
					task_1_text_1 = Task(50, 50, "Молодец! Ты собрал 20 монет, за это я даю тебе ключ.")
					task_1_text_1.draw_task()

			#nps 2
			if pygame.sprite.spritecollide(self, nps2_group, False) and key[pygame.K_e]:
				if self.box_count == 0 and self.money_count == 0:
					task_2_text_1 = Task(50, 50, "Тебе нужны деньги на ключ? Просто так я тебе ничего не дам. Сломаешь 8 коробок из этой комнаты - получишь 10 монет. (Чтобы сломать коробку используй кнопку R)")
					task_2_text_1.draw_task()
				elif self.box_count > 0 and self.box_count < 8 and self.money_count == 0:
					task_2 = Task(50, 50, f"Тебе нужно сломать больше коробок. Ты сломал только {self.box_count} коробок.")
					task_2.draw_task()
				elif self.box_count >= 8 and self.money_count == 0:
					task_2 = Task(50, 50, "Спасибо! Ты сломал все 8 коробок, держи 10 монет, ты их заслужил.")
					task_2.draw_task()
					if self.money_count == 0:
						self.money_count += 10
				elif self.money_count == 10:
					task_2 = Task(50, 50, "У меня больше нет денег. Попробуй подойти к кому-нибудь другому.")
					task_2.draw_task()
					destructible_box_group.empty()
			elif pygame.sprite.spritecollide(self, nps2_group, False):
				button_e = Button(1435, 150, button_e_image)
				button_e.draw_button()
				playing = 0
				if self.box_count == 0:
					task_2_text_1 = Task(50, 50, "Тебе нужны деньги на ключ? Просто так я тебе ничего не дам. Сломаешь 8 коробок из этой комнаты - получишь 10 монет. (Чтобы сломать коробку используй кнопку R)")
					task_2_text_1.draw_task()
				elif self.box_count > 0 and self.box_count < 8:
					task_2 = Task(50, 50, f"Тебе нужно сломать больше коробок. Ты сломал только {self.box_count} коробок.")
					task_2.draw_task()
				elif self.box_count >= 8:
					task_2 = Task(50, 50, "Спасибо! Ты сломал все 8 коробок, держи 10 монет, ты их заслужил.")
					task_2.draw_task()

			#nps 3
			if pygame.sprite.spritecollide(self, nps3_group, False) and key[pygame.K_e]:
				if self.money_count < 10:
					task_3 = Task(50, 50, "У тебя нет 10 монет. Я не буду играть с тобой просто так. Приходи когда найдешь деньги.")
					task_3.draw_task()
				elif self.money_count == 10 and your_shoot:
					playing = 2
				elif self.money_count == 10 and your_shoot == False:
					task_3 = Task(50, 50, "(Он умер. Забрать 10 монет.)")
					task_3.draw_task()
					self.money_count += 10
				elif self.money_count == 20:
					task_3 = Task(50, 50, "(Он умер.)")
					task_3.draw_task()
			elif pygame.sprite.spritecollide(self, nps3_group, False):
				button_e = Button(225, 550, button_e_image)
				button_e.draw_button()
				playing = 0
				task_3 = Task(50, 50, "Ты хочешь заработать? Мы сыграем с тобой в русскую рулетку на 10 монет, если выйграешь - заберешь мои деньги.")
				task_3.draw_task()
				if self.money_count == 10 and your_shoot == False:
					task_3 = Task(50, 50, "(Он умер. Забрать 10 монет.)")
					task_3.draw_task()
				elif self.money_count == 20:
					task_3 = Task(50, 50, "(Он умер.)")
					task_3.draw_task()

			#gramophone
			if pygame.sprite.spritecollide(self, gramophone_group, False) and key[pygame.K_e]:
				if self.audio_playing:
					self.audio_playing = False
					pygame.mixer.music.set_volume(0.0)
					click_fx.play()
					pygame.time.delay(400)
				else:
					pygame.mixer.music.set_volume(0.2)
					self.audio_playing = True
					click_fx.play()
					pygame.time.delay(400)
			elif pygame.sprite.spritecollide(self, gramophone_group, False):
				button_e = Button(1225, 550, button_e_image)
				button_e.draw_button()

			# check for collision with door
			if pygame.sprite.spritecollide(self, door1_group, False):
				playing = 6
			if pygame.sprite.spritecollide(self, door2_group, False):
				playing = 7
			if pygame.sprite.spritecollide(self, door3_group, False):
				playing = 1
			if pygame.sprite.spritecollide(self, door4_group, False):
				playing = 8

			#check for key and colision with exit
			if self.exit_key:
				if pygame.sprite.spritecollide(self, exit_group, False):
					door_fx.play()
					pygame.time.delay(1300)
					playing = 3
			else:
				if pygame.sprite.spritecollide(self, exit_group, False) and key[pygame.K_w]:
					task_exit = Task(50, 50, "Чтобы выйти из этой двери нужен ключ.")
					task_exit.draw_task()
					dy = 0

			#check for collision with box
			if pygame.sprite.spritecollide(self, destructible_box_group, False) and key[pygame.K_r]:
				if pygame.sprite.spritecollide(self, destructible_box_group, True):
					self.box_count += 1
					broke_box_fx.play()
			elif pygame.sprite.spritecollide(self, destructible_box_group, False):
				button_r = Button(self.rect.x + 25, self.rect.y - 50, button_r_image)
				button_r.draw_button()

			# update player coord
			self.rect.x += dx
			self.rect.y += dy

		#draw player
		screen.blit(self.player_image, self.rect)
		#pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

		return playing

	def reset(self, x, y):
		self.images_down = []
		self.images_up = []
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for n in range(1, 5):
			self.image_d = pygame.image.load(f'data/herooo{n}.png')
			self.images_down.append(self.image_d)
		for n in range(1, 5):
			self.image_up = pygame.image.load(f'data/heroo{n}.png')
			self.images_up.append(self.image_up)
		for n in range(1, 5):
			self.image_l = pygame.image.load(f'data/hero{n}.png')
			self.image_r = pygame.transform.flip(self.image_l, True, False)
			self.images_left.append(self.image_l)
			self.images_right.append(self.image_r)
		self.player_image = self.images_down[self.index]
		self.dir_x = -1
		self.dir_y = 0
		self.rect = self.player_image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.player_image.get_width()
		self.height = self.player_image.get_height()
		rr_game_st = 0


class World():
	def __init__(self, data):
		self.tile_list = []

		wall_image = pygame.image.load("data/wall.png")
		box_image = pygame.image.load("data/box.png")

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					image_rect = wall_image.get_rect()
					image_rect.x = col_count * cell_size
					image_rect.y = row_count * cell_size
					tile = (wall_image, image_rect)
					self.tile_list.append(tile)
				if tile == 2:
					image_rect = box_image.get_rect()
					image_rect.x = col_count * cell_size
					image_rect.y = row_count * cell_size
					tile = (box_image, image_rect)
					self.tile_list.append(tile)
				if tile == 3:
					door1 = Door(col_count * cell_size, row_count * cell_size)
					door1_group.add(door1)
				if tile == 4:
					door2 = Door(col_count * cell_size, row_count * cell_size)
					door2_group.add(door2)
				if tile == 5:
					door3 = Door(col_count * cell_size, row_count * cell_size)
					door3_group.add(door3)
				if tile == 6:
					door4 = Door(col_count * cell_size, row_count * cell_size)
					door4_group.add(door4)
				if tile == 8:
					exit = Door(col_count * cell_size, row_count * cell_size, close_door_image)
					exit_group.add(exit)
				if tile == 9:
					destructible_box = Dbox(col_count * cell_size, row_count * cell_size)
					destructible_box_group.add(destructible_box)
				if tile == 11:
					nps = Nps(col_count * cell_size, row_count * cell_size, nps_1_image)
					nps_group.add(nps)
				if tile == 12:
					nps2 = Nps(col_count * cell_size, row_count * cell_size, nps_2_image)
					nps2_group.add(nps2)
				if tile == 13:
					nps3 = Nps(col_count * cell_size, row_count * cell_size, nps_3_image)
					nps3_group.add(nps3)
				if tile == 21:
					image_rect = wardrobe_image.get_rect()
					image_rect.x = col_count * cell_size
					image_rect.y = row_count * cell_size
					tile = (wardrobe_image, image_rect)
					self.tile_list.append(tile)
				if tile == 22:
					image_rect = candle_image.get_rect()
					image_rect.x = col_count * cell_size
					image_rect.y = row_count * cell_size
					tile = (candle_image, image_rect)
					self.tile_list.append(tile)
				if tile == 23:
					gramophone = Nps(col_count * cell_size, row_count * cell_size, gramophone_image)
					gramophone_group.add(gramophone)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			#pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Nps(pygame.sprite.Sprite):
	def __init__(self, x, y, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Door(pygame.sprite.Sprite):
	def __init__(self, x, y, image=None):
		pygame.sprite.Sprite.__init__(self)
		if not image:
			self.image = pygame.image.load('data/plate.png')
		else:
			self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Dbox(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('data/not_box.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw_button(self):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		screen.blit(self.image, self.rect)
		return action


class Task():
	def __init__(self, x, y, text):
		self.x = x
		self.y = y
		self.text = text

	def draw_task(self):
		pygame.draw.rect(screen, (0, 0, 0), (0, 700, 1600, 200))
		font = pygame.font.Font(None, 25)
		text_render = font.render(self.text, True, (255, 255, 255))
		text_rect = text_render.get_rect()
		text_rect.x = self.x
		text_rect.y = screen_height - 200 + self.y
		screen.blit(text_render, text_rect)


class Money():
	def __init__(self, money):
		self.money = money

	def draw(self):
		pygame.draw.rect(screen, (0, 0, 0), (0, 0, 250, 55))
		font = pygame.font.Font(None, 40)
		text_render = font.render(f'Монет: {self.money}', True, (255, 255, 255))
		text_rect = text_render.get_rect()
		text_rect.x = 15
		text_rect.y = 15
		screen.blit(text_render, text_rect)


player = Player(750, 350)

#sprite groups
nps_group = pygame.sprite.Group()
nps2_group = pygame.sprite.Group()
nps3_group = pygame.sprite.Group()
gramophone_group = pygame.sprite.Group()
door1_group = pygame.sprite.Group()
door2_group = pygame.sprite.Group()
door3_group = pygame.sprite.Group()
door4_group = pygame.sprite.Group()
destructible_box_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#load worlds
world_data = worlds.world0
world = World(world_data)

#buttons
play_button = Button(screen_width // 2 - 250, screen_height // 2 - 200, start_game_button_image)
settings_button = Button(screen_width // 2 - 250, screen_height // 2, settings_button_image)
exit_button = Button(screen_width // 2 - 250, screen_height // 2 + 200, exit_button_image)
player_exit_button = Button(50, 50, exit_button_image)
back_button = Button(50, 50, back_button_image)
menu_button = Button(screen_width // 2 - 250, screen_height // 2 + 200, menu_button_image)
audio_true_button = Button(screen_width // 2 - 250, screen_height // 2 - 75, audio_true_button_image)
audio_false_button = Button(screen_width // 2 - 250, screen_height // 2 - 75, audio_false_button_image)
audio_button = audio_true_button

running = True
while running:

	clock.tick(FPS)
	#main menu
	if menu == 0:
		screen.blit(menu_bg, (0, 0))
		font2 = pygame.font.Font("data/Bad_Charm.ttf", 120)
		name2 = font2.render("Darkwood Manor", 1, (230, 230, 230))
		name_rect2 = name2.get_rect()
		name_rect2.x = 300
		name_rect2.y = 90
		screen.blit(name2, name_rect2)

		#game
		if play_button.draw_button():
			click_fx.play()
			player.money_count = 0
			player.exit_key = False
			player.box_count = 0
			your_shoot = True
			spin_button_clicked = False
			rr_game_st = 0
			menu = 1
			playing = 1
		#menu
		if settings_button.draw_button():
			click_fx.play()
			menu = 2
			dark()
		#exit game
		if exit_button.draw_button():
			click_fx.play()
			dark()
			running = False

	elif menu == 2:
		screen.blit(menu_bg, (0, 0))
		if back_button.draw_button():
			click_fx.play()
			dark()
			menu = 0
		if audio_playing:
			if audio_button.draw_button():
				click_fx.play()
				pygame.time.delay(300)
				pygame.mixer.music.set_volume(0.0)
				audio_button = audio_false_button
				audio_playing = False
		else:
			if audio_button.draw_button():
				click_fx.play()
				pygame.time.delay(300)
				pygame.mixer.music.set_volume(0.2)
				audio_button = audio_true_button
				audio_playing = True

		info_button = Button(1450, 50, info_button_image)
		if info_button.draw_button():
			click_fx.play()
			dark()
			menu = 3

	elif menu == 3:
		screen.blit(menu_bg, (0, 0))
		screen.blit(info_desk_image, (screen_width // 2 - 100, 50))
		if back_button.draw_button():
			click_fx.play()
			dark()
			menu = 2
		info_text = ["Darkwood Manor", "", "Главный герой попадает в дом из которого ему нужно найти",
					 "выход, для этого он должен взаимодействовать с персонажами",
					 "которые находятся с ним в одном доме, но в разных комнатах.",
					 "Герою предстоит выполнить несколько заданий, каждое из",
					 "которых может стоить ему жизни.",
					 "За каждое выполненное заданиe герой будет получать монеты,",
					 "которые помогут ему выбраться из дома."]
		font = pygame.font.Font(None, 30)
		text_coord = 115
		for line in info_text:
			string_rendered = font.render(line, 1, (255, 255, 255))
			intro_rect = string_rendered.get_rect()
			text_coord += 10
			intro_rect.top = text_coord
			intro_rect.x = 775
			text_coord += intro_rect.height
			screen.blit(string_rendered, intro_rect)

	#GAME
	elif menu == 1:
		if faded == False:
			dark()
			faded = True
		if playing == 0:
			screen.blit(background, (0, 0))
			#draw_grid()
			world.draw()
			money = Money(player.money_count)
			money.draw()
			nps_group.draw(screen)
			nps2_group.draw(screen)
			nps3_group.draw(screen)
			gramophone_group.draw(screen)
			door1_group.draw(screen)
			door2_group.draw(screen)
			door3_group.draw(screen)
			door4_group.draw(screen)
			destructible_box_group.draw(screen)
			exit_group.draw(screen)
			if player.exit_key:
				screen.blit(key_image, (player.rect.x + 5, player.rect.y - 90))
			playing = player.update(playing)
			key = pygame.key.get_pressed()
			if key[pygame.K_ESCAPE]:
				playing = 5



		if playing == 1:
			screen.blit(background, (0, 0))
			world_data = []
			world = reset_world(worlds.world0)
			playing = 0
			player.reset(750, 350)

		#rr game
		if playing == 2:
			screen.blit(rr_game_fon_image, (0, 0))
			rr_nps = pygame.transform.scale(nps_3_image, (600, 550))
			screen.blit(rr_nps, (screen_width // 2 - 300, screen_height // 2 - 200))
			screen.blit(rr_game_table_image, (screen_width // 2 - 450, screen_height // 2 + 100))
			screen.blit(rr_game_revolver_image, (screen_width // 2 + 175, screen_height // 2 + 90))

			if rr_game_st == 0:
				rr_button_play = Button(screen_width // 2 - 250, 135, start_game_button_image)
				if rr_button_play.draw_button():
					rr_game_st = 1

			if rr_game_st == 1:
				rr_game_task = Task(50, 50, "Выбери слот для пули в барабане.")
				rr_game_task.draw_task()
				rr_button_1 = Button(screen_width // 2 - 425, screen_height // 2 + 135, rr_game_button_1_image)
				rr_button_2 = Button(screen_width // 2 - 271, screen_height // 2 + 139, rr_game_button_2_image)
				rr_button_3 = Button(screen_width // 2 - 121, screen_height // 2 + 139, rr_game_button_3_image)
				rr_button_4 = Button(screen_width // 2 + 25, screen_height // 2 + 135, rr_game_button_4_image)
				rr_button_5 = Button(screen_width // 2 + 175, screen_height // 2 + 135, rr_game_button_5_image)
				rr_button_6 = Button(screen_width // 2 + 325, screen_height // 2 + 135, rr_game_button_6_image)
				if rr_button_1.draw_button():
					bull_fx.play()
					pygame.time.delay(700)
					rr_game_slot = 1
					rr_game_st = 2
				if rr_button_2.draw_button():
					bull_fx.play()
					pygame.time.delay(700)
					rr_game_slot = 2
					rr_game_st = 2
				if rr_button_3.draw_button():
					bull_fx.play()
					pygame.time.delay(700)
					rr_game_slot = 3
					rr_game_st = 2
				if rr_button_4.draw_button():
					bull_fx.play()
					pygame.time.delay(700)
					rr_game_slot = 4
					rr_game_st = 2
				if rr_button_5.draw_button():
					bull_fx.play()
					pygame.time.delay(700)
					rr_game_slot = 5
					rr_game_st = 2
				if rr_button_6.draw_button():
					bull_fx.play()
					pygame.time.delay(700)
					rr_game_slot = 6
					rr_game_st = 2

			if rr_game_st == 2:
				rr_spin_button = Button(screen_width // 2 - 550, screen_height // 2 + 135, rr_game_spin_button_image)
				rr_shoot_button = Button(screen_width // 2 + 50, screen_height // 2 + 135, rr_game_shoot_button_image)
				if your_shoot:
					rr_game_task_shoot = Task(50, 50, "Ваш ход. (Прокрутите барабан и выстрелите)")
					rr_game_task_shoot.draw_task()
				else:
					rr_game_task_shoot = Task(50, 50, "Ход соперника. (Прокрутите барабан и выстрелите)")
					rr_game_task_shoot.draw_task()
				if rr_spin_button.draw_button() and spin_button_clicked == False:
					spin_fx.play()
					rr_game_spin = random.randint(1, 6)
					print(rr_game_spin)
					spin_button_clicked = True
				if rr_shoot_button.draw_button() and spin_button_clicked:
					if your_shoot:
						if rr_game_spin == rr_game_slot:
							shoot_fx.play()
							pygame.time.delay(1000)
							playing = 4
						else:
							false_shoot_fx.play()
							your_shoot = False
					else:
						if rr_game_spin == rr_game_slot:
							shoot_fx.play()
							pygame.time.delay(500)
							playing = 7
						else:
							false_shoot_fx.play()
							your_shoot = True
					spin_button_clicked = False


		#ending
		if playing == 3:
			screen.blit(rr_game_fon_image, (0, 0))
			if player_exit_button.draw_button():
				click_fx.play()
				dark()
				menu = 0

		#game over
		if playing == 4:
			screen.fill((0, 0, 0))
			screen.blit(game_over_image, (200, 0))
			if menu_button.draw_button():
				click_fx.play()
				dark()
				menu = 0

		#pause
		if playing == 5:
			if play_button.draw_button():
				playing = 0
			if menu_button.draw_button():
				click_fx.play()
				dark()
				menu = 0

		#rooms
		if playing == 6:
			screen.blit(background, (0, 0))
			world_data = []
			world = reset_world(worlds.world1)
			playing = 0
			player.reset(750, 350)

		if playing == 7:
			screen.blit(background, (0, 0))
			world_data = []
			world = reset_world(worlds.world2)
			playing = 0
			player.reset(750, 350)

		if playing == 8:
			screen.blit(background, (0, 0))
			world_data = []
			world = reset_world(worlds.world3)
			playing = 0
			player.reset(750, 350)



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.display.update()

pygame.quit()