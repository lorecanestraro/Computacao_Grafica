import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

class Planet:
    def __init__(self, name, radius, distance, orbit_speed, rotation_speed, color):
        self.name = name
        self.radius = radius
        self.distance = distance
        self.orbit_speed = orbit_speed
        self.rotation_speed = rotation_speed
        self.color = color
        self.angle = 0
        self.rotation = 0
        self.texture_id = None
        
    def load_texture(self):
        texture_surface = self.create_procedural_texture()
        texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
        width, height = texture_surface.get_size()
        
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        
    def create_procedural_texture(self):
        size = 256
        surface = pygame.Surface((size, size))
        
        if self.name == "Sol":
            for y in range(size):
                for x in range(size):
                    dx = x - size/2
                    dy = y - size/2
                    dist = math.sqrt(dx*dx + dy*dy) / (size/2)
                    noise = math.sin(x * 0.1 + y * 0.05) * 0.3
                    intensity = max(0, 1 - dist + noise)
                    r = max(0, min(255, int(255 * intensity)))
                    g = max(0, min(255, int(200 * intensity)))
                    b = max(0, min(255, int(50 * intensity * 0.5)))
                    surface.set_at((x, y), (r, g, b))
                    
        elif self.name == "Mercúrio":
            for y in range(size):
                for x in range(size):
                    noise = math.sin(x * 0.2) * math.cos(y * 0.2) * 0.2
                    gray = max(0, min(255, int(120 + 40 * noise)))
                    surface.set_at((x, y), (gray, gray, gray))
                    
        elif self.name == "Vênus":
            for y in range(size):
                for x in range(size):
                    noise = math.sin(x * 0.15 + y * 0.1) * 0.3
                    r = max(0, min(255, int(220 + 35 * noise)))
                    g = max(0, min(255, int(180 + 30 * noise)))
                    b = max(0, min(255, int(100 + 20 * noise)))
                    surface.set_at((x, y), (r, g, b))
                    
        elif self.name == "Terra":
            for y in range(size):
                for x in range(size):
                    lat = (y / size) * math.pi
                    lon = (x / size) * 2 * math.pi
                    noise = math.sin(lon * 5) * math.cos(lat * 3) * 0.5
                    if noise > 0.2:
                        r, g, b = 34, 139, 34
                    else:
                        r, g, b = 30, 100, 200
                    surface.set_at((x, y), (r, g, b))
                    
        elif self.name == "Marte":
            for y in range(size):
                for x in range(size):
                    noise = math.sin(x * 0.1) * math.cos(y * 0.15) * 0.3
                    r = max(0, min(255, int(200 + 55 * noise)))
                    g = max(0, min(255, int(80 + 30 * noise)))
                    b = max(0, min(255, int(40 + 20 * noise)))
                    surface.set_at((x, y), (r, g, b))
                    
        elif self.name == "Júpiter":
            for y in range(size):
                for x in range(size):
                    band = math.sin(y * 0.1) * 0.5
                    noise = math.sin(x * 0.3) * 0.2
                    r = max(0, min(255, int(220 + 35 * (band + noise))))
                    g = max(0, min(255, int(170 + 30 * (band + noise))))
                    b = max(0, min(255, int(120 + 20 * (band + noise))))
                    surface.set_at((x, y), (r, g, b))
                    
        elif self.name == "Saturno":
            for y in range(size):
                for x in range(size):
                    band = math.sin(y * 0.08) * 0.3
                    r = max(0, min(255, int(230 + 25 * band)))
                    g = max(0, min(255, int(210 + 20 * band)))
                    b = max(0, min(255, int(160 + 15 * band)))
                    surface.set_at((x, y), (r, g, b))
                    
        elif self.name == "Urano":
            for y in range(size):
                for x in range(size):
                    noise = math.sin(x * 0.1 + y * 0.1) * 0.2
                    r = max(0, min(255, int(100 + 30 * noise)))
                    g = max(0, min(255, int(180 + 40 * noise)))
                    b = max(0, min(255, int(200 + 35 * noise)))
                    surface.set_at((x, y), (r, g, b))
                    
        elif self.name == "Netuno":
            for y in range(size):
                for x in range(size):
                    noise = math.sin(x * 0.12 + y * 0.08) * 0.3
                    r = max(0, min(255, int(50 + 30 * noise)))
                    g = max(0, min(255, int(80 + 40 * noise)))
                    b = max(0, min(255, int(220 + 35 * noise)))
                    surface.set_at((x, y), (r, g, b))
                    
        return surface
        
    def update(self, dt):
        self.angle += self.orbit_speed * dt
        self.rotation += self.rotation_speed * dt
        
    def draw(self, quadric):
        glPushMatrix()
        
        glRotatef(self.angle, 0, 1, 0)
        glTranslatef(self.distance, 0, 0)
        glRotatef(self.rotation, 0, 1, 0)
        
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor3f(1, 1, 1)
        else:
            glColor3fv(self.color)
        
        gluSphere(quadric, self.radius, 32, 32)
        
        if self.texture_id:
            glDisable(GL_TEXTURE_2D)
        
        glPopMatrix()
        
    def draw_orbit(self):
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            angle = 2 * math.pi * i / 100
            x = self.distance * math.cos(angle)
            z = self.distance * math.sin(angle)
            glVertex3f(x, 0, z)
        glEnd()

