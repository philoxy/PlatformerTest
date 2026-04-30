import pygame
from pygame.locals import *
import sys, json
# import antigravity

# to do list:
# redo camera movement cuz its broken


# the tiles make me want to make the 1st level azure lake zone

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 480
WIDTH = 640
# ACC = 0.2
FRIC = -0.12
FPS = 60
global jumps
jumps = 2
global offsetX
offsetX = 0
global offsetY
offsetY = 0
move = 3
gravity = 1
global camerabounds
camerabounds = 300
global direction
direction = 1
# 0 = left
# 1 = right
global hits
hits = False
hor_collision = False

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT), vsync=True)
pygame.display.set_caption("Platformer Test")	
icon = pygame.image.load("assets/player.png")
pygame.display.set_icon(icon)
# replace direction system because animations
player = pygame.image.load("assets/player.png")
flipped_player = pygame.transform.flip(player, True, False)

class Player(pygame.sprite.Sprite):
	def __init__(self, image_path, position):
		super().__init__()
		self.surf = pygame.Surface(position)
		#self.surf.fill((128,255,40))
		self.rect = self.surf.get_rect()

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(topleft=position)
		self.mask = None
	
		self.pos = vec(position)
		self.vel = vec(0,0)
		self.mask = None

	def move(self):
		global hor_collision
		global move
		global offsetX
		global camerabounds
		global direction
		global gravity

		self.acc = vec(0,0.3)

		pressed_keys = pygame.key.get_pressed()

		if pressed_keys[K_LSHIFT]:
			# ACC2 = 2*ACC
			move = 5
		else:
			# ACC2 = ACC
			move = 3

		"""failed horizontal collision
		P1.pos.y += 1
		if pressed_keys[K_LEFT]:
			P1.pos.x -= move
			if pygame.sprite.collide_mask(self, Platform):
				hor_collision = True
			else:
				hor_collision = False
			P1.pos.x += move
		elif pressed_keys[K_RIGHT]:
			P1.pos.x += move
			if pygame.sprite.collide_mask(self, Platform):
				hor_collision = True
			else:
				hor_collision = False
		P1.pos.y -= 1
		"""

		if hor_collision == False:
			if camerabounds < self.pos.x < (WIDTH-camerabounds):
				if pressed_keys[K_LEFT]:
					self.pos.x -= move
					direction = 0
				if pressed_keys[K_RIGHT]:
					self.pos.x += move
					direction = 1
			else: 
				if pressed_keys[K_LEFT]:
					# self.acc.x = 0
					# self.acc.x = -ACC
					offsetX += move
					self.pos.x -= move
					direction = 0
				if pressed_keys[K_RIGHT]:
					offsetX -= move
					self.pos.x += move
					direction = 1

		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc*gravity
		self.pos += self.vel + 0.5 * self.acc

		if self.pos.x > WIDTH-camerabounds:
			self.pos.x = WIDTH-camerabounds
		if self.pos.x < camerabounds:
			self.pos.x = camerabounds

		self.rect.midbottom = self.pos
		
	
	def update(self):
		self.mask = pygame.mask.from_surface(self.image)

		global direction
		#hits = pygame.sprite.spritecollide(self, platforms, False)
		#if self.rect.bottom == platforms.rect.top:
		#if self.vel.y > 0:
			#if hits:
				#if self.pos.y + 32 <= platforms.pos.y and platforms.pos.x + 64 > self.pos.x > platforms.pos.x - 32:
				#self.pos.y = hits[0].rect.top + 1
				#self.vel.y = 0
		if direction == 0:
			self.image = flipped_player

		elif direction == 1:
			self.image = player

	def jump(self):
		global jumps
		global gravity
		global hits

		#hits = pygame.sprite.spritecollide(self, platforms, False)
		#if hits or self.vel.y == 0:
			#jumps = 2
		#if jumps > 0:
			#if jumps == 2:
		self.vel.y = -(gravity*7)
				#jumps = 1
			#elif jumps == 1:
				#self.vel.y = -(gravity*2)
				#jumps = 0

