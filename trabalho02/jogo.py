import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import time

WIDTH, HEIGHT = 1200, 800
FPS = 60


MENU_PLAY = 0
MENU_INSTRUCOES = 1
MENU_SAIR = 2

player_x = 0.0
player_y = 0.0
player_z = 0.0
player_yaw = 0.0      
player_pitch = 0.0    
player_speed = 8.0    
player_score = 0


orbs = []
MAX_ORBS = 14


particles = []


in_menu = True
menu_selected = 0
running = True
game_started = False
game_time = 0.0
spawn_timer = 0.0
spawn_interval = 0.9
difficulty_timer = 0.0
orb_attract_factor = 1.0


CAM_MODE_TP = 0
CAM_MODE_FP = 1
cam_mode = CAM_MODE_TP


tp_distance = 9.0
tp_height = 3.0
cam_angle_x = 20.0
cam_angle_y = 0.0
cam_sensitivity = 0.18

pygame_font = None


quadric = None

def criar_orb():

    r = random.uniform(8.0, 24.0)
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(-0.35, 0.35)
    x = player_x + math.cos(theta) * r
    z = player_z + math.sin(theta) * r
    y = player_y + phi * 6.0
    size = random.uniform(0.25, 0.6)
    return {
        'x': x, 'y': y, 'z': z,
        'size': size,
        'rot': random.uniform(0, 360),
        'rot_speed': random.uniform(20, 90),
        'color': (random.random(), random.random(), random.random()),
        'attract_speed': random.uniform(0.25, 1.0)
    }

def spawn_initial_orbs(n=8):
    orbs.clear()
    for _ in range(n):
        orbs.append(criar_orb())

def add_particles(x, y, z, color, count=20):
   
    for _ in range(count):
        ang = random.uniform(0, 2*math.pi)
        elev = random.uniform(-0.6, 0.6)
        speed = random.uniform(2.0, 6.0)
        vx = math.cos(ang) * math.sqrt(max(0.001,1-elev*elev)) * speed
        vz = math.sin(ang) * math.sqrt(max(0.001,1-elev*elev)) * speed
        vy = elev * speed * 0.8
        particles.append({
            'x': x, 'y': y, 'z': z,
            'vx': vx, 'vy': vy, 'vz': vz,
            'life': 0.0, 'ttl': random.uniform(0.6, 1.5),
            'size': random.uniform(2.0, 5.0),
            'color': color
        })

def reset_game():
    global player_x, player_y, player_z, player_yaw, player_pitch, player_speed, player_score
    global orbs, particles, game_time, spawn_timer, difficulty_timer, orb_attract_factor, game_started
    player_x = 0.0; player_y = 0.0; player_z = 0.0
    player_yaw = 0.0; player_pitch = 0.0
    player_speed = 8.0
    player_score = 0
    orbs = []
    particles = []
    game_time = 0.0
    spawn_timer = 0.0
    difficulty_timer = 0.0
    orb_attract_factor = 1.0
    spawn_initial_orbs(9)
    game_started = True


def render_text(text, x, y, size=20, color=(255,255,255)):
  
    font = pygame.font.SysFont("Arial", size)
    surf = font.render(str(text), True, color)
    data = pygame.image.tostring(surf, "RGBA", True)
    w, h = surf.get_size()
   
    try:
        glWindowPos2i(int(x), int(HEIGHT - y - h))
        glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, data)
    except Exception:
        glRasterPos2f(x, HEIGHT - y)
        glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, data)

def draw_player_cube():
  
    s = 0.9
    glPushMatrix()
    glTranslatef(player_x, player_y, player_z)
    glScalef(0.8, 0.8, 1.2)
    glBegin(GL_QUADS)
   
    glColor3f(0.85, 0.45, 0.65)
    glVertex3f( s,  s, -s)
    glVertex3f(-s,  s, -s)
    glVertex3f(-s, -s, -s)
    glVertex3f( s, -s, -s)
   
    glColor3f(0.3, 0.6, 0.95)
    glVertex3f( s, -s, s)
    glVertex3f(-s, -s, s)
    glVertex3f(-s,  s, s)
    glVertex3f( s,  s, s)
    glEnd()
    glPopMatrix()

