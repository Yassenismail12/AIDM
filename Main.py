import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath, QRegion, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

class RoundedCornerWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Remove the window frame and make it frameless
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set window size
        self.resize(500, 400)

        # Create a layout to manage the top bar and main window content
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a custom top bar with a slightly different background color
        self.top_bar = QWidget(self)
        self.top_bar.setFixedHeight(40)
        self.top_bar.setStyleSheet("background-color: #eeeeee;")  # Dark background color for the top bar

        # Layout for the top bar (for window title and close/minimize buttons)
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(10, 0, 10, 0)
        top_bar_layout.setSpacing(10)

        # Add a label in the top bar as a placeholder for a window title
        self.title_label = QLabel("Custom App Window")
        self.title_label.setStyleSheet("color: white; font-size: 16px;")
        top_bar_layout.addWidget(self.title_label)

        # Add spacer to push buttons to the right
        top_bar_layout.addStretch()

        # Add close button
        self.close_button = QPushButton('X')
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet(
            "background-color: #e74c3c; color: white; border-radius: 10px; font-weight: bold;")
        self.close_button.clicked.connect(self.close)

        # Add the close button to the top bar
        top_bar_layout.addWidget(self.close_button)

        # Set the layout for the top bar
        self.top_bar.setLayout(top_bar_layout)

        # Add the top bar to the main layout
        layout.addWidget(self.top_bar)

        # Create the main content widget (could be anything, here it's just a blank space)
        self.main_content = QWidget(self)
        self.main_content.setStyleSheet("background-color: white;")
        layout.addWidget(self.main_content)

        # Set the main layout for the window
        self.setLayout(layout)

        # Set rounded corners for the window
        self.set_rounded_corners()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoundedCornerWindow()
    window.show()
    sys.exit(app.exec_())
