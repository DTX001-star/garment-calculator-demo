import streamlit as st

st.title('🧥 Ứng dụng Demo tính tài nguyên may mặc')

st.header('Nhập thông tin sản xuất hàng may mặc:')
so_luong = st.number_input('Số lượng sản phẩm:', min_value=1, value=50, step=1)
vai_m = st.number_input('Vải cho mỗi sản phẩm (mét):', min_value=0.1, value=1.5, step=0.1)
chi_m = st.number_input('Chỉ cho mỗi sản phẩm (mét):', min_value=1.0, value=30.0, step=1.0)
nut_cai = st.number_input('Nút cho mỗi sản phẩm (cái):', min_value=0, value=4, step=1)
gio_cong = st.number_input('Giờ công cho mỗi sản phẩm:', min_value=0.1, value=0.3, step=0.1)

tong_vai = so_luong * vai_m
tong_chi = so_luong * chi_m
tong_nut = so_luong * nut_cai
tong_gio_cong = so_luong * gio_cong

st.header('🔖 Tổng hợp tài nguyên cần thiết:')
st.write(f"**Tổng số lượng sản phẩm:** {so_luong} cái")
st.write(f"**Tổng lượng vải cần dùng:** {tong_vai:.2f} mét")
st.write(f"**Tổng lượng chỉ cần dùng:** {tong_chi:.2f} mét")
st.write(f"**Tổng số nút cần dùng:** {tong_nut} cái")
st.write(f"**Tổng giờ công lao động:** {tong_gio_cong:.2f} giờ")
