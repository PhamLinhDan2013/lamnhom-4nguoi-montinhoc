import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Streamlit Dino Pixel Game",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Đập Hộp Game Khủng Long Trên Streamlit")
st.caption("Phiên bản custom Pixel-Art đầy đủ Kho Nhân Vật, Tóc, Áo và Quần!")

# Toàn bộ mã nguồn HTML + CSS + JS của Game Khủng Long Custom
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #ffffff;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            user-select: none;
        }
        #game-container {
            position: relative;
            margin-top: 5px;
        }
        canvas {
            background: #fff;
            border-bottom: 2px solid #535353;
        }
        #custom-panel {
            width: 100%;
            max-width: 740px;
            background: #f7f7f7;
            margin-top: 15px;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            box-sizing: border-box;
        }
        .section {
            flex: 1;
            min-width: 200px;
            margin: 5px 10px;
        }
        .section-title {
            font-weight: bold;
            color: #333;
            border-bottom: 2px solid #ddd;
            padding-bottom: 5px;
            margin-bottom: 10px;
            font-size: 13px;
        }
        .options-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
        }
        .btn-opt {
            padding: 8px 2px;
            font-size: 11px;
            border: 2px solid #ccc;
            background: #fff;
            cursor: pointer;
            text-align: center;
            border-radius: 4px;
            font-family: inherit;
        }
        .btn-opt.active {
            border-color: #535353;
            background: #535353;
            color: #fff;
        }
        .btn-opt:hover:not(.active) {
            background: #eee;
        }
        #instructions {
            margin-top: 8px;
            color: #777;
            font-size: 12px;
            text-align: center;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <canvas id="gameCanvas" width="750" height="220"></canvas>
    </div>

    <div id="instructions">Bấm <b>Phím Cách (Spacebar)</b> hoặc chạm màn hình Game để Nhảy / Chơi lại</div>

    <div id="custom-panel">
        <!-- 1. Chọn nhân vật -->
        <div class="section">
            <div class="section-title">🦖 CHỌN NHÂN VẬT</div>
            <div class="options-grid" style="grid-template-columns: repeat(2, 1fr);">
                <button class="btn-opt active" onclick="setSkin('pink')">Khủng Long Hồng</button>
                <button class="btn-opt" onclick="setSkin('red')">Khủng Long Đỏ</button>
                <button class="btn-opt" onclick="setSkin('black')">Khủng Long Đen</button>
                <button class="btn-opt" onclick="setSkin('rainbow')">Cầu Vồng 🌈</button>
                <button class="btn-opt" onclick="setSkin('blue')">Khủng Long Xanh</button>
                <button class="btn-opt" onclick="setSkin('human')">👨 Con Người</button>
            </div>
        </div>

        <!-- 2. Chọn Tóc -->
        <div class="section">
            <div class="section-title">💇 KIỂU TÓC</div>
            <div class="options-grid">
                <button id="hair-0" class="btn-opt active" onclick="setHair(0)">Trọc</button>
                <button id="hair-1" class="btn-opt" onclick="setHair(1)">Tóc Ngầu</button>
                <button id="hair-2" class="btn-opt" onclick="setHair(2)">Quý Tộc</button>
            </div>
        </div>

        <!-- 3. Chọn Áo & Quần -->
        <div class="section">
            <div class="section-title">👕 TRANG PHỤC</div>
            <div style="font-size: 11px; margin-bottom: 2px;">Chọn Áo:</div>
            <div class="options-grid" style="margin-bottom: 8px;">
                <button id="shirt-0" class="btn-opt active" onclick="setShirt(0)">Không</button>
                <button id="shirt-1" class="btn-opt" onclick="setShirt(1)">Siêu Nhân</button>
                <button id="shirt-2" class="btn-opt" onclick="setShirt(2)">Hoàng Gia</button>
            </div>
            <div style="font-size: 11px; margin-bottom: 2px;">Chọn Quần:</div>
            <div class="options-grid">
                <button id="pant-0" class="btn-opt active" onclick="setPant(0)">Không</button>
                <button id="pant-1" class="btn-opt" onclick="setPant(1)">Quần Jean</button>
                <button id="pant-2" class="btn-opt" onclick="setPant(2)">Quần Lửa</button>
            </div>
        </div>
    </div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;

let currentSkin = 'pink';
let currentHair = 0;   
let currentShirt = 0;  
let currentPant = 0;   

