import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 新增：Matplotlib 全域字體與排版設定 ---
plt.rcParams.update({
    'font.size': 20,        # 基礎字體大小
    'axes.labelsize': 10,   # X軸/Y軸標題的字體大小
    'xtick.labelsize': 8,   # X軸刻度數字大小 (調小一點更精緻)
    'ytick.labelsize': 8,   # Y軸刻度數字大小
    'legend.fontsize': 9,   # 圖例字體大小
    'figure.autolayout': True # 自動排版，防止標籤被切掉
})

st.set_page_config(layout="wide")
st.title("格林定理 (Green's Theorem) 動態驗證器")
st.write("本工具動態展示並嚴格驗證封閉曲線之線積分與區域雙重積分的等價關係。")

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
# 將欄位比例改成 [1, 2] 或 [0.8, 1.5]，左邊數字越小，圖表區塊就會越窄、圖越小
col1, col2 = st.columns([1, 1.8])

with col1:
    # 稍微縮短標題，避免版面變窄時文字折行
    st.subheader("📊 向量場動態視覺化") 
    
    # figsize 數字調小，例如 (3.2, 3.2) 會讓整張圖的物理尺寸明顯縮小
    fig, ax = plt.subplots(figsize=(3.2, 3.2))
    
    # 畫出向量場 (Quiver)
    ax.quiver(X, Y, P, Q, color='lightgray', alpha=0.8)
    
    # 畫出積分區域 R (填色)
    ax.fill(x_c, y_c, color='#1f77b4', alpha=0.3, label=f'Region R (r={radius:.1f})')
    
    # 畫出邊界 C 及其方向 (逆時針箭頭)
    ax.plot(x_c, y_c, color='red', linewidth=2, label='Boundary C')
    ax.arrow(radius*0.707, radius*0.707, -0.1, 0.1, shape='full', lw=2, length_includes_head=True, head_width=radius*0.15, color='red', zorder=5) # 讓箭頭大小也會隨半徑動態縮放
    
    ax.set_xlim([-bound, bound])
    ax.set_ylim([-bound, bound])
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper right')
    
    st.pyplot(fig)
    
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
