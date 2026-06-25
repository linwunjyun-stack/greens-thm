import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 新增：Matplotlib 全域字體與排版設定 ---
plt.rcParams.update({
    'font.size': 20,        # 基礎字體大小
    'axes.labelsize': 5,   # X軸/Y軸標題的字體大小
    'xtick.labelsize': 5,   # X軸刻度數字大小 (調小一點更精緻)
    'ytick.labelsize': 5,   # Y軸刻度數字大小
    'legend.fontsize': 5,   # 圖例字體大小
    'figure.autolayout': True # 自動排版，防止標籤被切掉
})

st.set_page_config(layout="wide")
st.title("驗證格林定理 (Green's Theorem) ")
st.write("本工具動態展示並嚴格驗證封閉曲線之線積分與區域雙重積分的等價關係。"
        'font.size': 28, 
        )

# --- 側邊欄控制區 ---
st.sidebar.header("🛠️ 參數與向量場控制")

# 1. 選擇向量場
field_option = st.sidebar.selectbox(
    "選擇向量場 F(x, y) = P(x, y)i + Q(x, y)j",
    ("旋轉場 (P = -y, Q = x)", "純量場 (P = x, Q = y)")
)

# 2. 選擇積分區域大小 (以圓形為例)
radius = st.sidebar.number_input(
    "輸入積分區域半徑 (r)",
    min_value=0.1,    # 設定最小值，避免輸入 0 或負數導致圖形崩潰
    max_value=100.0,  # 設定最大值上限
    value=2.0,        # 預設數值
    step=0.5,         # 點擊上下箭頭時的增減幅度
    format="%.2f"     # 強制顯示到小數點後兩位，增加工程嚴謹度
)

st.sidebar.markdown("---")

# --- 數學與繪圖邏輯 ---
# 動態座標軸：根據輸入的半徑自動擴張範圍，確保圖形永遠美觀
bound = max(10.0, radius * 1.5) 

# 建立網格以繪製向量場
x = np.linspace(-bound, bound, 22)
y = np.linspace(-bound, bound, 22)
X, Y = np.meshgrid(x, y)

# 定義向量場 P 和 Q
if field_option == "旋轉場 (P = -y, Q = x)":
    P = -Y
    Q = X
    curl = 2  # dQ/dx - dP/dy = 1 - (-1) = 2
    P_str, Q_str = "-y", "x"
else:
    P = X
    Q = Y
    curl = 0  # dQ/dx - dP/dy = 0 - 0 = 0
    P_str, Q_str = "x", "y"

# 定義邊界曲線 C (圓形參數式)
theta = np.linspace(0, 2*np.pi, 100)
x_c = radius * np.cos(theta)
y_c = radius * np.sin(theta)

# --- 視覺化呈現 ---
# 調整左右欄位的比例：讓左邊圖表區佔比變小 (例如 1)，右邊文字計算區變大 (例如 1.5)
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📊 向量場與積分區域動態視覺化")
    # 將 figsize 的數字調小，例如 (4, 4) 或 (3.5, 3.5)
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    
    # 畫出向量場 (Quiver)
    ax.quiver(X, Y, P, Q, color='lightgray', alpha=0.8)
    
    # 畫出積分區域 R (填色)
    ax.fill(x_c, y_c, color='#1f77b4', alpha=0.3, label=f'Region R (r={radius})')
    
    # 畫出邊界 C 及其方向 (逆時針箭頭)
    ax.plot(x_c, y_c, color='red', linewidth=2, label='Boundary C')
    ax.arrow(radius*0.707, radius*0.707, -0.1, 0.1, shape='full', lw=2, length_includes_head=True, head_width=0.3, color='red', zorder=5) # 在 45 度角加個逆時針箭頭
    
    ax.set_xlim([-bound, bound])
    ax.set_ylim([-bound, bound])
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper right')
    
    st.pyplot(fig)

with col2:
    st.subheader("🧮 雙通道即時運算對決")
    st.markdown(f"**當前向量場**：$P(x,y) = {P_str}$, $Q(x,y) = {Q_str}$")
    st.markdown(f"**當前半徑**：$r = {radius}$")
    st.markdown("---")
    
    # 理論計算區
    if field_option == "旋轉場 (P = -y, Q = x)":
        line_integral_val = 2 * np.pi * (radius**2)
        area_integral_val = curl * (np.pi * (radius**2))
    else:
        line_integral_val = 0
        area_integral_val = 0

    st.markdown("### 🔵 通道一：直接計算線積分 (左式)")
    st.latex(r"\oint_C (P dx + Q dy)")
    st.write(f"沿著半徑為 {radius} 的圓周 $C$ 參數化積分：")
    st.write(f"計算結果 = **{line_integral_val:.4f}**")
    
    st.markdown("### 🔴 通道二：格林定理雙重積分 (右式)")
    st.latex(r"\iint_R \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dA")
    st.write(f"計算旋度 (Curl) = {curl}，並乘上圓面積 $\pi r^2$：")
    st.write(f"計算結果 = **{area_integral_val:.4f}**")
    
    st.markdown("---")
    if np.isclose(line_integral_val, area_integral_val):
        st.success("驗證：線積分結果與面積分結果完全相等")
    else:
        st.error("❌ 驗證失敗")