const skinColors = {
    pink: '#ff8da1', red: '#ff3b30', black: '#2c2c2e', blue: '#007aff', human: '#ffcc99'
};

// Đồ họa ma trận Pixel gốc rút gọn tối ưu
const DINO_PIXEL = [,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
    [0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0]
];

const HUMAN_PIXEL = [,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
 ,
    [0,0,0,0,1,1,0,0,1,1,0,0,0,0]
];

function getPixelOverlay(row, col, baseMatrix) {
    if (currentHair === 1) { 
        if (baseMatrix === DINO_PIXEL && row === 0 && col >= 11 && col <= 15) return '#ff9500';
        if (baseMatrix === HUMAN_PIXEL && row === 0 && col >= 5 && col <= 9) return '#ff9500';
    } else if (currentHair === 2) { 
        if (baseMatrix === DINO_PIXEL && row === 0 && col >= 11 && col <= 17) return '#af52de';
        if (baseMatrix === HUMAN_PIXEL && row === 0 && col >= 5 && col <= 10) return '#af52de';
    }
    if (currentShirt === 1) { 
        if (baseMatrix === DINO_PIXEL && row >= 5 && row <= 8 && col >= 6 && col <= 11) return '#e74c3c';
        if (baseMatrix === HUMAN_PIXEL && row >= 4 && row <= 8 && col >= 5 && col <= 9) return '#e74c3c';
    } else if (currentShirt === 2) { 
        if (baseMatrix === DINO_PIXEL && row >= 5 && row <= 8 && col >= 6 && col <= 11) return '#ffcc00';
        if (baseMatrix === HUMAN_PIXEL && row >= 4 && row <= 8 && col >= 5 && col <= 9) return '#ffcc00';
    }
    if (currentPant === 1) { 
        if (baseMatrix === DINO_PIXEL && row >= 9 && row <= 11 && col >= 4 && col <= 9) return '#2f80ed';
        if (baseMatrix === HUMAN_PIXEL && row >= 9 && row <= 11 && col >= 5 && col <= 9) return '#2f80ed';
    } else if (currentPant === 2) { 
        if (baseMatrix === DINO_PIXEL && row >= 9 && row <= 11 && col >= 4 && col <= 9) return '#ff453a';
        if (baseMatrix === HUMAN_PIXEL && row >= 9 && row <= 11 && col >= 5 && col <= 9) return '#ff453a';
    }
    return null;
}

let gameSpeed = 6.5; let score = 0; let highScore = 0;
let isGameOver = false; let gameStarted = false;
let obstacles = []; let clouds = []; let gameFrame = 0;

const dino = {
    x: 60, y: 160, width: 44, height: 44, vy: 0, gravity: 0.6, jumpForce: -11.5, isGrounded: true, legFrame: 0,
    update: function() {
        this.vy += this.gravity; this.y += this.vy;
        if (this.y >= 160) { this.y = 160; this.vy = 0; this.isGrounded = true; } else { this.isGrounded = false; }
        if (gameStarted && !isGameOver && gameFrame % 8 === 0) { this.legFrame = this.legFrame === 0 ? 1 : 0; }
    },
    draw: function() {
        const matrix = currentSkin === 'human' ? HUMAN_PIXEL : DINO_PIXEL;
        const pixelSize = 2.8;
        for (let r = 0; r < matrix.length; r++) {
            for (let c = 0; c < matrix[r].length; c++) {
                let cell = matrix[r][c];
                if (this.isGrounded && currentSkin !== 'human') {
                    if (this.legFrame === 0 && r >= 13 && c === 5) continue;
                    if (this.legFrame === 1 && r >= 13 && c === 7) continue;
                }
                if (cell > 0 || getPixelOverlay(r, c, matrix) !== null) {
                    let color = '#000'; const overlay = getPixelOverlay(r, c, matrix);
                    if (overlay) { color = overlay; } 
                    else if (cell === 2) { color = '#ffffff'; } 
                    else if (cell === 1) {
                        color = currentSkin === 'rainbow' ? `hsl(${(gameFrame * 3 + r * 15) % 360}, 90%, 65%)` : skinColors[currentSkin];
                    }
                    ctx.fillStyle = color;
                    ctx.fillRect(this.x + (c * pixelSize), this.y + (r * pixelSize), pixelSize + 0.2, pixelSize + 0.2);
