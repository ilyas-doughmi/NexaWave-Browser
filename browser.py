import sys
import os
from PyQt5.QtCore import QUrl, Qt, QSize, QPoint, QByteArray
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, 
                            QAction, QLineEdit, QProgressBar, 
                            QStatusBar, QTabWidget, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QFrame, QSplitter, 
                            QCompleter, QSpacerItem, QSizePolicy, QMenu, QDialog, QPushButton)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QPixmap, QCursor, QStandardItemModel, QImage

# Browser name and version
BROWSER_NAME = "NexaWave"
BROWSER_VERSION = "1.0"

# We'll initialize the browser icon later after QApplication is created
BROWSER_ICON = None

# Path to the logo file
LOGO_PATH = "nexawave_logo.png"

class UrlBar(QLineEdit):
    """Custom URL bar with rounded corners and better styling"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Apply styling
        self.setPlaceholderText("Search or enter website name")
        self.setStyleSheet("""
            QLineEdit {
                background-color: #f8f9fa;
                border: 1px solid #e2e8f0;
                border-radius: 24px;
                padding: 10px 18px;
                selection-background-color: #2563eb;
                font-size: 14px;
                color: #1e293b;
                min-height: 26px;
                margin: 4px 0px;
            }
            QLineEdit:focus {
                border: 1.5px solid #3b82f6;
                background-color: white;
            }
        """)

class TabBar(QTabWidget):
    """Custom tab widget with improved styling"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setElideMode(Qt.ElideRight)
        self.setStyleSheet("""
            QTabWidget::pane {
                border-top: 1px solid #e2e8f0;
                background: white;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background: #f8f9fa;
                border: 1px solid #e2e8f0;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 10px 16px;
                margin-right: 3px;
                color: #64748b;
                font-size: 13px;
                min-width: 140px;
                max-width: 220px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: none;
                border-top: 2.5px solid #3b82f6;
                color: #1e293b;
                font-weight: 600;
            }
            QTabBar::tab:hover:!selected {
                background: #f1f5f9;
            }
            QTabBar::close-button {
                image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSIjNjQ3NDhiIiBkPSJNMTkgNi40MUwxNy41OSA1IDEyIDEwLjU5IDYuNDEgNSA1IDYuNDEgMTAuNTkgMTIgNSAxNy41OSA2LjQxIDE5IDEyIDEzLjQxIDE3LjU5IDE5IDE5IDE3LjU5IDEzLjQxIDEyIDE5IDYuNDF6Ii8+PC9zdmc+);
                width: 16px;
                height: 16px;
                subcontrol-position: right;
                margin-right: 4px;
            }
            QTabBar::close-button:hover {
                background: #e2e8f0;
                border-radius: 8px;
            }
        """)

class NavigationToolBar(QToolBar):
    """Custom navigation toolbar with better styling"""
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setIconSize(QSize(24, 24))
        self.setMovable(False)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setStyleSheet("""
            QToolBar {
                background-color: #f8f9fa;
                border-bottom: 1px solid #e2e8f0;
                spacing: 10px;
                padding: 8px 12px;
            }
            QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 6px;
                padding: 8px;
            }
            QToolButton:hover {
                background-color: #f1f5f9;
                border: 1px solid #e2e8f0;
            }
            QToolButton:pressed {
                background-color: #e2e8f0;
            }
        """)

class ModernProgressBar(QProgressBar):
    """A more modern progress bar"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(False)
        self.setMaximumHeight(3)
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: #3b82f6;
                border-radius: 1.5px;
            }
        """)

