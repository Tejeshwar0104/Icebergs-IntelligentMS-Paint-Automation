import pyautogui
import pygetwindow as gw
import time
import math
import os
import logging
import subprocess

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Safety: small pause so you can abort with mouse move if needed
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True  # move mouse to top-left to abort

# ---------- Window focus helpers ----------
def open_or_focus_paint(timeout=12.0):
    """Ensure MS Paint is open and active."""
    # MS Store Paint has different window titles
    titles = ['Paint', 'Untitled - Paint', 'mspaint', 'Paint - Untitled']
    win = None

    # Step 1: Try to find an existing Paint window
    for t in titles:
        wins = gw.getWindowsWithTitle(t)
        if wins:
            win = wins[0]
            logging.info(f"Found existing Paint window: {win.title}")
            break

    # Step 2: If not found, launch MS Paint (MS Store version)
    if not win:
        logging.info("Launching MS Paint (MS Store version)...")
        try:
            # Method 1: Use shell:AppsFolder protocol (most reliable for MS Store apps)
            subprocess.Popen(['explorer.exe', 'shell:AppsFolder\\Microsoft.Paint_8wekyb3d8bbwe!Microsoft.Paint'])
            logging.info("Launch command sent, waiting for window...")
        except Exception as e:
            logging.error(f"Failed to launch Paint via shell protocol: {e}")
            # Method 2: Fallback - try using start command
            try:
                subprocess.Popen(['cmd', '/c', 'start', 'ms-paint:'], shell=True)
                logging.info("Trying alternative launch method...")
            except Exception as e2:
                logging.error(f"Fallback launch also failed: {e2}")
                return False

        # Wait until Paint window appears (MS Store apps take longer to start)
        start = time.time()
        while time.time() - start < timeout:
            for t in titles:
                wins = gw.getWindowsWithTitle(t)
                if wins:
                    win = wins[0]
                    logging.info(f"Paint window appeared: {win.title}")
                    break
            if win:
                break
            time.sleep(0.8)  # Longer sleep for MS Store apps

        if not win:
            logging.error("Could not find MS Paint window after launch.")
            logging.info("Please open Paint manually and try again.")
            return False

    # Step 3: Bring the window to the front safely
    try:
        if win.isMinimized:
            win.restore()
            time.sleep(0.5)
        win.activate()
        time.sleep(1.0)  # Longer wait for MS Store apps
        if not win.isActive:
            raise Exception("Window did not activate properly.")
    except Exception as e:
        logging.warning(f"Window activate() failed: {e}, trying Alt+Tab fallback.")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1.0)

    # Step 4: Maximize window for consistent coordinates
    try:
        if not win.isMaximized:
            win.maximize()
            time.sleep(0.5)
    except:
        pass

    # Step 5: Click inside Paint to ensure focus
    try:
        # Click in the center-right area (canvas area)
        cx = win.left + int(win.width * 0.6)
        cy = win.top + int(win.height * 0.5)
        pyautogui.click(cx, cy)
        time.sleep(0.3)
    except Exception as e:
        logging.warning(f"Click focus failed: {e}")

    logging.info(f"Paint window ready: {win.title}")
    return True

# ---------- Low-level helpers ----------
def move_and_drag(x0, y0, dx, dy, duration=0.5):
    pyautogui.moveTo(x0, y0)
    pyautogui.dragRel(dx, dy, duration)

def draw_rect(x, y, w, h, duration=0.6):
    pyautogui.moveTo(x, y)
    pyautogui.dragRel(w, 0, duration)
    pyautogui.dragRel(0, h, duration)
    pyautogui.dragRel(-w, 0, duration)
    pyautogui.dragRel(0, -h, duration)

def draw_filled_ellipse(center_x, center_y, rx, ry, steps=36):
    # approximate ellipse with short lines
    px = center_x + rx
    pyautogui.moveTo(px, center_y)
    for i in range(steps):
        theta = 2 * math.pi * (i+1) / steps
        nx = center_x + int(rx * math.cos(theta))
        ny = center_y + int(ry * math.sin(theta))
        pyautogui.dragTo(nx, ny, 0.02, button='left')

