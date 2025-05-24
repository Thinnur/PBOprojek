from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os  # Tambahkan ini untuk mengatasi error "os is not defined"

def load_stylesheet(filename):
    """Load stylesheet from CSS file dengan error handling yang lebih baik"""
    try:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        css_path = os.path.join(base_path, 'styles', filename)
        
        # Debug untuk tracking error
        print(f"Loading CSS from: {css_path}")
        
        # Cek apakah file ada
        if not os.path.exists(css_path):
            print(f"ERROR: File CSS tidak ditemukan: {css_path}")
            return ""
            
        with open(css_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"CSS berhasil dimuat ({len(content)} characters)")
            return content
    except Exception as e:
        print(f"Error loading stylesheet {filename}: {e}")
        return ""

class ModernButton(QPushButton):
    def __init__(self, text, color):
        super().__init__()
        self.setText(text)
        self.setMinimumHeight(50)
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 {self._darken_color(color)});
                border: none;
                border-radius: 8px;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self._darken_color(color)}, stop:1 {color});
            }}
        """)
    
    def _darken_color(self, color):
        color = QColor(color)
        h = color.hue()
        s = color.saturation()
        v = int(color.value() * 0.8)
        return QColor.fromHsv(h, s, v).name()

class KeuanganView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Pengelolaan Keuangan")
        self.setGeometry(100, 100, 1000, 600)
        
        try:
            # Load semua style sheet di satu tempat
            self.main_css = load_stylesheet("main.css") 
            self.buttons_css = load_stylesheet("buttons.css")
            self.forms_css = load_stylesheet("forms.css")
            self.tables_css = load_stylesheet("tables.css")
            self.sidebar_css = load_stylesheet("sidebar.css")
            self.riwayat_css = load_stylesheet("riwayat.css")
            
            # Terapkan style global
            self.setStyleSheet(self.main_css)
            print("Semua CSS berhasil dimuat")
        except Exception as e:
            print(f"Error loading CSS: {e}")
        
        # Main container
        self.main_container = QStackedWidget()
        self.setCentralWidget(self.main_container)
        
        # ===== HOME VIEW (CENTER MENU) =====
        self.home_widget = QWidget()
        home_layout = QVBoxLayout(self.home_widget)
        home_layout.setContentsMargins(20, 20, 20, 20)
        home_layout.setSpacing(20)

        # Header for home view
        header = QLabel("Sistem Pengelolaan Keuangan")
        header.setProperty("class", "header")

        home_layout.addWidget(header, alignment=Qt.AlignCenter)  # Tambahkan header ke layout

        # Add spacing
        home_layout.addSpacing(30)
        
        # Button style for home using external CSS
        button_style = load_stylesheet("buttons.css")
        
        # Create buttons dengan class selector
        self.home_tambah_btn = QPushButton("Tambah Transaksi")
        self.home_tambah_btn.setObjectName("button-tambah")

        self.home_saldo_btn = QPushButton("Lihat Saldo") 
        self.home_saldo_btn.setObjectName("button-saldo")

        self.home_riwayat_btn = QPushButton("Riwayat Transaksi")
        self.home_riwayat_btn.setObjectName("button-riwayat")

        # === HOME VIEW - Add Exit button ===
        self.home_keluar_btn = QPushButton("Keluar")
        self.home_keluar_btn.setObjectName("button-keluar")
        
        # Tambahkan class selector
        self.home_tambah_btn.setProperty("class", "button-tambah")
        self.home_saldo_btn.setProperty("class", "button-saldo")
        self.home_riwayat_btn.setProperty("class", "button-riwayat")
        self.home_keluar_btn.setProperty("class", "button-keluar")

        # Apply button CSS
        button_css = self.buttons_css  # Gunakan yang sudah dimuat
        self.home_tambah_btn.setStyleSheet(button_css)
        self.home_saldo_btn.setStyleSheet(button_css)
        self.home_riwayat_btn.setStyleSheet(button_css)
        self.home_keluar_btn.setStyleSheet(button_css)
        
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(15)
        button_layout.addWidget(self.home_tambah_btn, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.home_saldo_btn, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.home_riwayat_btn, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.home_keluar_btn, alignment=Qt.AlignCenter)
        
        home_layout.addWidget(button_container)
        home_layout.addStretch()
        
        # ===== DETAIL VIEW (SPLIT VIEW) =====
        self.detail_widget = QWidget()
        detail_layout = QHBoxLayout(self.detail_widget)
        detail_layout.setContentsMargins(0, 0, 0, 0)
        detail_layout.setSpacing(0)
        
        # Create hamburger menu container that stays visible
        self.menu_toggle_container = QWidget()
        self.menu_toggle_container.setFixedWidth(50)
        self.menu_toggle_container.setProperty("class", "menu-toggle")

        menu_toggle_layout = QVBoxLayout(self.menu_toggle_container)
        menu_toggle_layout.setContentsMargins(10, 20, 10, 10)
        menu_toggle_layout.setAlignment(Qt.AlignTop)
        
        # Create hamburger toggle button
        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(30, 30)
        
        # Create hamburger icon
        icon_pixmap = QPixmap(30, 30)
        icon_pixmap.fill(Qt.transparent)
        painter = QPainter(icon_pixmap)
        painter.setPen(QPen(QColor("white"), 2))
        
        # Draw three lines for hamburger icon
        painter.drawLine(5, 8, 25, 8)
        painter.drawLine(5, 15, 25, 15)
        painter.drawLine(5, 22, 25, 22)
        painter.end()
        
        self.toggle_btn.setIcon(QIcon(icon_pixmap))
        self.toggle_btn.setIconSize(QSize(20, 20))
        
        # Update hamburger button style to match the image (darker background)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #0A0908;
                border: none;
            }
            QPushButton:hover {
                background-color: #1A1918;
                border-radius: 4px;
            }
        """)
        menu_toggle_layout.addWidget(self.toggle_btn)
        
        # Update menu toggle container background to match dark theme
        self.menu_toggle_container.setStyleSheet("""
            QWidget {
                background-color: #0A0908;
            }
        """)
        
        # Left sidebar for menu with added border
        self.sidebar = QScrollArea()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setProperty("class", "sidebar")
        self.sidebar.setStyleSheet("""
            QScrollArea.sidebar {
                background-color: #EDEAE5;
                border-right: 10px solid #C6AC8F;
            }
        """)
        
        # Buat widget untuk konten sidebar
        sidebar_content = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_content)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)  # Kurangi spacing agar muat
        
        # Header for sidebar
        sidebar_header = QLabel("Sistem Pengelolaan\nKeuangan")
        sidebar_header.setStyleSheet("""
            QLabel {
                color: #0A0908;
                font-size: 24px;
                font-weight: bold;
                padding: 10px 0;  /* Kurangi padding */
            }
        """)
        sidebar_layout.addWidget(sidebar_header)
        
        # Kurangi spacing
        sidebar_layout.addSpacing(15)  # Dari 30 menjadi 15
        
        # Button style specifically for sidebar - PERBAIKAN STYLE
        sidebar_button_style = """
            QPushButton {
                background-color: %s;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-width: 200px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: %s;
                opacity: 0.8;
            }
        """
        
        # Create sidebar buttons with shorter style - PERUBAHAN WARNA
        self.tambah_btn = QPushButton("Tambah Transaksi")
        self.tambah_btn.setStyleSheet(sidebar_button_style % ("#EAE0D5", "#D4CFC4"))  # Ubah ke warna cream/beige
        
        self.saldo_btn = QPushButton("Lihat Saldo") 
        self.saldo_btn.setStyleSheet(sidebar_button_style % ("#C6AC8F", "#B59A7F"))  # Ubah ke warna tan/brown
        
        self.riwayat_btn = QPushButton("Riwayat Transaksi")
        self.riwayat_btn.setStyleSheet(sidebar_button_style % ("#5E503F", "#4E3B2B"))  # Ubah ke warna dark brown
        
        # Add exit button to sidebar with dark blue-gray color
        self.keluar_btn = QPushButton("Keluar")
        self.keluar_btn.setStyleSheet(sidebar_button_style % ("#22333B", "#1E2A30"))  # Ubah ke warna dark blue-gray
        
        # Add buttons to sidebar layout - PASTIKAN KODE INI ADA
        sidebar_layout.addWidget(self.tambah_btn)
        sidebar_layout.addWidget(self.saldo_btn)
        sidebar_layout.addWidget(self.riwayat_btn)
        sidebar_layout.addStretch()  # Menambah ruang kosong di antara tombol menu dan tombol keluar
        
        # Gunakan self.keluar_btn yang sudah dideklarasikan sebelumnya
        sidebar_layout.addWidget(self.keluar_btn)
        
        # Set widget ke scroll area
        self.sidebar.setWidget(sidebar_content)
        self.sidebar.setWidgetResizable(True)  # Penting! Agar widget bisa resize
        
        # Atur ukuran minimum content
        sidebar_content.setMinimumHeight(500)  # Pastikan tinggi minimum cukup
        
        # Connect buttons to their respective functions
        self.tambah_btn.clicked.connect(self.on_tambah_clicked)
        self.saldo_btn.clicked.connect(self.on_saldo_clicked)
        self.riwayat_btn.clicked.connect(self.on_riwayat_clicked)
        self.keluar_btn.clicked.connect(QApplication.instance().quit)
        
        # Content area on the right
        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Stacked widget for different content views
        self.content_area = QStackedWidget()
        content_layout.addWidget(self.content_area)
        
        # Add widgets to detail layout
        detail_layout.addWidget(self.menu_toggle_container)
        detail_layout.addWidget(self.sidebar)
        detail_layout.addWidget(self.content_container, 1)  # Content takes remaining space
        
        # Sidebar visibility state
        self.sidebar_visible = True
        
        # Connect toggle button
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        
        # Add both views to main container
        self.main_container.addWidget(self.home_widget)
        self.main_container.addWidget(self.detail_widget)
        
        # Initialize callbacks
        self.tambah_transaksi_callback = None
        self.lihat_saldo_callback = None
        self.lihat_transaksi_callback = None
        
        # Connect signals for both home and detail views
        self.home_tambah_btn.clicked.connect(lambda: self.on_menu_clicked(0))
        self.home_saldo_btn.clicked.connect(lambda: self.on_menu_clicked(1))
        self.home_riwayat_btn.clicked.connect(lambda: self.on_menu_clicked(2))
        
        self.tambah_btn.clicked.connect(self.on_tambah_clicked)
        self.saldo_btn.clicked.connect(self.on_saldo_clicked)
        self.riwayat_btn.clicked.connect(self.on_riwayat_clicked)
        
        # Connect exit buttons
        self.home_keluar_btn.clicked.connect(self.close)
        self.keluar_btn.clicked.connect(self.close)
        
        # Show home view initially
        self.main_container.setCurrentIndex(0)

    def on_menu_clicked(self, button_index):
        # Switch to detail view
        self.main_container.setCurrentWidget(self.detail_widget)
        
        # Execute corresponding function
        if button_index == 0:
            self.on_tambah_clicked()
        elif button_index == 1:
            self.on_saldo_clicked()
        elif button_index == 2:
            self.on_riwayat_clicked()
            
    def set_callbacks(self, tambah_transaksi, lihat_saldo, lihat_transaksi):
        self.tambah_transaksi_callback = tambah_transaksi
        self.lihat_saldo_callback = lihat_saldo
        self.lihat_transaksi_callback = lihat_transaksi

    def on_tambah_clicked(self):
        self.show_form_transaksi()

    def on_saldo_clicked(self):
        if self.lihat_saldo_callback:
            data = self.lihat_saldo_callback()
            self.show_saldo(data)

    def on_riwayat_clicked(self):
        self.show_riwayat()

    def show_form_transaksi(self):
        form = QWidget()
        layout = QFormLayout(form)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Form fields
        jenis = QComboBox()
        jenis.addItems(["Tunai", "Bank", "Dompet-Digital"])
        jenis.setCurrentText("Tunai")
        
        tipe = QComboBox()
        tipe.addItems(["masuk", "keluar"])
        tipe.setCurrentText("masuk")
        
        jumlah = QLineEdit()
        keterangan = QLineEdit()

        # Set properties untuk penggunaan CSS yang lebih baik
        form.setProperty("class", "form-container")
        submit = QPushButton("Simpan")
        submit.setProperty("class", "form-button")
        
        # Terapkan CSS baru
        form_style = self.forms_css  # Gunakan CSS yang sudah dimuat
        form.setStyleSheet(form_style)
        
        layout.addRow("Jenis Penyimpanan:", jenis)
        layout.addRow("Tipe Transaksi:", tipe)
        layout.addRow("Jumlah:", jumlah)
        layout.addRow("Keterangan:", keterangan)

        def on_submit():
            try:
                amount_text = jumlah.text().replace(',', '').replace('.', '')
                if not amount_text:
                    raise ValueError("Jumlah harus diisi!")
                amount = float(amount_text)
                
                result = self.tambah_transaksi_callback(
                    jenis.currentText(),
                    amount,
                    tipe.currentText(),
                    keterangan.text()
                )
                
                if result:
                    QMessageBox.information(self, "Sukses", "Transaksi berhasil ditambahkan!")
                    self.on_saldo_clicked()
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))

        # Submit button with updated style
        submit = QPushButton("Simpan")
        layout.addRow("", submit)
        submit.clicked.connect(on_submit)

        # Clear and set new content
        while self.content_area.count():
            self.content_area.removeWidget(self.content_area.widget(0))
        self.content_area.addWidget(form)

    def show_saldo(self, data):
        """Display saldo information in a table"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create table
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Jenis Penyimpanan", "Saldo"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Apply CSS using class property
        table.setProperty("class", "table-saldo")
        table.setStyleSheet(load_stylesheet("tables.css"))
        
        # Add data to table
        total = 0
        table.setRowCount(len(data))
        for row, (nama, saldo) in enumerate(data):
            # Jenis Penyimpanan
            nama_item = QTableWidgetItem(nama)
            table.setItem(row, 0, nama_item)
            
            # Saldo with formatting
            saldo_text = f"Rp {saldo:,.2f}"
            saldo_item = QTableWidgetItem(saldo_text)
            saldo_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            table.setItem(row, 1, saldo_item)
            
            total += saldo

        layout.addWidget(table)

        # Add total saldo
        total_label = QLabel(f"Total Saldo: Rp {total:,.2f}")
        total_label.setStyleSheet("""
            color: #5E503F;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(total_label, alignment=Qt.AlignRight)

        # Set as current widget
        while self.content_area.count():
            self.content_area.removeWidget(self.content_area.widget(0))
        self.content_area.addWidget(widget)

    def show_riwayat(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Label and ComboBox
        label = QLabel("Pilih Jenis Penyimpanan:")
        label.setProperty("class", "riwayat-label")
        
        combo = QComboBox()
        combo.addItems(["Tunai", "Bank", "Dompet-Digital"])
        combo.setProperty("class", "riwayat-combo")
        
        # Create table with correct columns
        table = QTableWidget()  # Pastikan table didefinisikan sebelum digunakan
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Tanggal", "Tipe", "Jumlah", "Keterangan"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Apply CSS using class property
        table.setProperty("class", "table-riwayat")
        
        # Load external CSS (gunakan self.tables_css yang sudah dimuat di __init__)
        label.setStyleSheet(self.riwayat_css)
        combo.setStyleSheet(self.riwayat_css)
        table.setStyleSheet(self.tables_css)  

        layout.addWidget(label)
        layout.addWidget(combo)
        layout.addWidget(table)
        
        def update_table(storage_type):
            try:
                if self.lihat_transaksi_callback:
                    data = self.lihat_transaksi_callback(storage_type)
                    if data:
                        # Filter empty rows and parse data
                        rows = [row.split('|') for row in data.strip().split('\n') if row.strip()]
                        
                        # Set table row count
                        table.setRowCount(len(rows))
                        
                        for i, row in enumerate(rows):
                            # Tanggal
                            table.setItem(i, 0, QTableWidgetItem(row[0].strip()))
                            
                            # Tipe with color
                            tipe_item = QTableWidgetItem(row[1].strip())
                            if row[1].strip() == "masuk":
                                tipe_item.setForeground(QColor("#22c55e"))
                            else:
                                tipe_item.setForeground(QColor("#ef4444"))
                            table.setItem(i, 1, tipe_item)
                            
                            # Jumlah - Parse amount correctly
                            jumlah_str = row[2].strip()
                            jumlah_item = QTableWidgetItem(jumlah_str)
                            jumlah_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                            table.setItem(i, 2, jumlah_item)
                            
                            # Keterangan
                            table.setItem(i, 3, QTableWidgetItem(row[3].strip()))

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

        combo.currentTextChanged.connect(update_table)
        
        # Initial load
        if combo.count() > 0:
            combo.setCurrentIndex(0)
            update_table(combo.currentText())

        # Set as current widget
        while self.content_area.count():
            self.content_area.removeWidget(self.content_area.widget(0))
        self.content_area.addWidget(widget)
    
    # Add toggle sidebar method
    def toggle_sidebar(self):
        if self.sidebar_visible:
            # Hide sidebar
            self.sidebar.hide()
            self.sidebar_visible = False
        else:
            # Show sidebar
            self.sidebar.show()
            self.sidebar_visible = True