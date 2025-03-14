import streamlit as st
import sqlite3
import datetime

# Thiết lập tiêu đề App
st.set_page_config(page_title="Quản Lý May Mặc", layout="centered")

# Kết nối và khởi tạo database SQLite
def get_db_connection():
    conn = sqlite3.connect('quanly_maymac.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nguyen_lieu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT NOT NULL,
        so_luong INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS don_hang (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        san_pham TEXT NOT NULL,
        so_luong INTEGER NOT NULL,
        cong_mot_sp INTEGER NOT NULL,
        han_hoan_thanh TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# ===============================
# QUẢN LÝ NGUYÊN LIỆU
# ===============================
def quan_ly_nguyen_lieu():
    st.header("📦 Quản lý nguyên liệu")

    conn = get_db_connection()
    materials = conn.execute("SELECT * FROM nguyen_lieu").fetchall()

    # Hiển thị danh sách nguyên liệu
    st.subheader("Danh sách nguyên liệu hiện có")
    if materials:
        for material in materials:
            st.text(f"👉 {material['ten']} - {material['so_luong']} cái")
    else:
        st.info("Chưa có nguyên liệu nào.")

    st.subheader("➕ Thêm nguyên liệu mới")
    ten = st.text_input("Tên nguyên liệu")
    so_luong = st.number_input("Số lượng", min_value=1, step=1)

    if st.button("Thêm nguyên liệu"):
        if ten:
            conn.execute("INSERT INTO nguyen_lieu (ten, so_luong) VALUES (?, ?)", (ten, so_luong))
            conn.commit()
            st.success(f"✅ Đã thêm nguyên liệu '{ten}' với số lượng {so_luong}")
            st.experimental_rerun()
        else:
            st.warning("⚠️ Nhập tên nguyên liệu trước khi thêm.")

    conn.close()

# ===============================
# QUẢN LÝ ĐƠN HÀNG
# ===============================
def quan_ly_don_hang():
    st.header("📝 Quản lý đơn hàng")

    conn = get_db_connection()
    orders = conn.execute("SELECT * FROM don_hang").fetchall()

    st.subheader("Danh sách đơn hàng hiện có")
    if orders:
        for order in orders:
            st.text(f"👉 {order['san_pham']} | SL: {order['so_luong']} | Hạn: {order['han_hoan_thanh']}")
    else:
        st.info("Chưa có đơn hàng nào.")

    st.subheader("➕ Thêm đơn hàng mới")
    san_pham = st.text_input("Tên sản phẩm")
    so_luong = st.number_input("Số lượng cần sản xuất", min_value=1, step=1)
    cong_mot_sp = st.number_input("Số công cho 1 sản phẩm", min_value=1, step=1)
    han_hoan_thanh = st.date_input("Hạn hoàn thành", min_value=datetime.date.today())

    if st.button("Thêm đơn hàng"):
        if san_pham:
            conn.execute('''
                INSERT INTO don_hang (san_pham, so_luong, cong_mot_sp, han_hoan_thanh) 
                VALUES (?, ?, ?, ?)''',
                (san_pham, so_luong, cong_mot_sp, han_hoan_thanh.strftime("%Y-%m-%d"))
            )
            conn.commit()
            st.success(f"✅ Đã thêm đơn hàng '{san_pham}' với SL {so_luong}")
            st.experimental_rerun()
        else:
            st.warning("⚠️ Nhập tên sản phẩm trước khi thêm.")

    conn.close()

# ===============================
# TÍNH TOÁN SẢN XUẤT
# ===============================
def tinh_toan_san_xuat():
    st.header("📊 Tính toán khả năng hoàn thành đơn hàng")

    conn = get_db_connection()
    orders = conn.execute("SELECT * FROM don_hang").fetchall()

    if not orders:
        st.info("Không có đơn hàng để tính toán.")
        return

    order_list = [f"{o['id']} - {o['san_pham']}" for o in orders]
    selected_order = st.selectbox("Chọn đơn hàng", order_list)

    order_id = int(selected_order.split(" - ")[0])
    order = conn.execute("SELECT * FROM don_hang WHERE id = ?", (order_id,)).fetchone()

    nhan_cong = st.number_input("Số lượng nhân công", min_value=1, step=1)
    gio_lam_ngay = st.number_input("Số giờ làm/ngày", min_value=1, step=1)

    if st.button("Tính toán"):
        so_luong = order['so_luong']
        cong_mot_sp = order['cong_mot_sp']
        han_hoan_thanh = order['han_hoan_thanh']

        tong_cong = so_luong * cong_mot_sp
        gio_mot_ngay = nhan_cong * gio_lam_ngay
        so_ngay_can = tong_cong / gio_mot_ngay

        ngay_hien_tai = datetime.date.today()
        han_date = datetime.datetime.strptime(han_hoan_thanh, "%Y-%m-%d").date()
        ngay_con_lai = (han_date - ngay_hien_tai).days

        st.subheader("📈 Kết quả tính toán")
        st.write(f"✅ Tổng công cần: **{tong_cong} công (giờ)**")
        st.write(f"✅ Số công/ngày có thể làm: **{gio_mot_ngay} công/ngày**")
        st.write(f"✅ Sẽ cần khoảng **{so_ngay_can:.2f} ngày** để hoàn thành.")

        if so_ngay_can <= ngay_con_lai:
            st.success(f"🎉 Đủ thời gian để hoàn thành. Còn {ngay_con_lai} ngày.")
        else:
            st.error(f"⚠️ Không đủ thời gian! Cần thêm nhân công hoặc tăng giờ làm.")
            st.write(f"Cần ít nhất **{so_ngay_can - ngay_con_lai:.2f} ngày** bổ sung.")

    conn.close()

# ===============================
# MAIN MENU
# ===============================
def main():
    st.title("🧵 HỆ THỐNG QUẢN LÝ MAY MẶC")

    menu = ["🏠 Trang chính", "📦 Quản lý nguyên liệu", "📝 Quản lý đơn hàng", "📊 Tính toán sản xuất"]
    choice = st.sidebar.selectbox("Chọn chức năng", menu)

    if choice == "🏠 Trang chính":
        st.subheader("Chào mừng đến hệ thống quản lý may mặc 👋")
        st.image("https://img.freepik.com/free-photo/fashion-designer-making-sketches_23-2148528880.jpg", use_column_width=True)
        st.markdown("""
        #### Các tính năng chính:
        - Quản lý nguyên liệu tồn kho
        - Quản lý đơn hàng, sản phẩm cần sản xuất
        - Tính toán tiến độ hoàn thành sản phẩm dựa vào nhân công và thời gian
        """)
    elif choice == "📦 Quản lý nguyên liệu":
        quan_ly_nguyen_lieu()
    elif choice == "📝 Quản lý đơn hàng":
        quan_ly_don_hang()
    elif choice == "📊 Tính toán sản xuất":
        tinh_toan_san_xuat()

if __name__ == '__main__':
    main()
