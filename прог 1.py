import random
import tkinter as tk

WIDTH, HEIGHT = 800, 600
FPS_MS = 16                    
BACKGROUND = "#000000"

FADE_COLORS = [
    "#ffffff", "#fff7c0", "#ffe566", "#ffb347",
    "#ff7a2f", "#e8491d", "#8a2b12", "#3a1a0c",
]

class Particle:

    def __init__(self, x, y):
        self.x = x + random.uniform(-6, 6)
        self.y = y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-4.2, -1.8)
        self.max_life = random.randint(40, 90) 
        self.life = self.max_life
        self.radius = random.uniform(2.0, 6.0)

    def step(self):
        self.x += self.vx + random.uniform(-0.4, 0.4)
        self.y += self.vy
        self.vy *= 0.985           
        self.vx *= 0.99
        self.radius *= 0.995
        self.life -= 1

    @property
    def alive(self):
        return self.life > 0

    @property
    def color(self):
        frac = self.life / self.max_life
        idx = min(int(frac * len(FADE_COLORS)), len(FADE_COLORS) - 1)
        return FADE_COLORS[idx]

    def draw(self, canvas):
        r = max(self.radius, 0.5)
        canvas.create_oval(self.x - r, self.y - r,
                           self.x + r, self.y + r,
                           fill=self.color, outline="")

class Emitter:

    def __init__(self, x, y, rate=3):
        self.x, self.y = x, y
        self.rate = rate
        self.particles = []

    def step(self, canvas):
        for _ in range(self.rate):
            self.particles.append(Particle(self.x, self.y))
        alive = []
        for p in self.particles:
            p.step()
            if p.alive:
                p.draw(canvas)
                alive.append(p)
        self.particles = alive

    def draw_base(self, canvas):
        canvas.create_oval(self.x - 8, self.y - 8,
                           self.x + 8, self.y + 8,
                           fill="#ffdd88", outline="")

class App:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=BACKGROUND, highlightthickness=0)
        self.canvas.pack()
        self.emitters = [Emitter(WIDTH // 2, HEIGHT - 60)]

        self.canvas.bind("<Button-1>", self.add_emitter)
        self.canvas.bind("<Button-3>", self.remove_emitter)
        self.canvas.bind("<Button-2>", self.remove_emitter)

        self.loop()

    def add_emitter(self, event):
        self.emitters.append(Emitter(event.x, event.y))

    def remove_emitter(self, event):
        if len(self.emitters) > 1:
            nearest = min(self.emitters,
                          key=lambda e: (e.x - event.x) ** 2 + (e.y - event.y) ** 2)
            self.emitters.remove(nearest)

    def loop(self):
        self.canvas.delete("all")
        for e in self.emitters:
            e.draw_base(self.canvas)
            e.step(self.canvas)
        self.canvas.after(FPS_MS, self.loop)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Система частиц")
    App(root)
    root.mainloop()