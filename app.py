import streamlit as st
import time
import random

# Cấu hình trang Streamlit
st.set_page_config(page_title="Pixel Dino Adventure", page_icon="🦖", layout="centered")

# Khởi tạo trạng thái game (Session State)
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.dino_y = 0        # Độ cao của khủng long (0: mặt đất)
    st.session_state.is_jumping = False
    st.session_state.is_flying = False # Trạng thái bay bằng jetpack
    st.session_state.fly_start_time = 0
    st.session_state.obstacle_count = 0 # Đếm số chướng ngại vật đã vượt qua
    st.session_state.map_state = "DESERT" # Bản đồ: DESERT (Xương rồng) hoặc ROAD (Tảng đá)
    st.session_state.obstacle_x = 100  # Vị trí chướng ngại vật (chạy từ phải 100% sang trái 0%)
    st.session_state.current_obstacle_type = "CACTUS"

# Định nghĩa giao diện đồ họa Pixel Art bằng CSS
st.markdown("""
<style>
    .game-container {
        width: 100%;
        height: 250px;
        background-color: #f7f7f7;
        border-bottom: 3px solid #535353;
        position: relative;
        overflow: hidden;
        border-radius: 8px;
    }
    .road-theme {
        background-color: #9E9E9E !important;
        border-bottom: 5px dashed #FFF !important;
    }
    /* Chú Khủng Long Pixel Google siêu đẹp */
    .dino {
        width: 44px;
        height: 47px;
        position: absolute;
        bottom: 0px;
        left: 50px;
        transition: bottom 0.1s ease-out;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://w3.org" viewBox="0 0 22 24" shape-rendering="crispEdges"><path d="M14 0h6v1h2v2h-2v1h-2v1h-4V4h-2V3h2V2h2V1h-2zm-4 4h4v1h-4zm-2 1h2v1H8zm-1 1h1v1H7zm-1 1h1v1H6zm-1 1h1v6H5zm-1 6h1v4H4zm1 4h1v1H5zm1 1h2v1H6zm5-13h1v1h-1zm1 3h7v1h-7zm0 1h8v1h-8zm0 1h9v1h-9zm0 1h7v1h-7zm0 1h5v1h-5zm0 1h4v1h-4zm0 1h6v1h-6zm0 1h7v1h-7zm1 1h6v1h-6zm1 1h5v1h-5zm1 1h4v1h-4zm-7 1h2v1H8zm1 1h2v1H9zm2 1h2v1h-2zm4-4h1v3h-1zm2 1h1v3h-1z" fill="%23535353"/></svg>');
        background-size: contain;
        background-repeat: no-repeat;
    }
    .jetpack {
        box-shadow: 0 -8px 0 #FF5722, 0 -16px 0 #FFC107;
        animation: burn 0.1s infinite alternate;
    }
    /* Xương rồng Pixel */
    .cactus {
        width: 25px;
        height: 50px;
        position: absolute;
        bottom: 0px;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://w3.org" viewBox="0 0 10 20" shape-rendering="crispEdges"><path d="M3 0h3v20H3zm-2 4h2v7H1zm6 3h2v6H7z" fill="%23388E3C"/></svg>');
        background-size: contain;
        background-repeat: no-repeat;
    }
    /* Cây thứ 6 có trang bị bay */
    .jetpack-cactus {
        width: 30px;
        height: 50px;
        position: absolute;
        bottom: 0px;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://w3.org" viewBox="0 0 12 20" shape-rendering="crispEdges"><path d="M2 0h3v20H2zm5 2h3v10H7z" fill="%23388E3C"/><path d="M7 2h4v5H7z" fill="%23FF5722"/></svg>');
        background-size: contain;
        background-repeat: no-repeat;
    }
    /* Tảng đá Pixel ngoài đường */
    .rock {
        width: 35px;
        height: 30px;
        position: absolute;
        bottom: 0px;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://w3.org" viewBox="0 0 12 10" shape-rendering="crispEdges"><path d="M3 0h6v2h3v5H9v3H0V5h3z" fill="%23616161"/></svg>');
        background-size: contain;
        background-repeat: no-repeat;
    }
    /* Cổng dịch chuyển mãnh liệt */
    .portal {
        width: 40px;
        height: 70px;
        position: absolute;
        bottom: 0px;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://w3.org" viewBox="0 0 10 20" shape-rendering="crispEdges"><path d="M0 0h10v20H0z" fill="%23E040FB"/></svg>');
        background-size: contain;
        background-repeat: no-repeat;
        box-shadow: 0 0 15px #E040FB;
        border-radius: 50%;
    }
</style>
""", unsafe_allow_html=True)

st.title("🦖 Siêu Khủng Long Pixel Phiêu Lưu Ký")
st.write("Nhấn nút **Nhảy 🦘** để vượt qua các chướng ngại vật theo cốt truyện đặc biệt!")

# Cơ chế điều khiển hành động
def trigger_jump():
    if not st.session_state.game_over and not st.session_state.is_jumping and not st.session_state.is_flying:
        st.session_state.is_jumping = True
        st.session_state.dino_y = 90  # Nhảy lên cao

