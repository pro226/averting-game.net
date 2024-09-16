import pyxel
import time
import random

# ゲームの設定
WINDOW_WIDTH = 160
WINDOW_HEIGHT = 120
BALL_SIZE = 8
PLAYER_SIZE = 8
BALL_COLORS = [8, 10]  # 赤色(8)または黄色(10)
PLAYER_COLOR = 12  # 水色
SCORE_INCREMENT_INTERVAL = 1.2  # スコア追加の間隔（秒）
BALL_GENERATION_INTERVAL = 0.8  # ボールを生成する間隔

# ゲーム状態
ball_positions = []
ball_colors = []
score = 0
high_score = 0
start_time = time.time()
last_ball_generation_time = time.time()
game_over = False
player_x = WINDOW_WIDTH // 2
player_y = WINDOW_HEIGHT - PLAYER_SIZE - 2  # プレイヤーは画面下部に配置

def reset_game():
    global ball_positions, ball_colors, score, start_time, last_ball_generation_time, game_over, player_x
    ball_positions = []
    ball_colors = []
    score = 0
    start_time = time.time()
    last_ball_generation_time = time.time()
    game_over = False
    player_x = WINDOW_WIDTH // 2

def update_ball_positions():
    global ball_positions, ball_colors, last_ball_generation_time
    current_time = time.time()
    
    # 0.8秒ごとにボールを生成
    if current_time - last_ball_generation_time > BALL_GENERATION_INTERVAL:
        for _ in range(5):
            ball_positions.append([random.randint(0, WINDOW_WIDTH - BALL_SIZE), -BALL_SIZE])
            ball_colors.append(random.choice(BALL_COLORS))
        last_ball_generation_time = current_time
    
    # ボールの移動
    for i in range(len(ball_positions)):
        ball_positions[i][1] += 1

    # 画面外に出たボールを削除（ゲーム終了にはならない）
    ball_positions = [pos for pos in ball_positions if pos[1] < WINDOW_HEIGHT]
    ball_colors = [color for i, color in enumerate(ball_colors) if i < len(ball_positions)]

def check_collision():
    for bx, by in ball_positions:
        if bx < player_x + PLAYER_SIZE and bx + BALL_SIZE > player_x and by < player_y + PLAYER_SIZE and by + BALL_SIZE > player_y:
            return True
    return False

def update_score():
    global score, start_time
    if time.time() - start_time > SCORE_INCREMENT_INTERVAL:
        score += 2
        start_time = time.time()

def draw_game():
    pyxel.cls(0)
    
    # プレイヤーの描画（水色ではっきり表示）
    pyxel.rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE, PLAYER_COLOR)
    
    # ボールの描画（赤または黄色）
    for (bx, by), color in zip(ball_positions, ball_colors):
        pyxel.rect(bx, by, BALL_SIZE, BALL_SIZE, color)
    
    # スコアとハイスコアを左上に表示
    pyxel.text(10, 10, f"Score: {score}", 7)
    pyxel.text(10, 20, f"High Score: {high_score}", 7)

    # ゲームオーバー画面
    if game_over:
        pyxel.cls(0)
        pyxel.text(50, 50, "GAME OVER", 8)
        pyxel.text(50, 60, f"Score: {score}", 7)
        pyxel.text(50, 70, f"High Score: {high_score}", 7)
        pyxel.text(50, 90, "Press R to Restart", 7)

def update_game():
    global ball_positions, score, high_score, game_over, player_x
    if not game_over:
        update_ball_positions()
        update_score()

        # プレイヤーの左右移動
        if pyxel.btn(pyxel.KEY_LEFT):
            player_x = max(player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            player_x = min(player_x + 2, WINDOW_WIDTH - PLAYER_SIZE)

        # 衝突判定
        if check_collision():
            high_score = max(score, high_score)
            game_over = True

    # ゲーム再スタート
    if game_over and pyxel.btnp(pyxel.KEY_R):
        reset_game()

def main():
    pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)
    reset_game()
    pyxel.run(update_game, draw_game)

if __name__ == "__main__":
    main()
