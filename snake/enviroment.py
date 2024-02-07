import gym, numpy as np, pygame, random, cv2
from gym import Env, spaces

class SnakeEnv(Env):
    window_width, window_height = 640, 480
    black = (0, 0, 0)
    white = (255, 255, 255)
    fps = 30

    def __init__(self): #actions observation
        self.clock = pygame.time.Clock()
        self.state = None
        pygame.init()
        self.window_width, window_height = 640, 480
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Snake Game')
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.window_width, self.window_height, 1), dtype=np.float16)

    def step(self, action): #perform action
        if action == 0:
            self.snake.move_up()
        elif action == 1:
            self.snake.move_down()
        elif action == 2:
            self.snake.move_left()
        elif action == 3:
            self.snake.move_right()
        if not self.snake.update() or self.snake.check_collision():
            reward = -1
            done = True
        elif self.snake.x_pos == self.food.x and self.snake.y_pos == self.food.y:
            self.food.generate()
            self.snake.length += 1
            reward = 1
            done = False
        #elif
        else:
            reward = 0
            done = False
        state = self._get_state()
        info = {}

        return state, reward, done, info
    
    def _get_state(self):
        frame = pygame.surfarray.array3d(pygame.display.get_surface())
        frame = frame[:,:,::-1]
        state = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return state

    def reset(self): #initiats
        self.snake = self.Snake(20)
        self.food = self.Food(20)
        self.food.generate()
        self.state = self._get_state()

        return self.state,
    
    def render(self, mode='human'): #show game
        self.window.fill(self.black)
        self.snake.draw(self.window)
        self.food.draw(self.window)
        self.score_text = pygame.font.SysFont(None, 20).render(f"Score: {self.snake.length - 1}", True, self.white)
        self.window.blit(self.score_text, (10, 10))
        pygame.display.flip()
        self.clock.tick(self.fps)

    def close(self):
        pygame.quit()
        
    class Snake:
        window_width, window_height = 640, 480
        green = (0, 255, 0)
        size = 20
        def __init__(self, size):
            self.size = size
            self.x_pos = self.window_width // 2
            self.y_pos = self.window_height // 2
            self.x_vel = self.size
            self.y_vel = 0
            self.body = []
            self.length = 1
            self.can_change_direction = True

        def check_collision(self):
            head = (self.x_pos, self.y_pos)
            if self.x_pos < 0 or self.x_pos >= self.window_width or self.y_pos < 0 or self.y_pos >= self.window_height:
                return True
            if head in self.body[:-1]:
                return True

            return False

        def update(self):
            if not self.can_change_direction:
                self.can_change_direction = True
            self.x_pos += self.x_vel
            self.y_pos += self.y_vel
            self.body.append((self.x_pos, self.y_pos))
            if len(self.body) > self.length:
                del self.body[0]

            return True

        def move_up(self):
            if self.can_change_direction and self.y_vel != self.size:
                self.x_vel = 0
                self.y_vel = -self.size
                self.can_change_direction = False

        def move_down(self):
            if self.can_change_direction and self.y_vel != -self.size:
                self.x_vel = 0
                self.y_vel = self.size
                self.can_change_direction = False

        def move_left(self):
            if self.can_change_direction and self.x_vel != self.size:
                self.x_vel = -self.size
                self.y_vel = 0
                self.can_change_direction = False

        def move_right(self):
            if self.can_change_direction and self.x_vel != -self.size:
                self.x_vel = self.size
                self.y_vel = 0
                self.can_change_direction = False

        def draw(self, window):
            for segment in self.body:
                pygame.draw.rect(window, self.green, (segment[0], segment[1], self.size, self.size))

    class Food:
        window_width, window_height = 640, 480
        red = (255, 0, 0)
        size = 20
        def __init__(self, size):
            self.size = size
            self.x = random.randint(0, self.window_width - self.size) // self.size * self.size
            self.y = random.randint(0, self.window_height - self.size) // self.size * self.size

        def generate(self):
            self.x = random.randint(0, self.window_width - self.size) // self.size * self.size
            self.y = random.randint(0, self.window_height - self.size) // self.size * self.size

        def draw(self, window):
            pygame.draw.rect(window, self.red, (self.x, self.y, self.size, self.size))

env = SnakeEnv()
input = env.observation_space.shape
output = env.action_space.n
print(input)
print(env.observation_space.sample())
generations = 100
for generation in range(generations):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action = env.action_space.sample()
        next_state, reward, done, info = env.step(action)
        state = next_state
        score += reward
        env.render()