class Platform(pygame.sprite.Sprite):
	def __init__(self, image_path, position):
		super().__init__()
		self.surf = pygame.Surface(position)
		self.surf.fill((250,0,0))
		self.rect = self.surf.get_rect(topleft=position)

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(topleft=position)
		self.pos = vec(position)
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		global move
		global hits
		global saved_x
		global saved_y
		global direction
		saved_x = P1.pos.x
		saved_y = P1.pos.y
		global hor_collision
		#self.pos.x += offsetX

		#hits = self.sprite.spritecollide(P1.rect)

		#self.rect.midbottom = self.pos
		self.rect.midbottom = (self.pos.x + offsetX, self.pos.y)
		self.mask = pygame.mask.from_surface(self.image)

		"""
		if pygame.sprite.collide_mask(P1, self):
			if P1.vel.y > 0:
				P1.rect.bottom = self.rect.top
				P1.pos.y = P1.rect.bottom
				P1.vel.y = 0
			elif P1.vel.y < 0:
				P1.rect.top = self.rect.bottom
				P1.pos.y = P1.rect.bottom
				P1.vel.y = 0
			#elif direction == 0:
			#	P1.rect.left = self.rect.right
			#	P1.pos.x = P1.rect.left
			#elif direction == 1:
			#	P1.rect.right = self.rect.left
			#	P1.pos.x = P1.rect.left
			"""

		#for obj in all_sprites:
		#	if pygame.sprite.collide_mask(P1, obj):
		#		collided_object = obj
		#		break

		#	if direction == 0:
		#		P1.pos.x -= move
		#	elif direction == 1:
		#		P1.pos.x += move

		if pygame.sprite.collide_mask(P1, self):
				#if hits:
					#if self.pos.y + 32 <= platforms.pos.y and platforms.pos.x + 64 > self.pos.x > platforms.pos.x - 32:
						#self.pos.y = hits[0].rect.top + 1
						#self.vel.y = 0

			"""
			# inconsistent commenting
			# Calculate overlap distances
			dx_left = P1.rect.right - self.rect.left
			dx_right = self.rect.right - P1.rect.left
			dy_top = P1.rect.bottom - self.rect.top
			dy_bottom = self.rect.bottom - P1.rect.top

			# Find smallest overlap (collision side)
			min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

			#hits = False

			# Vertical collisions
			if P1.vel.y > 0 and min_overlap == dy_top:
				P1.rect.bottom = self.rect.top
				#P1.pos.x = P1.rect.left
				P1.pos.y = P1.rect.bottom
				P1.vel.y = 0
				hits = True

			elif P1.vel.y < 0 and min_overlap == dy_bottom:
				P1.rect.top = self.rect.bottom
				#P1.pos.x = P1.rect.left
				P1.pos.y = P1.rect.bottom
				P1.vel.y = 0

			#min_overlap sucks

			# Horizontal collisions
			if direction == 1 and min_overlap == dx_left:
				P1.rect.right = self.rect.left
				P1.pos.x = P1.rect.left
				P1.pos.y = P1.rect.bottom
				#P1.vel.x = 0

			elif direction == 0 and min_overlap == dx_right:
				P1.rect.left = self.rect.right
				P1.pos.x = P1.rect.left
				P1.pos.y = P1.rect.bottom
				#P1.vel.x = 0

			"""

			if P1.vel.y > 0:
				P1.rect.bottom = self.rect.top
				P1.pos.y = P1.rect.bottom
				P1.vel.y = 0
			elif P1.vel.y < 0:
				P1.rect.top = self.rect.bottom
				P1.pos.y = P1.rect.bottom
				P1.vel.y = 0


class PlatformSprite(pygame.sprite.Sprite):
	def __init__(self, image_path, position):
		super().__init__()
		self.surf = pygame.Surface(position)
		self.surf.fill((250,0,0))
		self.rect = self.surf.get_rect(topleft=position)

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(topleft=position)
		self.pos = vec(position)

	def update(self):
		#self.pos.x += offsetX

		#self.rect.midtop = self.pos
		self.rect.midbottom = (self.pos.x+offsetX, self.pos.y)

# making level objects (v2)

# if it helps, try making levels as an array then make it one
with open("levels/level1.json", "r") as level:
	level_content = json.load(level)
	objs = list(level_content.keys())
	#level_array = level_array.split(", ")

#for row_index, row in enumerate(level_array):
#	for col_index, cell in enumerate(row):
#		x, y = col_index * tilesize, row_index * tile_size
#		if cell = "X"

	


for i in range(len(level_content)):
	sprite = level_content[objs[i]]['sprite']
	objtype = level_content[objs[i]]['objtype']
	pos = (64*level_content[objs[i]]['posx'], 64*level_content[objs[i]]['posy'])
	if objtype == "platform":
		objs[i] = Platform(sprite, pos)
	elif objtype == "sprite":
		objs[i] = PlatformSprite(sprite, pos)
	elif objtype == "player":
		print("Player object, avoided")
		#objs[i] = Player(sprite, pos)
		#yes i added this function

platforms = pygame.sprite.Group()
platformSprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
P1 = Player("assets/player.png", (300, 200))
all_sprites.add(P1)

for i in range(len(level_content)):
	objtype = level_content[list(level_content.keys())[i]]['objtype']
	if objtype == "platform":
		platforms.add(objs[i])
	elif objtype == "sprite":
		platformSprites.add(objs[i])
	elif objtype == "player":
		print("Player object, avoided")
		Player.add(objs[i])
		all_sprites.add(objs[i])
	all_sprites.add(objs[i])

	# main loop

while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				P1.jump()

	pygame.display.update()
	FramePerSec.tick(FPS)

	P1.update()
	P1.move()
	platforms.update()
	platformSprites.update()

	if P1.pos.y > HEIGHT:
		P1.pos.y = 0
		P1.vel.y = 0

	displaysurface.fill("#aabbcc") #causes screen tearing
	all_sprites.update()
	all_sprites.draw(displaysurface)
	pygame.display.flip()
