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
gravity = 0.001
global camerabounds
camerabounds = 300
global direction
direction = 1
# 0 = left
# 1 = right
global hits
hits = False

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
		self.surf = pygame.Surface((32,32))
		#self.surf.fill((128,255,40))
		self.rect = self.surf.get_rect()

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(topleft=position)
	
		self.pos = vec(position)
		self.vel = vec(0,0)

	def move(self):
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
		if hits or self.vel.y == 0:
			jumps = 2
		if jumps > 0:
			if jumps == 2:
				self.vel.y = -(gravity*1.5)
				jumps = 1
			elif jumps == 1:
				self.vel.y = -gravity
				jumps = 0

class Platform(pygame.sprite.Sprite):
	def __init__(self, image_path, position):
		super().__init__()
		self.surf = pygame.Surface(position)
		self.surf.fill((250,0,0))
		self.rect = self.surf.get_rect(topleft=position)

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(topleft=position)
		self.pos = vec(position)

	def update(self):
		global move
		global hits
		global saved_x
		global saved_y
		saved_x = P1.pos.x
		saved_y = P1.pos.y
		#self.pos.x += offsetX

		hits = self.rect.colliderect(P1.rect)

		#self.rect.midbottom = self.pos
		self.rect.midbottom = (self.pos.x + offsetX, self.pos.y)

		if self.rect.colliderect(P1.rect):

			# Calculate overlap distances
			dx_left = P1.rect.right - self.rect.left
			dx_right = self.rect.right - P1.rect.left
			dy_top = P1.rect.bottom - self.rect.top
			dy_bottom = self.rect.bottom - P1.rect.top

			# Find smallest overlap (collision side)
			min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

			# Horizontal collisions
			if min_overlap == dx_left:
				P1.rect.right = self.rect.left
				P1.pos.x = P1.rect.right

			elif min_overlap == dx_right:
				P1.rect.left = self.rect.right
				P1.pos.x = P1.rect.left

			# Vertical collisions
			elif min_overlap == dy_top:
				P1.rect.bottom = self.rect.top
				P1.pos.y = P1.rect.bottom
				P1.vel.y = 0

			elif min_overlap == dy_bottom:
				P1.rect.top = self.rect.bottom
				P1.pos.y = P1.rect.top
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

P1 = Player("assets/player.png", (300, 200))

# making level objects

with open("levels/level1.json", "r") as level:
	level_content = json.load(level)
	objs = list(level_content.keys())

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
		
platforms = pygame.sprite.Group()
platformSprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
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

	P1.move()
	P1.update()
	platforms.update()
	platformSprites.update()

	if P1.pos.y > HEIGHT:
		P1.pos.y = 0
		P1.vel.y = 0

	displaysurface.fill("#aabbcc") #causes screen tearing
	all_sprites.update()
	all_sprites.draw(displaysurface)
	pygame.display.flip()