class ActionButton(QAction):
    """Custom action button with better styling"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        font = QFont()
        font.setPointSize(13)
        self.setFont(font)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        global BROWSER_ICON
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QStatusBar {
                background-color: #f8f9fa;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
                font-size: 12px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f5f9;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f1f5f9;
                height: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal {
                background: #cbd5e1;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QMenuBar {
                background-color: #f8f9fa;
                color: #1e293b;
                border-bottom: 1px solid #e2e8f0;
            }
            QMenuBar::item {
                background: transparent;
                padding: 8px 12px;
            }
            QMenuBar::item:selected {
                background: #e2e8f0;
                border-radius: 4px;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 30px 8px 15px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #f1f5f9;
                color: #1e293b;
            }
            QMenu::separator {
                height: 1px;
                background-color: #e2e8f0;
                margin: 6px 10px;
            }
        """)
        
        # Set window attributes
        self.setWindowTitle(f"{BROWSER_NAME} - Developed by ILYAS DOUGHMI")
        if BROWSER_ICON:
            self.setWindowIcon(BROWSER_ICON)
        self.setGeometry(100, 100, 1280, 800)
        
        # Create central widget with layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Create menu bar
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # New tab action
        new_tab_action = QAction("New Tab", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        file_menu.addAction(new_tab_action)
        
        # Close tab action
        close_tab_action = QAction("Close Tab", self)
        close_tab_action.setShortcut("Ctrl+W")
        close_tab_action.triggered.connect(lambda: self.close_tab(self.tabs.currentIndex()))
        file_menu.addAction(close_tab_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        # About action
        about_action = QAction(f"About {BROWSER_NAME}", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Create modern tab widget
        self.tabs = TabBar()
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        # Create navigation toolbar
        navbar = NavigationToolBar("Navigation")
        self.addToolBar(navbar)
        
        # Create navigation action buttons with proper icons using SVG data
        back_icon = QIcon(QPixmap.fromImage(QImage.fromData(QByteArray.fromBase64(
            b'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSIjNTA1MDUwIiBkPSJNMjAgMTFINy44M2w1LjU5LTUuNTlMMTIgNGwtOCA4IDggOCAxLjQxLTEuNDFMNy44MyAxM0gyMHYtMnoiLz48L3N2Zz4='))))
        back_btn = QAction(back_icon, "Back", self)
        back_btn.setToolTip("Back")
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)
        
        forward_icon = QIcon(QPixmap.fromImage(QImage.fromData(QByteArray.fromBase64(
            b'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSIjNTA1MDUwIiBkPSJNMTIgNGwtMS40MSAxLjQxTDE2LjE3IDExSDR2MmgxMi4xN2wtNS41OCA1LjU5TDEyIDIwbDgtOHoiLz48L3N2Zz4='))))
        forward_btn = QAction(forward_icon, "Forward", self)
        forward_btn.setToolTip("Forward")
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)
        
        reload_icon = QIcon(QPixmap.fromImage(QImage.fromData(QByteArray.fromBase64(
            b'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSIjNTA1MDUwIiBkPSJNMTcuNjUgNi4zNUMxNi4yIDQuOSAxNC4yMSA0IDEyIDRjLTQuNDIgMC03Ljk5IDMuNTgtNy45OSA4czMuNTcgOCA3Ljk5IDhjMy43MyAwIDYuODQtMi41NSA3LjczLTZoLTIuMDhjLS44MiAyLjMzLTMuMDQgNC01LjY1IDQtMy4zMSAwLTYtMi42OS02LTZzMi42OS02IDYtNmMxLjY2IDAgMy4xNC42OSA0LjIyIDEuNzhMMTMgMTFoN1Y0bC0yLjM1IDIuMzV6Ii8+PC9zdmc+'))))
        reload_btn = QAction(reload_icon, "Reload", self)
        reload_btn.setToolTip("Reload")
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)
        
        home_icon = QIcon(QPixmap.fromImage(QImage.fromData(QByteArray.fromBase64(
            b'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSIjNTA1MDUwIiBkPSJNMTAgMjB2LTZoNHY2aDV2LThoM0wxMiAzIDIgMTJoM3Y4eiIvPjwvc3ZnPg=='))))
        home_btn = QAction(home_icon, "Home", self)
        home_btn.setToolTip("Home")
        home_btn.triggered.connect(self.go_home)
        navbar.addAction(home_btn)
        
        # Add a small spacer
        spacer = QWidget()
        spacer.setFixedWidth(10)
        navbar.addWidget(spacer)
        
        # URL Bar (modern style)
        self.url_bar = UrlBar()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        # Add URL completer for better UX
        self.url_model = QStandardItemModel()
        self.url_completer = QCompleter(self.url_model, self)
        self.url_completer.setCompletionMode(QCompleter.InlineCompletion)
        self.url_bar.setCompleter(self.url_completer)
        
        navbar.addWidget(self.url_bar)
        
        # Add right-side actions
        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        navbar.addWidget(spacer2)
        
        newtab_icon = QIcon(QPixmap.fromImage(QImage.fromData(QByteArray.fromBase64(
            b'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSIjNTA1MDUwIiBkPSJNMTkgMTNoLTZ2NmgtMnYtNkg1di0yaDZWNWgydjZoNnYyeiIvPjwvc3ZnPg=='))))
        newtab_btn = QAction(newtab_icon, "New Tab", self)
        newtab_btn.setToolTip("New Tab")
        newtab_btn.triggered.connect(self.add_new_tab)
        navbar.addAction(newtab_btn)
        
        # Modern progress bar
        self.progress_bar = ModernProgressBar()
        
        # Add widgets to main layout
        layout.addWidget(navbar)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.tabs)
        
        # Status bar with modern styling
        self.status_bar = QStatusBar()
        self.status_bar.setFixedHeight(24)
        self.setStatusBar(self.status_bar)
        
        # Create first tab
        self.add_new_tab()
        
        self.show()
    
    def add_new_tab(self, url=None):
        if url is None:
            url = QUrl("https://ilyas-doughmi.vercel.app/")
        elif isinstance(url, str):
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            url = QUrl(url)
        
        # Create container widget with zero margins
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        tab.setLayout(layout)
        
        # Create browser
        browser = QWebEngineView()
        
        # Set page zoom factor for better readability
        browser.setZoomFactor(1.0)
        
        browser.setUrl(url)
        layout.addWidget(browser)
        
        # Add tab with loading title
        index = self.tabs.addTab(tab, "Loading...")
        self.tabs.setCurrentIndex(index)
        
        # Connect signals
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        browser.loadProgress.connect(self.update_progress)
        browser.loadFinished.connect(lambda _, browser=browser: self.update_title(browser))
        
        # Set focus to the web view
        browser.setFocus()
        
        return browser
    
    def current_browser(self):
        return self.tabs.currentWidget().layout().itemAt(0).widget()
    
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()
    
    def navigate_to_url(self):
        url = self.url_bar.text()
        
        # If it's a search term, send to Google
        if " " in url or not "." in url:
            url = f"https://www.google.com/search?q={url}"
        # Otherwise ensure it has http/https
        elif not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        qurl = QUrl(url)
        self.current_browser().setUrl(qurl)
        
        # Add to URL model for auto-completion
        self.url_model.insertRow(0)
        self.url_model.setData(self.url_model.index(0, 0), url)
    
    def update_url(self, url, browser=None):
        if browser == self.current_browser():
            self.url_bar.setText(url.toString())
            self.url_bar.setCursorPosition(0)
    
    def update_title(self, browser=None):
        if browser == self.current_browser():
            title = browser.page().title()
            if title:
                self.tabs.setTabText(self.tabs.currentIndex(), title)
                self.setWindowTitle(f"{title} - {BROWSER_NAME}")
            else:
                self.tabs.setTabText(self.tabs.currentIndex(), "New Tab")
                self.setWindowTitle(f"{BROWSER_NAME} - Developed by ILYAS DOUGHMI")
    
    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress == 100:
            # Hide progress bar when loading complete
            self.progress_bar.hide()
        else:
            self.progress_bar.show()
    
    def go_home(self):
        self.current_browser().setUrl(QUrl("https://ilyas-doughmi.vercel.app/"))
    
    def show_about(self):
        global BROWSER_ICON
        
        # Create about dialog with HTML content for proper formatting
        about_text = f'''
        <div style="text-align:center;">
            <h2>{BROWSER_NAME}</h2>
            <p>Version {BROWSER_VERSION}</p>
            <p>A sleek, modern web browser built with Python and PyQt5.</p>
            <p><b>Developed by: <a href="https://ilyas-doughmi.vercel.app/">ILYAS DOUGHMI</a></b></p>
            <p>&copy; 2023 - All rights reserved</p>
            <p>This browser is open source and free to use under the MIT License.</p>
        </div>
        '''
        
        # Create a dialog to display the about information
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle(f"About {BROWSER_NAME}")
        if BROWSER_ICON:
            about_dialog.setWindowIcon(BROWSER_ICON)
        about_dialog.setFixedSize(400, 300)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create label with about text
        about_label = QLabel(about_text)
        about_label.setOpenExternalLinks(True)  # Allow clicking on links
        about_label.setTextFormat(Qt.RichText)
        layout.addWidget(about_label)
        
        # Create button area
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Create close button
        close_button = QPushButton("Close")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(about_dialog.close)
        
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        about_dialog.setLayout(layout)
        
        about_dialog.exec_()