class Moon:
    def __init__(self, radius, distance, orbit_speed):
        self.radius = radius
        self.distance = distance
        self.orbit_speed = orbit_speed
        self.angle = 0
        self.texture_id = None
        
    def load_texture(self):
        size = 128
        surface = pygame.Surface((size, size))
        
        for y in range(size):
            for x in range(size):
                noise1 = math.sin(x * 0.3) * math.cos(y * 0.3)
                noise2 = math.sin(x * 0.5 + y * 0.2) * 0.5
                gray = max(0, min(255, int(180 + 40 * noise1 + 35 * noise2)))
                surface.set_at((x, y), (gray, gray, gray))
        
        texture_data = pygame.image.tostring(surface, "RGB", 1)
        width, height = surface.get_size()
        
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        
    def update(self, dt):
        self.angle += self.orbit_speed * dt
        
    def draw(self, quadric, planet_distance, planet_angle):
        glPushMatrix()
        
        glRotatef(planet_angle, 0, 1, 0)
        glTranslatef(planet_distance, 0, 0)
        glRotatef(self.angle, 0, 1, 0)
        glTranslatef(self.distance, 0, 0)
        
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor3f(1, 1, 1)
        else:
            glColor3f(0.8, 0.8, 0.8)
            
        gluSphere(quadric, self.radius, 16, 16)
        
        if self.texture_id:
            glDisable(GL_TEXTURE_2D)
        
        glPopMatrix()

class SaturnRings:
    def __init__(self, inner_radius, outer_radius):
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.texture_id = None
        
    def load_texture(self):
        size = 256
        surface = pygame.Surface((size, size))
        
        for y in range(size):
            for x in range(size):
                dx = x - size/2
                dy = y - size/2
                dist = math.sqrt(dx*dx + dy*dy) / (size/2)
                
                if dist > 0.5 and dist < 0.9:
                    band = math.sin(dist * 30) * 0.3
                    r = max(0, min(255, int(200 + 55 * band)))
                    g = max(0, min(255, int(180 + 45 * band)))
                    b = max(0, min(255, int(130 + 30 * band)))
                    a = max(0, min(255, int(180 * (1 - abs(dist - 0.7) * 3))))
                else:
                    r, g, b, a = 0, 0, 0, 0
                    
                surface.set_at((x, y), (r, g, b))
        
        texture_data = pygame.image.tostring(surface, "RGBA", 1)
        width, height = surface.get_size()
        
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        
    def draw(self, planet_distance, planet_angle, planet_rotation):
        glPushMatrix()
        
        glRotatef(planet_angle, 0, 1, 0)
        glTranslatef(planet_distance, 0, 0)
        glRotatef(planet_rotation, 0, 1, 0)
        glRotatef(20, 1, 0, 0)
        
        glColor4f(0.8, 0.7, 0.5, 0.6)
        glBegin(GL_QUAD_STRIP)
        for i in range(101):
            angle = 2 * math.pi * i / 100
            x1 = self.inner_radius * math.cos(angle)
            z1 = self.inner_radius * math.sin(angle)
            x2 = self.outer_radius * math.cos(angle)
            z2 = self.outer_radius * math.sin(angle)
            glVertex3f(x1, 0, z1)
            glVertex3f(x2, 0, z2)
        glEnd()
        
        glPopMatrix()

