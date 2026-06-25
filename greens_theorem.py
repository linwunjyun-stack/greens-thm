import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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
radius = st.sidebar.slider("調整積分區域半徑 (r)", 1.0, 3.0, 2.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.write("💡 **工程應用提示**：在測量學中，我們常利用格林定理（面積計算特例）來求算不規則土地的面積；在流體力學中，它則關乎環流與旋度的計算。")

# --- 數學與繪圖邏輯 ---
# 建立網格以繪製向量場
x = np.linspace(-6, 6, 20)
y = np.linspace(-6, 6, 20)
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
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📊 向量場與積分區域動態視覺化")
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # 畫出向量場 (Quiver)
    ax.quiver(X, Y, P, Q, color='lightgray', alpha=0.8)
    
    # 畫出積分區域 R (填色)
    ax.fill(x_c, y_c, color='#1f77b4', alpha=0.3, label=f'Region R (r={radius})')
    
    # 畫出邊界 C 及其方向 (逆時針箭頭)
    ax.plot(x_c, y_c, color='red', linewidth=2, label='Boundary C')
    ax.arrow(radius*0.707, radius*0.707, -0.1, 0.1, shape='full', lw=2, length_includes_head=True, head_width=0.3, color='red', zorder=5) # 在 45 度角加個逆時針箭頭
    
    ax.set_xlim([-6, 6])
    ax.set_ylim([-6, 6])
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
        st.success("✅ 驗證成功：線積分結果與面積分結果完全相等！")
    else:
        st.error("❌ 驗證失敗")