if __name__ == "__main__":
    # Set application-wide attributes for high DPI screens before creating QApplication
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    app.setApplicationName(BROWSER_NAME)
    app.setApplicationVersion(BROWSER_VERSION)
    app.setOrganizationName("ILYAS DOUGHMI")
    app.setOrganizationDomain("ilyas-doughmi.vercel.app")
    
    # Now create the browser icon after QApplication is initialized
    if os.path.exists(LOGO_PATH):
        BROWSER_ICON = QIcon(LOGO_PATH)
    else:
        # Fallback to a simple icon file if logo doesn't exist
        BROWSER_ICON = QIcon("favicon.ico")
        
        # Create simple favicon.ico file if it doesn't exist
        if not os.path.exists("favicon.ico"):
            # Create a simple blue icon as a fallback
            icon_pixmap = QPixmap(64, 64)
            icon_pixmap.fill(QColor(59, 130, 246))  # Blue color
            icon_pixmap.save("favicon.ico")
            BROWSER_ICON = QIcon("favicon.ico")
    
    # Set application palette for a cohesive look
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(30, 41, 59))  # Dark slate blue
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(248, 250, 252))
    palette.setColor(QPalette.Text, QColor(30, 41, 59))
    palette.setColor(QPalette.Button, QColor(248, 250, 252))
    palette.setColor(QPalette.ButtonText, QColor(30, 41, 59))
    palette.setColor(QPalette.Link, QColor(59, 130, 246))  # Bright blue
    palette.setColor(QPalette.Highlight, QColor(59, 130, 246))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    browser = Browser()
    sys.exit(app.exec_()) 