class SolarSystem:
    def __init__(self):
        pygame.init()
        self.display = (1200, 800)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Sistema Solar 3D")
        
        self.setup_opengl()
        self.setup_lighting()
        
        self.quadric = gluNewQuadric()
        gluQuadricTexture(self.quadric, GL_TRUE)
        gluQuadricNormals(self.quadric, GLU_SMOOTH)
        
        self.sun = Planet("Sol", 2.0, 0, 0, 5, (1, 1, 0))
        
        self.planets = [
            Planet("Mercúrio", 0.3, 4, 47, 10, (0.7, 0.7, 0.7)),
            Planet("Vênus", 0.6, 6, 35, 6, (0.9, 0.7, 0.4)),
            Planet("Terra", 0.65, 8, 30, 100, (0.2, 0.4, 0.8)),
            Planet("Marte", 0.4, 10, 24, 97, (0.8, 0.3, 0.2)),
            Planet("Júpiter", 1.2, 14, 13, 240, (0.8, 0.6, 0.4)),
            Planet("Saturno", 1.0, 18, 9, 220, (0.9, 0.8, 0.6)),
            Planet("Urano", 0.7, 22, 7, 140, (0.4, 0.7, 0.8)),
            Planet("Netuno", 0.7, 26, 5, 150, (0.2, 0.3, 0.8))
        ]
        
        self.moon = Moon(0.15, 1.2, 360)
        self.saturn_rings = SaturnRings(1.3, 2.0)
        
        self.load_all_textures()
        
        self.camera_distance = 35
        self.camera_angle_x = 30
        self.camera_angle_y = 0
        
        self.clock = pygame.time.Clock()
        self.running = True
        
    def load_all_textures(self):
        print("Carregando texturas...")
        self.sun.load_texture()
        for planet in self.planets:
            planet.load_texture()
        self.moon.load_texture()
        self.saturn_rings.load_texture()
        print("Texturas carregadas!")
        
    def setup_opengl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.camera_distance = max(15, self.camera_distance - 2)
                elif event.button == 5:
                    self.camera_distance = min(60, self.camera_distance + 2)
        
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            mouse_rel = pygame.mouse.get_rel()
            self.camera_angle_y += mouse_rel[0] * 0.5
            self.camera_angle_x -= mouse_rel[1] * 0.5
            self.camera_angle_x = max(-89, min(89, self.camera_angle_x))
        else:
            pygame.mouse.get_rel()
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.camera_angle_x -= 2
        if keys[pygame.K_DOWN]:
            self.camera_angle_x += 2
        if keys[pygame.K_LEFT]:
            self.camera_angle_y -= 2
        if keys[pygame.K_RIGHT]:
            self.camera_angle_y += 2
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.camera_distance = max(15, self.camera_distance - 0.5)
        if keys[pygame.K_MINUS]:
            self.camera_distance = min(60, self.camera_distance + 0.5)
            
    def update(self, dt):
        for planet in self.planets:
            planet.update(dt)
        
        self.moon.update(dt)
        self.sun.update(dt)
        
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(0, 0, -self.camera_distance)
        glRotatef(self.camera_angle_x, 1, 0, 0)
        glRotatef(self.camera_angle_y, 0, 1, 0)
        
        glPushMatrix()
        glDisable(GL_LIGHTING)
        
        if self.sun.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.sun.texture_id)
            glColor3f(1, 1, 1)
        else:
            glColor3f(1, 1, 0)
            
        gluSphere(self.quadric, self.sun.radius, 32, 32)
        
        if self.sun.texture_id:
            glDisable(GL_TEXTURE_2D)
            
        glEnable(GL_LIGHTING)
        glPopMatrix()
        
        for planet in self.planets:
            planet.draw_orbit()
        
        for planet in self.planets:
            planet.draw(self.quadric)
        
        earth = self.planets[2]
        self.moon.draw(self.quadric, earth.distance, earth.angle)
        
        saturn = self.planets[5]
        self.saturn_rings.draw(saturn.distance, saturn.angle, saturn.rotation)
        
        pygame.display.flip()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()

if __name__ == "__main__":
    solar_system = SolarSystem()
    print("=== CONTROLES ===")
    print("Mouse: Clique e arraste para rotacionar")
    print("Scroll: Zoom in/out")
    print("Setas: Rotacionar câmera")
    print("+/-: Zoom")
    print("ESC: Sair")
    print("=================")
    solar_system.run()