def draw_sphere_at(ox, oy, oz, radius, color):
   
    global quadric
    glPushMatrix()
    glTranslatef(ox, oy, oz)
    glColor3f(color[0], color[1], color[2])
  
    gluSphere(quadric, radius, 18, 14)
    glPopMatrix()

def draw_orb(orb):
    glPushMatrix()
    glTranslatef(orb['x'], orb['y'], orb['z'])
    glRotatef(orb['rot'], 0, 1, 0)
    glColor3f(*orb['color'])
    gluSphere(quadric, orb['size'], 18, 14)
    glPopMatrix()

def draw_particles():
    glDisable(GL_LIGHTING)
    glPointSize(3)
    glBegin(GL_POINTS)
    for p in particles:
        t = max(0.0, 1.0 - (p['life'] / p['ttl']))
        glColor4f(p['color'][0]*t, p['color'][1]*t, p['color'][2]*t, t)
        glVertex3f(p['x'], p['y'], p['z'])
    glEnd()
    glEnable(GL_LIGHTING)


def setup_opengl():
    global quadric
    glClearColor(0.02, 0.02, 0.05, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION,  (0.0, 20.0, 10.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,   (0.12, 0.12, 0.14, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,   (0.95, 0.95, 0.9, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR,  (0.8, 0.8, 0.8, 1.0))
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)


def draw_menu_screen(screen, font, selected):
    screen.fill((6, 8, 20))
    title = font.render("COLETA CÓSMICA", True, (255, 220, 90))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 110))
    subtitle = pygame.font.SysFont("Arial", 18).render("Enter para escolher • ESC para sair", True, (200,200,220))
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 150))

    options = ["JOGAR", "INSTRUÇÕES", "SAIR"]
    for i, opt in enumerate(options):
        rect = pygame.Rect(WIDTH//2-240, 240 + i*90, 480, 64)
        color_box = (40, 40, 80) if i != selected else (70, 70, 120)
        pygame.draw.rect(screen, color_box, rect, border_radius=10)
        txt = font.render(opt, True, (255,255,200) if i == selected else (220,220,220))
        screen.blit(txt, (rect.x + rect.width//2 - txt.get_width()//2, rect.y + 12))

    hint = pygame.font.SysFont("Arial", 16).render("WASD mover | Q/E subir-descer | V alterna câmera (FP/TP) | R reiniciar", True, (180,180,200))
    screen.blit(hint, (20, HEIGHT-36))
    pygame.display.flip()


def update_orbs(dt):
    global orbs
    for orb in orbs:
        orb['rot'] += orb['rot_speed'] * dt
        dx = player_x - orb['x']
        dy = player_y - orb['y']
        dz = player_z - orb['z']
        dist = math.sqrt(dx*dx + dy*dy + dz*dz) + 1e-6
        orb['x'] += (dx / dist) * orb['attract_speed'] * orb_attract_factor * dt
        orb['y'] += (dy / dist) * (orb['attract_speed']*0.5) * orb_attract_factor * dt
        orb['z'] += (dz / dist) * orb['attract_speed'] * orb_attract_factor * dt

def update_particles(dt):
    to_remove = []
    for p in particles:
        p['life'] += dt
        p['x'] += p['vx'] * dt
        p['y'] += p['vy'] * dt - 3.0 * dt * 0.5
        p['z'] += p['vz'] * dt
        p['vx'] *= (1.0 - 1.5*dt)
        p['vy'] *= (1.0 - 1.5*dt)
        p['vz'] *= (1.0 - 1.5*dt)
        if p['life'] >= p['ttl']:
            to_remove.append(p)
    for r in to_remove:
        particles.remove(r)

def check_collisions():
    global player_score
    removed = []
    for orb in orbs:
        dx = orb['x'] - player_x
        dy = orb['y'] - player_y
        dz = orb['z'] - player_z
        d = math.sqrt(dx*dx + dy*dy + dz*dz)
        if d < orb['size'] + 1.0:   
        
            player_score += int(10 + orb['size'] * 10)
            add_particles(orb['x'], orb['y'], orb['z'], orb['color'], count=22)
            removed.append(orb)
    for r in removed:
        if r in orbs:
            orbs.remove(r)


def draw_hud():
    render_text(f"Pontos: {player_score}", 18, 18, 20, (255, 220, 90))
    render_text(f"Orbs: {len(orbs)}", 18, 46, 18, (200,200,255))
    render_text(f"Tempo: {int(game_time)}s", WIDTH-220, 18, 18, (200,255,200))
    render_text("V - Troca Câmera (FP/TP)  |  R - Reiniciar  |  ESC - Menu", WIDTH-540, 46, 16, (200,200,200))
    mode_name = "FP" if cam_mode == CAM_MODE_FP else "TP"
    render_text(f"Câmera: {mode_name}", WIDTH-220, 76, 16, (255,215,140))

def main():
    global in_menu, menu_selected, running, player_x, player_y, player_z
    global player_yaw, player_pitch, player_speed, player_score
    global game_time, spawn_timer, spawn_interval, difficulty_timer, orb_attract_factor
    global cam_mode, tp_distance, tp_height, cam_angle_x, cam_angle_y
    global quadric, game_started

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Coleta Cósmica — FP + TP (sem classes)")
    clock = pygame.time.Clock()
    font_menu = pygame.font.SysFont("Arial", 34)

    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, WIDTH / HEIGHT, 0.1, 350.0)
    glMatrixMode(GL_MODELVIEW)
    setup_opengl()

    spawn_initial_orbs(9)
    last_time = time.time()
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    mouse_look_active = False

    while running:
        dt = clock.tick(FPS) / 1000.0
        now = time.time()
        elapsed = now - last_time
        last_time = now

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if in_menu:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_UP:
                        menu_selected = (menu_selected - 1) % 3
                    elif event.key == K_DOWN:
                        menu_selected = (menu_selected + 1) % 3
                    elif event.key == K_RETURN:
                        if menu_selected == MENU_PLAY:
                            reset_game()
                            in_menu = False
                        elif menu_selected == MENU_INSTRUCOES:

                            print("INSTRUÇÕES: WASD mover, Q/E subir-descer, V alterna câmera, mouse arrastar para olhar.")
                        elif menu_selected == MENU_SAIR:
                            running = False
                else:
                    if event.key == K_ESCAPE:
                        in_menu = True
                        game_started = False
                        pygame.event.set_grab(False)
                        pygame.mouse.set_visible(True)
                    elif event.key == K_r:
                        reset_game()
                    elif event.key == K_v:
                        # alterna modo câmera
                        if cam_mode == CAM_MODE_TP:
                            cam_mode = CAM_MODE_FP
                            # ative captura do mouse para FP
                            pygame.event.set_grab(True)
                            pygame.mouse.set_visible(False)
                        else:
                            cam_mode = CAM_MODE_TP
                            pygame.event.set_grab(False)
                            pygame.mouse.set_visible(True)

            elif event.type == MOUSEBUTTONDOWN:
                if not in_menu:
                    if event.button == 1:
                        mouse_look_active = True
                        pygame.mouse.get_rel()  # limpar rel
                    elif event.button == 4:
                        tp_distance = max(3.0, tp_distance - 1.0)
                    elif event.button == 5:
                        tp_distance = min(35.0, tp_distance + 1.0)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_look_active = False
            elif event.type == MOUSEMOTION:
                mx, my = event.rel
                if not in_menu:
                    if cam_mode == CAM_MODE_FP and pygame.event.get_grab():
                        player_yaw += mx * cam_sensitivity
                        player_pitch -= my * cam_sensitivity
                        player_pitch = max(-89.0, min(89.0, player_pitch))
                    elif cam_mode == CAM_MODE_TP and pygame.mouse.get_pressed()[0]:
                        cam_angle_y += mx * cam_sensitivity
                        cam_angle_x += my * cam_sensitivity
                        cam_angle_x = max(-80, min(80, cam_angle_x))

 
        if in_menu:
            draw_menu_screen(screen, font_menu, menu_selected)
            continue

  
        keys = pygame.key.get_pressed()
        move_x = 0.0; move_y = 0.0; move_z = 0.0
        if keys[K_w]: move_z -= 1.0
        if keys[K_s]: move_z += 1.0
        if keys[K_a]: move_x -= 1.0
        if keys[K_d]: move_x += 1.0
        if keys[K_q]: move_y -= 1.0
        if keys[K_e]: move_y += 1.0

        if cam_mode == CAM_MODE_FP:

            rad = math.radians(player_yaw)
            forward_x = -math.sin(rad)
            forward_z = -math.cos(rad)
            right_x = math.cos(rad)
            right_z = -math.sin(rad)
            dir_x = forward_x * move_z + right_x * move_x
            dir_z = forward_z * move_z + right_z * move_x
        else:
        
            dir_x = move_x
            dir_z = move_z

        mag = math.sqrt(dir_x*dir_x + move_y*move_y + dir_z*dir_z)
        if mag > 0.0001:
            nx = dir_x / mag; ny = move_y / mag; nz = dir_z / mag
            speed = player_speed * (1.0 + 0.02 * player_score)
            player_x += nx * speed * dt
            player_y += ny * speed * dt
            player_z += nz * speed * dt

  
        player_y = max(-6.0, min(12.0, player_y))

   
        spawn_timer += dt
        difficulty_timer += dt
        if spawn_timer >= spawn_interval:
            orbs.append(criar_orb())
            spawn_timer = 0.0
            while len(orbs) > MAX_ORBS:
                orbs.pop(0)
        if difficulty_timer > 10.0:
            orb_attract_factor = 1.0 + difficulty_timer / 40.0
            difficulty_timer = difficulty_timer % 10.0

        update_orbs(dt)
        update_particles(dt)
        check_collisions()

        game_time += dt

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        if cam_mode == CAM_MODE_FP:
           
            glRotatef(-player_pitch, 1, 0, 0)
            glRotatef(-player_yaw, 0, 1, 0)
            glTranslatef(-player_x, -player_y - 0.4, -player_z)
        else:
         
            yaw_rad = math.radians(player_yaw + cam_angle_y)
            pitch_rad = math.radians(cam_angle_x)
           
            cx = player_x + math.sin(yaw_rad) * tp_distance * math.cos(pitch_rad)
            cz = player_z + math.cos(yaw_rad) * tp_distance * math.cos(pitch_rad)
            cy = player_y + tp_height + math.sin(pitch_rad) * tp_distance
      
            gluLookAt(cx, cy, cz, player_x, player_y + 0.4, player_z, 0, 1, 0)

     
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 0.95, 0.6)
        glTranslatef(player_x + 18, player_y + 12, player_z + 18)
  
        gluSphere(quadric, 1.0, 8, 6)
        glEnable(GL_LIGHTING)
        glPopMatrix()


        glPushMatrix()
        glColor4f(0.15, 0.18, 0.23, 1.0)
        glBegin(GL_LINES)
        grid = 28
        step = 1.0
        for i in range(-grid, grid+1):
            glVertex3f(i*step, -4.5, -grid*step)
            glVertex3f(i*step, -4.5, grid*step)
            glVertex3f(-grid*step, -4.5, i*step)
            glVertex3f(grid*step, -4.5, i*step)
        glEnd()
        glPopMatrix()


        for orb in orbs:
            draw_orb(orb)

        if cam_mode == CAM_MODE_TP:
            draw_player_cube()
        else:
            glPushMatrix()
        
            rad = math.radians(player_yaw)
            fx = player_x - math.sin(rad) * 1.0
            fz = player_z - math.cos(rad) * 1.0
            fy = player_y + 0.0
            glTranslatef(fx, fy, fz)
            glScalef(0.4, 0.4, 1.2)
            glColor3f(0.7,0.4,0.6)
            glBegin(GL_QUADS)
            glVertex3f( 0.3, 0.3,-0.3)
            glVertex3f(-0.3, 0.3,-0.3)
            glVertex3f(-0.3,-0.3,-0.3)
            glVertex3f( 0.3,-0.3,-0.3)
            glEnd()
            glPopMatrix()

      
        draw_particles()

       
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WIDTH, 0, HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        draw_hud()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
