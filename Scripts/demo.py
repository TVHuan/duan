import pygame
import random

pygame.init()

SIZE = 4 #xác định kích thước cảu bảng:4*4
TILE_SIZE = 100#mỗi ô với kích thước 100*100
GRID_SIZE = SIZE * TILE_SIZE#kích thước màn hình=kthuoc mỗi ô*số lượng ô theo chiều rộng và ccao
FONT = pygame.font.Font(None, 36)#khởi tạo đối tượng Font cảu pgame để vẽ văn bản,c kthuoc là 36 và font mặc định
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)#định nghĩa màu sắc cơ bản

screen = pygame.display.set_mode((GRID_SIZE, GRID_SIZE))#tạo cửa sổ màn hình để vẽ ô và hiển thị trò chơi
pygame.display.set_caption('2048 Game')#đặt tiêu đề cửa sổ

def initialize_board():#tạo 1 mảng trắng 2D
    return [[0] * SIZE for _ in range(SIZE)]#trả về mảng 2D,tạo một list chứa "SIZE" số 0 và tạo một bảng 'size*size'toàn số 0

def add_new_tile(board):#thêm một ô mơới vaào bảng với gtri 2 hoặc 4(ô mới được thêm ngẫu nhiên vào một ô trống có giá trong
    empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4#gán giá trị 2 or 4 cho ô vừa chọn với xác suất 90% là 2 và 10% là 4

def draw_board(board):#vẽ bảng trò chơi lên màn hình
    for i in range(SIZE):
        for j in range(SIZE):
            pygame.draw.rect(screen, GRAY, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))#vẽ một hình vuông màu xám tại vị trí (j * TILE_SIZE, i * TILE_SIZE) với kích thước là TILE_SIZE x TILE_SIZE.
            if board[i][j] != 0:
                draw_tile(j * TILE_SIZE + TILE_SIZE / 2, i * TILE_SIZE + TILE_SIZE / 2, str(board[i][j]))#gọi hàm 'draw_tile' để vẽ giá trị cảu ô bên trong ô đó

def draw_tile(x, y, value):#vẽ một ô trong bảng trò chơi,được vẽ dạng hình tròn và giá trị của ô được hiển thị
    pygame.draw.circle(screen, get_tile_color(int(value)), (int(x), int(y)), TILE_SIZE // 2 - 5)#màu sắc của ô được
    text = FONT.render(value, True, BLACK)#tạo một đối tượng văn bản pygame cos gtri value
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)#vẽ đối tượng lên màn

def get_tile_color(value):#trả về màu sắc tuowgn ứng với giá trị của ô
    colors = {2: (255, 255, 150), 4: (255, 255, 100), 8: (255, 200, 100), 16: (255, 150, 100),
              32: (255, 100, 100), 64: (255, 50, 50), 128: (255, 0, 0), 256: (200, 0, 0),
              512: (150, 0, 0), 1024: (100, 0, 0), 2048: (50, 0, 0)}
    return colors.get(value, (0, 0, 0))#trả về giá trị màu sắc mỗi ô

def move(board, direction):#định nghĩa hàm move để thuwcj hiện di chuyển ô
    if direction == 'left':
        for row in board:
            row[:] = merge_tiles(row)#gán giá trị hàng sau khi hợp nhất trở lại hàng
    elif direction == 'right':
        for row in board:
            row[:] = merge_tiles(row[::-1])[::-1]#gán và đảo ngược
    elif direction == 'up':
        for col in range(SIZE):#duyệt từng cột
            column = [board[row][col] for row in range(SIZE)]#tạo danh sách chứ giá trị từng ô
            merged_column = merge_tiles(column)#hợp nhất cột và lưu
            for row in range(SIZE):
                board[row][col] = merged_column[row]
    elif direction == 'down':
        for col in range(SIZE):
            column = [board[row][col] for row in range(SIZE - 1, -1, -1)]#tạo danh sách chứa gtri từng ô trong cột
            merged_column = merge_tiles(column)
            for row in range(SIZE - 1, -1, -1):
                board[row][col] = merged_column[SIZE - 1 - row]#duyệt qua từng hàng,nhưng đảo ngược lại

def merge_tiles(line):#hợp nhất các ô c giá trị trong 1 dòng(cột)
    new_line = [0] * SIZE#tạo dòng mới chứa'size' số 0
    index = 0#giữ vị trí hiện tại trong dòng mới
    for tile in line:#duyệt qua từng ô trong dòng đầu vào
        if tile != 0:
            if new_line[index] == 0:#nếu ô tiếp theo trong dòng mới trống,gán giá trị ô hiện tại vào
                new_line[index] = tile
            elif new_line[index] == tile:#giống thì hợp nhaats
                new_line[index] *= 2
                index += 1
            else:#di chuyển ô tiếp theo trong dòng mới
                index += 1
                new_line[index] = tile
    return new_line#trả về dòng moi

def is_game_over(board):#kiểm tra trò chơi kết thúc chưa
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0 or (j < SIZE - 1 and board[i][j] == board[i][j + 1]) or (i < SIZE - 1 and board[i][j] == board[i + 1][j]):
                return False#thoar mãn dkien thì chưa kết thúc và ngược lại
    return True

def run_game():
    board = initialize_board()#khởi tạo một bảng
    add_new_tile(board)#thêm một ô mới vào bảng
    add_new_tile(board)

    while True:#vòng vô hạn làm trò chơi chạy mãi
        for event in pygame.event.get() :#duyệtện qua pygame
            if event.type == pygame.QUIT:#kiểm tra nếu sư kiện là việc đóng cửa sổ
                pygame.quit()#kết thúc gảme
                quit()#kết thúc cả chương trình
            elif event.type == pygame.KEYDOWN:#nếu sự kiện là phím nhấn
                if event.key == pygame.K_LEFT:
                    move(board, 'left')
                elif event.key == pygame.K_RIGHT:
                    move(board, 'right')
                elif event.key == pygame.K_UP:
                    move(board, 'up')
                elif event.key == pygame.K_DOWN:
                    move(board, 'down')
                add_new_tile(board)#sau bất kỳ một di chuyển nào ta thêm ô mới vào bảng

        screen.fill(WHITE)#xóa màn hình bằng cách tô trắng
        draw_board(board)
        pygame.display.update()#cập nhật màn hình để hển thị trạng thái
#kiểm tra trò chơi ết thúc chưa
        if is_game_over(board):
            print("Game Over!")
            pygame.quit()
            quit()

run_game()#chạy trò chơi