def reset_game():
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.dino_y = 0
    st.session_state.is_jumping = False
    st.session_state.is_flying = False
    st.session_state.obstacle_count = 0
    st.session_state.map_state = "DESERT"
    st.session_state.obstacle_x = 100
    st.session_state.current_obstacle_type = "CACTUS"

# Vòng lặp cập nhật chuyển động logic (Game Loop Tích Hợp)
if not st.session_state.game_over:
    # 1. Di chuyển chướng ngại vật từ phải sang trái
    st.session_state.obstacle_x -= 8
    
    # Xử lý hiệu ứng rơi sau khi nhảy
    if st.session_state.is_jumping:
        st.session_state.dino_y -= 15
        if st.session_state.dino_y <= 0:
            st.session_state.dino_y = 0
            st.session_state.is_jumping = False

    # Xử lý tính năng BAY 3 GIÂY của Cây thứ 6
    if st.session_state.is_flying:
        st.session_state.dino_y = 120 # Giữ khủng long trên trời cao hẳn
        if time.time() - st.session_state.fly_start_time > 3.0:
            st.session_state.is_flying = False
            st.session_state.dino_y = 0 # Đáp xuống vị trí trống an toàn

    # 2. Định nghĩa thể loại chướng ngại vật dựa trên số lượng đếm được
    count = st.session_state.obstacle_count
    if st.session_state.map_state == "DESERT":
        if count == 5:
            st.session_state.current_obstacle_type = "JETPACK_CACTUS"
        elif count == 11:
            st.session_state.current_obstacle_type = "PORTAL"
        else:
            st.session_state.current_obstacle_type = "CACTUS"
    else:
        st.session_state.current_obstacle_type = "ROCK"

    # 3. Khi chướng ngại vật chạy hết màn hình bên trái -> Vượt qua thành công
    if st.session_state.obstacle_x < 0:
        st.session_state.obstacle_x = 100
        st.session_state.obstacle_count += 1
        st.session_state.score += 10
        
        # Nếu vừa đi qua cổng dịch chuyển -> Đổi bản đồ sang Ngoài Đường
        if st.session_state.current_obstacle_type == "PORTAL":
            st.session_state.map_state = "ROAD"

    # 4. Kiểm tra va chạm (Collision Detection) khi vật thể đến gần Khủng long (khoảng x từ 10% đến 22%)
    if 10 <= st.session_state.obstacle_x <= 22:
        # Nếu va chạm vào cây số 6 mang Jetpack -> Kích hoạt bay lên trời
        if st.session_state.current_obstacle_type == "JETPACK_CACTUS":
            if not st.session_state.is_flying:
                st.session_state.is_flying = True
                st.session_state.fly_start_time = time.time()
        # Đối với các chướng ngại vật nguy hiểm thông thường (Cactus hoặc Rock)
        elif st.session_state.current_obstacle_type in ["CACTUS", "ROCK"]:
            if st.session_state.dino_y < 40: # Khủng long nhảy không đủ cao
                st.session_state.game_over = True

# --- THIẾT KẾ ĐỒ HỌA RENDER RA MÀN HÌNH ---
container_class = "game-container road-theme" if st.session_state.map_state == "ROAD" else "game-container"
dino_jetpack_effect = "jetpack" if st.session_state.is_flying else ""
obs_type = st.session_state.current_obstacle_type.lower().replace("_", "-")

game_html = f"""
<div class="{container_class}">
    <!-- Chú Khủng long Google -->
    <div class="dino {dino_jetpack_effect}" style="bottom: {st.session_state.dino_y}px;"></div>
    <!-- Chướng ngại vật chuyển động -->
    <div class="{obs_type}" style="left: {st.session_state.obstacle_x}%;"></div>
</div>
"""
st.markdown(game_html, unsafe_allow_html=True)

# Bảng trạng thái thông tin game
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.metric("🏆 Điểm số", f"{st.session_state.score}")
with col_info2:
    st.metric("🗺️ Bản đồ hiện tại", "Bên Ngoài Đường 🛣️" if st.session_state.map_state == "ROAD" else "Sa mạc Xương rồng 🏜️")
with col_info3:
    st.metric("🚩 Chướng ngại vật", f"{st.session_state.obstacle_count} / Đang đợi...")

# Giao diện các nút tương tác điều khiển hành động
st.write("")
if st.session_state.game_over:
    st.error("💥 GAME OVER! Chú khủng long đã va chạm chướng ngại vật.")
    st.button("🔄 Chơi lại từ đầu", on_click=reset_game, type="primary", use_container_width=True)
else:
    if st.session_state.is_flying:
        st.warning("🚀 ĐANG BAY BẰNG JETPACK TRÊN TRỜI CAO TRONG 3 GIÂY! HÃY ĐỢI ĐÁP XUỐNG...")
    st.button("🦘 NHẢY LÊN", on_click=trigger_jump, type="primary", use_container_width=True)

# Cơ chế tự động làm mới khung hình để tạo chuyển động mượt mà liên tục
if not st.session_state.game_over:
    time.sleep(0.08)
    st.rerun()
