import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath, QRegion, QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame

class RoundedCornerWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Load the custom font
        self.load_custom_font()

        # Remove the window frame and make it frameless
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set window size
        self.resize(1200, 700)

        # Create a main layout (horizontal layout to include sidebar + main content)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === Sidebar Layout ===
        self.sidebar = QWidget(self)
        self.sidebar.setFixedWidth(100)
        self.sidebar.setStyleSheet("background-color: #e5e5e5;")  # Sidebar background color (dark)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(20)

        # Sidebar Title (Label)
        sidebar_title = QLabel("Menu")
        sidebar_title.setStyleSheet("background-color: #e5e5e5; font-size: 18px; font-weight: bold;")
        sidebar_title.setAlignment(Qt.AlignCenter)
        sidebar_title.setFont(self.custom_font)
        sidebar_layout.addWidget(sidebar_title)

        # Sidebar Buttons
        button_style = """
            QPushButton {
                background-color: #cdcdcd;
                color: black;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #9f9f9f;
            }
        """
        logout_button_style = """
                    QPushButton {
                        background-color: #cdcdcd;
                        color: #b73535;
                        font-weight: bold;
                        border-radius: 10px;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: #9f9f9f;
                    }
                """

        # Add some sidebar buttons
        btn1 = QPushButton("Customers")
        btn1.setStyleSheet(button_style)
        btn1.setFont(self.custom_font)
        sidebar_layout.addWidget(btn1)

        btn2 = QPushButton("Scripts")
        btn2.setStyleSheet(button_style)
        btn2.setFont(self.custom_font)
        sidebar_layout.addWidget(btn2)

        btn3 = QPushButton("Wallet")
        btn3.setStyleSheet(button_style)
        btn3.setFont(self.custom_font)
        sidebar_layout.addWidget(btn3)

        btn4 = QPushButton("Logout")
        btn4.setStyleSheet(logout_button_style)
        btn4.setFont(self.custom_font)
        sidebar_layout.addWidget(btn4)

        # Add sidebar layout to the sidebar widget
        self.sidebar.setLayout(sidebar_layout)

        # Add the sidebar to the main layout
        main_layout.addWidget(self.sidebar)

        # === Main Content Layout ===
        main_content_layout = QVBoxLayout()
        main_content_layout.setContentsMargins(0, 0, 0, 0)

        # Create a custom top bar
        self.top_bar = QWidget(self)
        self.top_bar.setFixedHeight(40)
        self.top_bar.setStyleSheet("background-color: #e5e5e5;")  # Same color as sidebar

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(10, 0, 10, 0)
        top_bar_layout.setSpacing(10)

        # Add a label in the top bar as a placeholder for a window title
        self.title_label = QLabel("AID Manager")
        self.title_label.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        self.title_label.setFont(self.custom_font)
        top_bar_layout.addWidget(self.title_label)

        # Add spacer to push buttons to the right
        top_bar_layout.addStretch()

        # Add close button
        self.close_button = QPushButton('X')
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet(
            "background-color: #e74c3c; color: white; border-radius: 10px; font-weight: bold;")
        self.close_button.clicked.connect(self.close)
        self.close_button.setFont(self.custom_font)
        # Add Settings button
        self.sttng_button = QPushButton('@')
        self.sttng_button.setFixedSize(20, 20)
        self.sttng_button.setStyleSheet(
            "background-color: #6fa8dc; color: white; border-radius: 10px; font-weight: bold;")
        self.sttng_button.clicked.connect(self.close) #It is the same as close for now
        self.sttng_button.setFont(self.custom_font)
        # Add the close button to the top bar
        top_bar_layout.addWidget(self.sttng_button)
        top_bar_layout.addWidget(self.close_button)

        # Set the layout for the top bar
        self.top_bar.setLayout(top_bar_layout)

        # Add the top bar to the main content layout
        main_content_layout.addWidget(self.top_bar)

        # Create the main content widget (blank space for now)
        self.main_content = QWidget(self)
        self.main_content.setStyleSheet("background-color: white;")
        main_content_layout.addWidget(self.main_content)
        # Set a layout for the main content widget
        self.main_content_layout = QVBoxLayout(self.main_content)
        self.main_content_layout.setAlignment(Qt.AlignCenter)

        # Add the "Welcome User" text to the main content
        welcome_label = QLabel("Welcome User!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 110px; font-weight: black; color: #333;")
        welcome_label.setFont(self.custom_font)
        self.main_content_layout.addWidget(welcome_label)

        # Add main content layout to the main layout
        main_layout.addLayout(main_content_layout)

        # Set the main layout for the window
        self.setLayout(main_layout)

        # Set rounded corners for the window
        self.set_rounded_corners()

        btn1.clicked.connect(lambda: self.switch_page(self.create_customers_page()))
        btn2.clicked.connect(lambda: self.switch_page(self.create_scripts_page()))
        btn3.clicked.connect(lambda: self.switch_page(self.create_wallet_page()))

    def load_custom_font(self):
        # Load the custom font
        font_id = QFontDatabase.addApplicationFont("Figtree.ttf")  # Provide the path to your font file
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.custom_font = QFont(font_family)
    def set_rounded_corners(self):
        # Define the radius for the rounded corners
        radius = 20  # Change this value to make the corners more or less rounded

        # Create a rectangular painter path with rounded corners
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), radius, radius)

        # Apply the rounded mask to the window
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def mousePressEvent(self, event):
        # Enable dragging by clicking the top bar
        if event.button() == Qt.LeftButton:
            if event.pos().y() < self.top_bar.height():  # Only allow dragging from the top bar
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        # Drag window only when the mouse is within the top bar
        if event.buttons() == Qt.LeftButton and event.pos().y() < self.top_bar.height():
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    # Page creation methods
    def create_customers_page(self):
        label = QLabel("Customers Page")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        label.setFont(self.custom_font)
        return label

    def create_scripts_page(self):
        label = QLabel("Scripts Page")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        label.setFont(self.custom_font)
        return label

    def create_wallet_page(self):
        label = QLabel("Wallet Page")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        label.setFont(self.custom_font)
        return label

    def switch_page(self, page_content):
        # Clear the current layout
        for i in reversed(range(self.main_content_layout.count())):
            widget = self.main_content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add the new page content
        self.main_content_layout.addWidget(page_content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoundedCornerWindow()
    window.show()
    sys.exit(app.exec_())
