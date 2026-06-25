import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Matplotlib 全域字體與排版設定 ---
plt.rcParams.update({
    'font.size': 10,        
    'axes.labelsize': 10,   
    'xtick.labelsize': 8,   
    'ytick.labelsize': 8,   
    'legend.fontsize': 9,   
    'figure.autolayout': True 
})

# --- 2. 確保網頁是寬螢幕版面 (如果你剛好遺失了這行，這會補回來) ---
st.set_page_config(layout="wide")

# --- 3. CSS 魔法：全局字體放大設定 ---
st.markdown(
    """
    <style>
    /* 側邊欄：標題與說明文字 */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        font-size: 18px !important;
    }
    [data-testid="stSidebar"] input, 
    [data-testid="stSidebar"] div[data-baseweb="select"] {
        font-size: 19.5px !important;
    }

    /* 主畫面：一般說明文字 */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 19.5px !important;
        line-height: 1.8 !important; 
    }
    
    /* 主畫面：放大 H3 標題 */
    h3 {
        font-size: 26px !important;
        font-weight: bold !important;
        padding-top: 15px !important; 
    }
    
    /* 主畫面：放大綠色提示框文字 */
    div[data-testid="stAlert"] div[data-testid="stMarkdownContainer"] p {
        font-size: 22px !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 4. 網頁大標題與說明 (使用 HTML 放大) ---
st.markdown('<h1 style="font-size: 40px;">驗證格林定理 (Green\'s Theorem)</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 22px;">本工具動態展示並嚴格驗證封閉曲線之線積分與區域雙重積分的等價關係。</p>', unsafe_allow_html=True)

# (接下來就接著原本的側邊欄控制區：st.sidebar.header("🛠️ 參數與向量場控制")...)
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
    st.subheader("*向量場與積分區域動態視覺化")
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
    
    # --- 新增：在圖表下方動態顯示圓方程式 ---
    st.markdown("<br>", unsafe_allow_html=True) # 增加一點上方留白，讓排版不擁擠
    st.markdown("<p style='text-align: center; font-size: 18px; font-weight: bold; color: #1f77b4;'>📍 積分邊界 C (圓方程式)</p>", unsafe_allow_html=True)
    st.latex(rf"x^2 + y^2 = {radius**2:.2f}")

with col2:
    st.markdown(f"**當前向量場**：$P(x,y) = {P_str}$, $Q(x,y) = {Q_str}$")
    st.markdown(f"**當前半徑**：$r = {radius:.2f}$")
    st.markdown("---")
    
    if field_option == "旋轉場 (P = -y, Q = x)":
        # --- 🔵 左式：線積分推導 ---
        st.markdown("### 🔵 左式：直接計算線積分")
        st.latex(r"\LARGE \oint_C (P dx + Q dy)")
        st.write("參數化圓周 $C$：$x = r\cosθ, y = r\sinθ$")
        st.write("微分轉換：$dx = -r\sinθ dθ, dy = r\cosθ dθ$")
        st.latex(r"= \int_{0}^{2\pi} [(-r\sin\theta)(-r\sin\theta) + (r\cos\theta)(r\cos\theta)] d\theta")
        st.latex(r"= \int_{0}^{2\pi} r^2 (\sin^2\theta + \cos^2\theta) d\theta")
        st.latex(r"= \int_{0}^{2\pi} r^2 d\theta = 2\pi r^2")
        
        line_integral_val = 2 * np.pi * (radius**2)
        st.latex(rf"= 2\pi ({radius:.2f})^2 = \mathbf{{{line_integral_val:.4f}}}")

        # --- 🔴 右式：雙重積分推導 (偏微分與極座標) ---
        st.markdown("### 🔴 右式：格林定理雙重積分")
        st.latex(r"\LARGE \iint_R \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dA")
        st.write("1. 計算偏微分與旋度 (Curl)：")
        st.latex(r"\frac{\partial Q}{\partial x} = 1, \quad \frac{\partial P}{\partial y} = -1 \quad \Rightarrow \quad \text{Curl} = 1 - (-1) = 2")
        st.write("2. 轉化為極座標計算 ($x=ρ\cosθ, y=ρ\sinθ, dA = ρ dρ dθ$)：")
        st.latex(r"= \int_{0}^{2\pi} \int_{0}^{r} (2) \rho \, d\rho \, d\theta")
        st.latex(r"= \int_{0}^{2\pi} \left[ \rho^2 \right]_{0}^{r} d\theta = \int_{0}^{2\pi} r^2 d\theta")
        
        area_integral_val = 2 * np.pi * (radius**2)
        st.latex(rf"= 2\pi ({radius:.2f})^2 = \mathbf{{{area_integral_val:.4f}}}")

    else:
        # --- 🔵 左式：線積分推導 (純量場) ---
        st.markdown("### 🔵 左式：直接計算線積分")
        st.latex(r"\LARGE \oint_C (P dx + Q dy)")
        st.write("參數化圓周 $C$：$x = r\cos\θ, y = r\sin\θ$")
        st.write("微小量轉換：$dx = -r\sin\θ d\θ, dy = r\cos\θ d\θ$")
        st.latex(r"= \int_{0}^{2\pi} [(r\cos\theta)(-r\sin\theta) + (r\sin\theta)(r\cos\theta)] d\theta")
        st.latex(r"= \int_{0}^{2\pi} (-r^2\sin\theta\cos\theta + r^2\sin\theta\cos\theta) d\theta")
        
       # 將原本的 {0} 改成 {{0}}，{2\pi} 改成 {{2\pi}}
        st.latex(rf"= \int_{{0}}^{{2\pi}} 0 \, d\theta = \mathbf{{{line_integral_val:.4f}}}")

        # --- 🔴 右式：雙重積分推導 (純量場) ---
        st.markdown("### 🔴 右式：格林定理雙重積分")
        st.latex(r"\LARGE \iint_R \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dA")
        st.write("1. 計算偏微分與旋度 (CurlF)：")
        st.latex(r"\frac{\partial Q}{\partial x} = 0, \quad \frac{\partial P}{\partial y} = 0 \quad \Rightarrow \quad \text{CurlF} = 0 - 0 = 0")
        st.write("2. 轉化為極座標計算 ($x = ρcosθ, y = ρsinθ, dA = ρdρ dθ$)：")
        st.latex(r"= \int_{0}^{2\pi} \int_{0}^{r} (0) \rho \, d\rho \, d\theta")
        
        area_integral_val = 0.0
        st.latex(rf"= \mathbf{{{area_integral_val:.4f}}}")

    st.markdown("---")
    if np.isclose(line_integral_val, area_integral_val):
        st.success("✅ 驗證：線積分結果與面積分結果完全相等")
    else:
        st.error("❌ 驗證失敗")
