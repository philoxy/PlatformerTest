import pygame
from pygame.locals import *
import sys
# import antigravity

# to make a side scroller just add a variable which offsets how the platforms are displayed on their x and y
# then display the platforms with that variables added to the x and y
# maybe make each level place the platforms themselves rather than making it built into the main
# like, make it run python code (somehow??)
# to make camera movement make another update function for the platforms dflksafj

# ok, what if instead of the player moving the platforms moved
# ill do it later cuz im lazy


pygame.init()
vec = pygame.math.Vector2

HEIGHT = 480
WIDTH = 640
ACC = 0.2 # acceleration
FRIC = -0.12 # friction
FPS = 60
global jumps
jumps = 2 # this is going to be horrible later on
global offsetX
offsetX = 0
global offsetY
offsetY = 0
move = 3
gravity = 6


FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
pygame.display.set_caption("Platformer Test")

# displaysurface.blit(imagey, (self.pos.x, self.pos.y))
# pygame.display.flip()

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

		self.acc = vec(0,0.3)

		pressed_keys = pygame.key.get_pressed()

		if pressed_keys[K_LSHIFT]:
			# ACC2 = 2*ACC
			move = 5
		else:
			# ACC2 = ACC
			move = 3

		if pressed_keys[K_LEFT]:
			# self.acc.x = 0
			# self.acc.x = -ACC
			# self.pos.x -= move
			offsetX -= move

		if pressed_keys[K_RIGHT]:
			# self.acc.x = 0
			# self.acc.x = -ACC
			# self.pos.x += move
			offsetX += move

		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		if self.pos.x > WIDTH-15:
			self.pos.x = WIDTH-15
		if self.pos.x < 15:
			self.pos.x = 15

		self.rect.midbottom = self.pos
		
	
	def update(self):
		hits = pygame.sprite.spritecollide(P1 , platforms, False)
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

class platforms(pygame.sprite.Sprite):
	def __init__(self, image_path, position):
		super().__init__()
		self.surf = pygame.Surface((WIDTH, 20))
		self.surf.fill((250,0,0))
		self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(topleft=position)
		self.pos = vec((10, 385))

	def update(self):
		self.pos.x = offsetX

		self.rect.midbottom = self.pos

class platformsprite(pygame.sprite.Sprite):
	def __init__(self, image_path, position):
		super().__init__()
		self.surf = pygame.Surface((WIDTH, 20))
		self.surf.fill((250,0,0))
		self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(topleft=position)
		self.pos = vec((10, 385))

	def update(self):
		self.pos.x = offsetX

		self.rect.midtop = self.pos

P1 = Player("assets/player.png", (30, 30))
PT1 = platforms("assets/platform-collision.png", ((0+offsetX), 400))
PT2 = platforms("assets/platform-collision.png", ((64+offsetX), 350))
PT1S = platformsprite("assets/platform.png", ((0+offsetX), 400))
PT2S = platformsprite("assets/platform.png", ((64+offsetX), 350))

platforms = pygame.sprite.Group()
platforms.add(PT1)
platforms.add(PT2)
platformsprite.add(PT1S)
platformsprite.add(PT2S)

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(PT2)
all_sprites.add(P1)
all_sprites.add(PT1S)
all_sprites.add(PT2S)

while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				P1.jump()

	# for entity in all_sprites:
	# 	displaysurface.blit(entity.surf, entity.rect)

	#offsetX = WIDTH-P1.pos.x
	#offsetY = HEIGHT-P1.pos.y

	pygame.display.update()
	FramePerSec.tick(FPS)

	P1.move()
	P1.update()
	platforms.update()
	print(offsetX)

	if P1.pos.y > HEIGHT:
		P1.pos.y = 0

	displaysurface.fill("#000000")
	all_sprites.update()
	all_sprites.draw(displaysurface)
	pygame.display.flip()
