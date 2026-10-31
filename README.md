import streamlit as st
import random
import time

# Cấu hình trang Streamlit
st.set_page_config(page_title="Streamlit Snake Game", page_icon="🐍", layout="centered")

# Tiêu đề game
st.title("🐍 Trò chơi Rắn Săn Mồi trên Streamlit")
st.write("Sử dụng các nút bấm bên dưới để điều khiển chú rắn ăn mồi!")

# Kích thước bàn cờ
GRID_SIZE = 15

# Khởi tạo trạng thái game (Session State)
if 'snake' not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 6), (5, 7)] # Tọa độ ban đầu của rắn
    st.session_state.direction = "UP"                 # Hướng đi ban đầu
    st.session_state.food = (10, 10)                  # Vị trí mồi ban đầu
    st.session_state.score = 0                        # Điểm số
    st.session_state.game_over = False               # Trạng thái kết thúc game

# Hàm tạo mồi mới ngẫu nhiên không trùng với thân rắn
def generate_food():
    while True:
        pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        if pos not in st.session_state.snake:
            return pos

# Hàm cập nhật logic trò chơi sau mỗi bước đi
def move_snake():
    if st.session_state.game_over:
        return

    # Lấy vị trí đầu rắn hiện tại
    head_x, head_y = st.session_state.snake[0]
    
    # Xác định tọa độ đầu mới dựa trên hướng đi
    if st.session_state.direction == "UP":
        new_head = (head_x - 1, head_y)
    elif st.session_state.direction == "DOWN":
        new_head = (head_x + 1, head_y)
    elif st.session_state.direction == "LEFT":
        new_head = (head_x, head_y - 1)
    elif st.session_state.direction == "RIGHT":
        new_head = (head_x, head_y + 1)

    # Kiểm tra va chạm biên hoặc va chạm chính mình
    if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or 
        new_head[1] < 0 or new_head[1] >= GRID_SIZE or 
        new_head in st.session_state.snake):
        st.session_state.game_over = True
        return

    # Thêm đầu mới vào thân rắn
    st.session_state.snake.insert(0, new_head)

    # Kiểm tra nếu rắn ăn được mồi
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = generate_food()
    else:
        # Nếu không ăn mồi, xóa phần đuôi cũ để giữ nguyên chiều dài
        st.session_state.snake.pop()

# Hàm xử lý khi bấm nút điều khiển
def change_direction(new_dir):
    # Tránh việc rắn tự quay đầu ngược lại trực tiếp (ví dụ đang UP không thể chuyển ngay thành DOWN)
    oppositie_dirs = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
    if new_dir != oppositie_dirs.get(st.session_state.direction):
        st.session_state.direction = new_dir
        move_snake()

# Hàm reset lại game từ đầu
def reset_game():
    st.session_state.snake = [(5, 5), (5, 6), (5, 7)]
    st.session_state.direction = "UP"
    st.session_state.food = (10, 10)
    st.session_state.score = 0
    st.session_state.game_over = False

# --- GIAO DIỆN ĐIỀU KHIỂN ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.button("⬆️ Lên", on_click=change_direction, args=("UP",), use_container_width=True)
    
col_left, col_space, col_right = st.columns([1.5, 0.2, 1.5])
with col_left:
    st.button("⬅️ Trái", on_click=change_direction, args=("LEFT",), use_container_width=True)
with col_right:
    st.button("Phải ➡️", on_click=change_direction, args=("RIGHT",), use_container_width=True)
    
with col2:
    st.button("⬇️ Xuống", on_click=change_direction, args=("DOWN",), use_container_width=True)

st.markdown("---")

# Hiển thị điểm số và trạng thái game
st.subheader(f"🏆 Điểm số: {st.session_state.score}")

if st.session_state.game_over:
    st.error("💥 GAME OVER! Chú rắn của bạn đã va chạm.")
    st.button("🔄 Chơi lại", on_click=reset_game, type="primary")

# --- VẼ BÀN CỜ GAME ---
# Xây dựng bảng hiển thị bằng Emoji
grid_html = ""
for r in range(GRID_SIZE):
    row_str = ""
    for c in range(GRID_SIZE):
        if (r, c) == st.session_state.snake[0]:
            row_str += "👺" # Đầu rắn
        elif (r, c) in st.session_state.snake:
            row_str += "🟢" # Thân rắn
        elif (r, c) == st.session_state.food:
            row_str += "🍎" # Mồi ngon
        else:
            row_str += "⬜" # Ô trống
    grid_html += row_str + "<br>"

# Render bàn cờ ra màn hình bằng markdown hỗ trợ HTML font lớn
st.markdown(
    f"<div style='font-family: monospace; font-size: 20px; line-height: 20px; text-align: center;'>{grid_html}</div>", 
    unsafe_allow_html=True
)

# Tự động cập nhật di chuyển chậm nếu game chưa kết thúc (Cơ chế auto-tick cơ bản)
if not st.session_state.game_over:
    time.sleep(0.4)
    move_snake()
    st.rerun()
