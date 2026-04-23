import pygame
from pygame.locals import *
import sys, json
# import antigravity

# to do list:
# load levels somehow
# vertical camera movement

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 480
WIDTH = 640
# ACC = 0.2
FRIC = -0.12
FPS = 60
global jumps
jumps = 2 # this is going to be horrible later on
global offsetX
offsetX = 0
global offsetY
offsetY = 0
move = 3
gravity = 6
global camerabounds
camerabounds = 300

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
pygame.display.set_caption("Platformer Test")

class Player(pygame.sprite.Sprite):
	def __init__(self, image_path, position):
		super().__init__()
		self.surf = pygame.Surface((50, 50))
		self.surf.fill((128,255,40))
		self.rect = self.surf.get_rect()

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(topleft=position)
	
		self.pos = vec((10, 385))
		self.vel = vec(0,0)
		self.acc = vec(0,0)

	def move(self):
		global move
		global offsetX
		global camerabounds

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
			if pressed_keys[K_RIGHT]:
				self.pos.x += move
		else: 
			if pressed_keys[K_LEFT]:
				# self.acc.x = 0
				# self.acc.x = -ACC
				offsetX += move
				self.pos.x -= move
			if pressed_keys[K_RIGHT]:
				offsetX -= move
				self.pos.x += move




		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		if self.pos.x > WIDTH-camerabounds:
			self.pos.x = WIDTH-camerabounds
		if self.pos.x < camerabounds:
			self.pos.x = camerabounds

		self.rect.midbottom = self.pos
		
	
	def update(self):
		hits = pygame.sprite.spritecollide(self, platforms, False)
		if P1.vel.y > 0:
			if hits:
				self.pos.y = hits[0].rect.top + 1
				self.vel.y = 0

	def jump(self):
		global jumps
		global gravity

		hits = pygame.sprite.spritecollide(self, platforms, False)
		if hits:
			jumps = 2
		if jumps > 0:
			if jumps == 2:
				self.vel.y = -(gravity*1.5)
			elif jumps == 1:
				self.vel.y = -gravity
			jumps -= 1

class Platform(pygame.sprite.Sprite):
	def __init__(self, image_path, position):
		super().__init__()
		self.surf = pygame.Surface((WIDTH, 20))
		self.surf.fill((250,0,0))
		self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(topleft=position)
		self.pos = vec(position)

	def update(self):
		self.pos.x = offsetX

		self.rect.midbottom = self.pos

class PlatformSprite(pygame.sprite.Sprite):
	def __init__(self, image_path, position):
		super().__init__()
		self.surf = pygame.Surface((WIDTH, 20))
		self.surf.fill((250,0,0))
		self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(topleft=position)
		self.pos = vec(position)

	def update(self):
		self.pos.x = offsetX

		self.rect.midtop = self.pos

P1 = Player("assets/player.png", (200, 100))

# making level objects

with open("levels/level1.json", "r") as level:
	level_content = json.load(level)
	level_objs = list(level_content.keys())

for i in range(len(level_content)):
	level_sprite = level_content[level_objs[i]]['sprite']
	level_objtype = level_content[level_objs[i]]['objtype']
	level_pos = (level_content[level_objs[i]]['posx'], level_content[level_objs[i]]['posy'])
	if level_objtype == "platform":
		level_objs[i] = Platform(level_sprite, level_pos)
	elif level_objtype == "sprite":
		level_objs[i] = PlatformSprite(level_sprite, level_pos)

	print(level_pos)

# these MUST stay after the sprite definitions to avoid bugs
platforms = pygame.sprite.Group()
platformSprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

for i in range(len(level_content)):
	objtype = level_content[list(level_content.keys())[i]]['objtype']
	if objtype == "platform":
		platforms.add(level_objs[i])
		all_sprites.add(level_objs[i])
	elif objtype == "sprite":
		platformSprites.add(level_objs[i])
		all_sprites.add(level_objs[i])
	print(level_objs[i].pos)

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

	if P1.pos.y > HEIGHT:
		P1.pos.y = 0

	displaysurface.fill("#aabbcc")
	all_sprites.update()
	all_sprites.draw(displaysurface)
	pygame.display.flip()
