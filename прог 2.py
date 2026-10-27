import pygame
import math
import sys

SCREEN_SIZE = 800
ROWS = 7
COLS = 7
PADDING = 10
CELL_SIZE = (SCREEN_SIZE - PADDING * 2) // ROWS

COLOR_BG = (18, 18, 24)       
COLOR_GRID = (40, 40, 50)     
COLOR_DOTS = (255, 100, 100)  
COLOR_LINE = (100, 255, 100)  
COLOR_CURVE = (0, 220, 255)   

class CircleTracker:
    def __init__(self, cx, cy, radius, speed, is_horizontal=True):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.speed = speed
        self.is_horizontal = is_horizontal
        self.angle = 0.0
        self.current_pos = (0, 0)

    def update(self, dt, phase_shift=0.0):
        self.angle += self.speed * dt
       
        angle_with_phase = self.angle + (phase_shift if self.is_horizontal else 0)
        x = self.cx + self.radius * math.cos(angle_with_phase)
        y = self.cy + self.radius * math.sin(angle_with_phase)
        self.current_pos = (x, y)

    def draw(self, surface):
        pygame.draw.circle(surface, COLOR_GRID, (self.cx, self.cy), self.radius, 1)
        pygame.draw.circle(surface, COLOR_DOTS, (int(self.current_pos[0]), int(self.current_pos[1])), 4)

class LissajousCell:
    def __init__(self, r_tracker, c_tracker):
        self.r_tracker = r_tracker  
        self.c_tracker = c_tracker  
        self.points = []            

    def update(self):
        x = self.c_tracker.current_pos[0]
        y = self.r_tracker.current_pos[1]
       
        self.points.append((x, y))
        if len(self.points) > 300: 
            self.points.pop(0)

    def clear(self):
        self.points.clear()

    def draw(self, surface):
        if len(self.points) > 1:
            pygame.draw.lines(surface, COLOR_CURVE, False, self.points, 2)

class LissajousMatrix:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Лабораторная №2: Таблица Фигур Лиссажу")
        self.clock = pygame.time.Clock()
       
        self.radius = (CELL_SIZE - 16) // 2
        self.phase = 0.0  

        self.row_trackers = []
        self.col_trackers = []
        self.matrix = []

        self._build_matrix()

    def _build_matrix(self):
        for r in range(1, ROWS):
            cx = PADDING + CELL_SIZE // 2
            cy = PADDING + r * CELL_SIZE + CELL_SIZE // 2
            self.row_trackers.append(CircleTracker(cx, cy, self.radius, speed=r * 1.5, is_horizontal=False))

        for c in range(1, COLS):
            cx = PADDING + c * CELL_SIZE + CELL_SIZE // 2
            cy = PADDING + CELL_SIZE // 2
            self.col_trackers.append(CircleTracker(cx, cy, self.radius, speed=c * 1.5, is_horizontal=True))

        for r_tracker in self.row_trackers:
            row_cells = []
            for c_tracker in self.col_trackers:
                row_cells.append(LissajousCell(r_tracker, c_tracker))
            self.matrix.append(row_cells)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0  
            self.phase += dt * 0.5             

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for row in self.matrix:
                            for cell in row:
                                cell.clear()

            for tracker in self.row_trackers:
                tracker.update(dt, phase_shift=0.0)
            for tracker in self.col_trackers:
                tracker.update(dt, phase_shift=self.phase) 

            for row in self.matrix:
                for cell in row:
                    cell.update()

            self.screen.fill(COLOR_BG)

            for tracker in self.row_trackers:
                tracker.draw(self.screen)
            for tracker in self.col_trackers:
                tracker.draw(self.screen)

            for r_tr in self.row_trackers:
                pygame.draw.line(self.screen, COLOR_LINE, (0, r_tr.current_pos[1]), (SCREEN_SIZE, r_tr.current_pos[1]), 1)
            for c_tr in self.col_trackers:
                pygame.draw.line(self.screen, COLOR_LINE, (c_tr.current_pos[0], 0), (c_tr.current_pos[0], SCREEN_SIZE), 1)

            for row in self.matrix:
                for cell in row:
                    cell.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = LissajousMatrix()
    app.run()