# ---------- Professional drawing modules ----------
def draw_modern_house(x=350, y=420, width=340, height=220):
    """Clean architectural-style house. Returns (x,y,w,h)."""
    logging.info(f"Drawing house at ({x},{y}) size ({width}x{height})")
    # Walls (outline)
    draw_rect(x, y, width, height, duration=0.4)

    # Roof - straight clean triangle
    roof_h = int(height * 0.5)
    pyautogui.moveTo(x, y)
    pyautogui.dragRel(width//2, -roof_h, 0.35)
    pyautogui.dragRel(width//2, roof_h, 0.35)

    # Door - centered, with frame (two-line style)
    door_w = width // 6
    door_h = int(height * 0.55)
    door_x = x + width//2 - door_w//2
    door_y = y + height
    # door frame
    draw_rect(door_x, door_y - door_h, door_w, door_h, duration=0.25)
    # small handle as a short line
    pyautogui.moveTo(door_x + door_w - 10, door_y - door_h//2)
    pyautogui.dragRel(6, 0, 0.08)

    # Two windows (clean rectangles with mullion)
    win_w = width // 6
    win_h = int(height * 0.28)
    win_y = y + int(height * 0.18)
    left_x = x + width // 8
    right_x = x + width - width//8 - win_w
    for wx in (left_x, right_x):
        draw_rect(wx, win_y, win_w, win_h, duration=0.18)
        # mullion: vertical and horizontal center lines
        pyautogui.moveTo(wx + win_w//2, win_y)
        pyautogui.dragRel(0, win_h, 0.08)
        pyautogui.moveTo(wx, win_y + win_h//2)
        pyautogui.dragRel(win_w, 0, 0.08)

    # Return house bounding info
    return (x, y, width, height)


def draw_tree_near_house(house_x, house_y, house_w, house_h, side='right'):
    logging.info("Drawing tree near house")
    trunk_w = 24
    trunk_h = int(house_h * 0.45)
    # choose coordinates relative to house
    if side == 'right':
        tx = house_x + house_w + 100
    else:
        tx = house_x - 60 - trunk_w
    ty = house_y + house_h
    # trunk
    draw_rect(tx, ty - trunk_h, trunk_w, trunk_h, duration=0.12)
    # foliage - layered ellipses (professional clustered canopy)
    cx = tx + trunk_w//2
    cy = ty - trunk_h - 30
    draw_filled_ellipse(cx, cy, 60, 40)
    draw_filled_ellipse(cx - 30, cy + 10, 45, 30)
    draw_filled_ellipse(cx + 30, cy + 10, 45, 30)


def draw_sun(x, y, radius=44):
    logging.info("Drawing sun")
    # circle - approximate by many tiny lines
    steps = 36
    pyautogui.moveTo(x + radius, y)
    for i in range(steps):
        theta = 2 * math.pi * (i+1) / steps
        nx = x + int(radius * math.cos(theta))
        ny = y + int(radius * math.sin(theta))
        pyautogui.dragTo(nx, ny, 0.02)
    # rays - evenly spaced short lines
    for i in range(12):
        theta = 2 * math.pi * i / 12
        sx = x + int((radius+6) * math.cos(theta))
        sy = y + int((radius+6) * math.sin(theta))
        ex = x + int((radius+26) * math.cos(theta))
        ey = y + int((radius+26) * math.sin(theta))
        pyautogui.moveTo(sx, sy)
        pyautogui.dragTo(ex, ey, 0.06)

def draw_person_front(house_x, house_y, house_w, house_h):
    logging.info("Drawing person")
    # place near front center
    px = house_x + house_w//2 + 20
    py = house_y + house_h + 40
    head_r = 10
    # head (circle approximation)
    draw_filled_ellipse(px, py - 10, head_r, head_r)
    # body line
    pyautogui.moveTo(px, py + head_r - 6)
    pyautogui.dragRel(0, 40, 0.15)
    # arms
    pyautogui.moveTo(px - 18, py + 18)
    pyautogui.dragRel(36, 0, 0.12)
    # legs
    pyautogui.moveTo(px, py + 40)
    pyautogui.dragRel(-12, 28, 0.12)
    pyautogui.moveTo(px, py + 40)
    pyautogui.dragRel(12, 28, 0.12)


# Stub functions for car and grass (referenced but not defined in original)
def draw_car_front_left(house_x, house_y, house_w, house_h):
    logging.info("Drawing car (stub - implement as needed)")
    # Simple car placeholder
    cx = house_x - 150
    cy = house_y + house_h - 80
    draw_rect(cx, cy, 120, 60, duration=0.3)
    # wheels
    draw_filled_ellipse(cx + 25, cy + 60, 15, 15)
    draw_filled_ellipse(cx + 95, cy + 60, 15, 15)

def draw_grass_strip(house_x, house_y, house_w, house_h, count=12):
    logging.info("Drawing grass strip")
    base_y = house_y + house_h + 5
    for i in range(count):
        gx = house_x - 50 + (i * 40)
        pyautogui.moveTo(gx, base_y)
        pyautogui.dragRel(0, 20, 0.05)
        pyautogui.moveTo(gx - 5, base_y + 10)
        pyautogui.dragRel(10, 0, 0.05)


# ---------- Command interpreter ----------
last_house = None

def process_command(prompt_text: str):
    """Interprets the prompt and executes the appropriate draw function.
       Returns a status string for logging / UI."""
    prompt = prompt_text.lower().strip()
    logging.info(f"Received command: {prompt}")

    ok = open_or_focus_paint()
    if not ok:
        return "ERROR: Could not open/focus MS Paint."

    global last_house

    # high-level "draw scene" command
    if 'draw scene' in prompt or 'draw full scene' in prompt:
        # draw house then other elements relative to it
        last_house = draw_modern_house()
        time.sleep(0.3)
        hx, hy, hw, hh = last_house
        draw_tree_near_house(hx, hy, hw, hh, side='right')
        time.sleep(0.2)
        draw_person_front(hx, hy, hw, hh)
        time.sleep(0.2)
        draw_sun(hx + hw + 160, hy - 80)
        return "OK: Full professional scene drawn."

    # single operations
    if 'house' in prompt:
        last_house = draw_modern_house()
        return "OK: House drawn."

    if 'tree' in prompt:
        if last_house:
            hx, hy, hw, hh = last_house
            draw_tree_near_house(hx, hy, hw, hh, side='right')
            return "OK: Tree drawn to the right of last house."
        else:
            # fallback position (center-right)
            draw_tree_near_house(600, 300, 1, 1, side='right')
            return "OK: Tree drawn (no house found earlier)."

    if 'car' in prompt:
        if last_house:
            hx, hy, hw, hh = last_house
            draw_car_front_left(hx, hy, hw, hh)
            return "OK: Car drawn front-left of last house."
        else:
            draw_car_front_left(450, 400, 1, 1)
            return "OK: Car drawn (no house found earlier)."

    if 'person' in prompt or 'man' in prompt or 'woman' in prompt:
        if last_house:
            hx, hy, hw, hh = last_house
            draw_person_front(hx, hy, hw, hh)
            return "OK: Person drawn near last house."
        else:
            draw_person_front(450, 400, 1, 1)
            return "OK: Person drawn (no house found earlier)."

    if 'sun' in prompt:
        # relative top-right if house present else fixed
        if last_house:
            hx, hy, hw, hh = last_house
            draw_sun(hx + hw + 160, hy - 80)
        else:
            draw_sun(1000, 120)
        return "OK: Sun drawn."

    if 'grass' in prompt or 'grasses' in prompt:
        if last_house:
            hx, hy, hw, hh = last_house
            draw_grass_strip(hx, hy, hw, hh, count=12)
        else:
            draw_grass_strip(300, 400, 1, 1, count=12)
        return "OK: Grass drawn."

    if 'clear' in prompt or 'reset' in prompt:
        # Ctrl+A then Delete - careful (affects Paint)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.05)
        pyautogui.press('delete')
        last_house = None
        return "OK: Canvas cleared."

    return "Unknown command. Use keywords: house / tree / car / person / sun / grass / draw scene / clear."