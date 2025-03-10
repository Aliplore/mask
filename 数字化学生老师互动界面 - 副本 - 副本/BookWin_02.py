import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedWidget, \
    QMessageBox
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont, QColor
from PyQt5 import uic
from PyQt5.QtGui import QTextDocument, QTextCursor, QTextBlockFormat, QTextCharFormat


class LetterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_window()
        self.init_pages()

    def init_window(self):
        """初始化窗口"""
        self.setWindowTitle("书信输入")
        self.setGeometry(600, 300, 600, 500)

        self.setFixedSize(600, 500)  # 固定窗口大小

        # 禁止窗口的最大化按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # 使用 QStackedWidget 实现多页面切换
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

    def init_pages(self):
        """初始化所有页面"""
        # 第一页：书信输入页面
        self.page_letter = QWidget()
        self.init_letter_page()
        self.stacked_widget.addWidget(self.page_letter)

        # 第二页：下一页内容
        self.page_next = uic.loadUi("PlaygroundWindow_02.ui")
        self.init_next_page()
        self.stacked_widget.addWidget(self.page_next)

        # 第三页
        self.page_three = uic.loadUi("ImageShow_03.ui")
        self.init_three_page()
        self.stacked_widget.addWidget(self.page_three)

    def init_letter_page(self):
        """初始化书信输入页面"""
        layout = QVBoxLayout(self.page_letter)
        self.font = QFont("楷体", 11)

        # 设置背景图像
        self.set_background_image(self.page_letter, "imgs/3.jpg")

        # 显示书信内容的标签
        self.label_letter = QLabel()
        self.setup_label(self.label_letter, self.font, Qt.AlignLeft | Qt.AlignTop, True)
        layout.addWidget(self.label_letter)

        # 开始按钮
        self.button_start = QPushButton("开始写信")
        self.setup_button(self.button_start, self.font, self.start_letter)
        layout.addWidget(self.button_start)

        # 进入下一页按钮
        self.button_next = QPushButton("进入下一页")
        self.setup_button(self.button_next, self.font, self.go_to_next_page)
        self.button_next.setEnabled(False)  # 初始状态禁用
        layout.addWidget(self.button_next)

        # 书信内容
        self.letter_content = """
亲爱的邓老师：
    您好！

    时光匆匆，转眼间我们快要毕业了。我一直想找机会向您表达我的感激之情。感谢您两年来给予我慈母般的关爱：摔倒了，是您教会我如何爬起来；失败了，是您教会我如何吸取教训；哭泣时，是您在我身旁安慰我。还记得那次，我在课堂上答错问题，紧张得满脸通红，满手是汗，是您微笑着走到我身边，轻轻地拍了拍我的肩膀，温柔地鼓励我；“别害怕，相信自己，再想想，大胆说出来让我们听听！”在老师的鼓励下，我勇敢地讲出了自己的想法，赢得同学们一阵阵掌声。

    从那以后，我重拾自信，在语文课上积极举手发言。我知道自己有时会任性调皮，给您添了不少麻烦，但您从来没有严厉地斥责过我，而是用温和的话语引导我。您的教导就像一盏明灯，照亮我前行的道路。您不仅是传道授业的好老师，更是我们亲密无间的良师益友。最难忘的是那次在操场上，您正带着一群同学打篮球，只见您一个灵活的转身，轻松避开了防守的同学，您高高跃起，双手举起篮球。篮球在空中划过一道漂亮的弧线，球如入无人之境，一击即中，引得同学们一阵欢呼。您那专注又充满活力的身影，哪像个语文老师，分明是我们的挚友，那一刻，我们师生之间的距离被无限拉近。

    一朝沐杏雨，一生念师恩。感谢您一直以来的关心和教导。毕业后，我会常常回学校看望您，祝您身体健康，工作顺利，生活愉快！
                                                       学生：崔凯晴
                                                       2025年3月5日

        """
        self.current_text = ""  # 当前显示的文字
        self.char_index = 0  # 当前字符的索引

        # 定时器用于逐字输出
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_letter)

    def init_next_page(self):
        """初始化下一页"""
        # 获取 UI 中的组件
        self.label_1 = self.page_next.findChild(QLabel, "label_2x1")
        self.label_2 = self.page_next.findChild(QLabel, "label_2x2")
        self.label_3 = self.page_next.findChild(QLabel, "label_2x3")
        self.label_4 = self.page_next.findChild(QLabel, "label_2x4")
        self.label_result = self.page_next.findChild(QLabel, "label_2x5")
        self.label_back_onepage = self.page_next.findChild(QLabel, "label_2x6")
        self.label_to_threepage = self.page_next.findChild(QLabel, "label_2x7")

        # 设置标签样式
        self.set_label_style(self.label_1)
        self.set_label_style(self.label_2)
        self.set_label_style(self.label_3)
        self.set_label_style(self.label_4)
        self.set_label_result_style(self.label_result)
        self.set_labelpage_style(self.label_back_onepage)
        self.set_labelpage_style(self.label_to_threepage)

        # 设置字体
        font = QFont("楷体")
        font2 = QFont("楷体", 13)
        labels = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_back_onepage,
                  self.label_to_threepage]
        for label in labels:
            label.setFont(font)
        self.label_result.setFont(font2)

        # 绑定点击事件
        self.label_1.mousePressEvent = lambda event: self.on_label_click(self.label_1)
        self.label_2.mousePressEvent = lambda event: self.on_label_click(self.label_2)
        self.label_3.mousePressEvent = lambda event: self.on_label_click(self.label_3)
        self.label_4.mousePressEvent = lambda event: self.on_label_click(self.label_4)
        self.label_back_onepage.mousePressEvent = lambda event: self.go_to_letter_page()
        self.label_to_threepage.mousePressEvent = lambda event: self.go_to_three_page()

        # 初始化逐字显示定时器
        self.result_timer = QTimer()
        self.result_timer.timeout.connect(self.update_result_text)
        self.result_text = ""  # 当前显示的结果文字
        self.result_char_index = 0  # 当前字符的索引

        # 初始化颜色变化定时器
        self.color_timer = QTimer()
        self.color_timer.timeout.connect(self.update_label_colors)
        self.color_timer.start(200)  # 每200ms更新一次颜色

    def init_three_page(self):
        """初始化第三页"""
        # 获取 UI 中的组件
        self.image_label = self.page_three.findChild(QLabel, "label_3x1")  # 获取图像显示区域
        if self.image_label is None:
            raise ValueError("未找到 image_label，请检查 UI 文件")

        self.label_3x2 = self.page_three.findChild(QLabel, "label_3x2")
        self.label_3x2.setAttribute(Qt.WA_TranslucentBackground)
        font = QFont("楷体", 16)
        self.label_3x2.setFont(font)

        # 图像列表
        self.image_paths = ["imgs/shool_1.jpg", "imgs/shool_2.jpg", "imgs/shool_3.jpg",
                            "imgs/shool_4.jpg", "imgs/shool_5.jpg", "imgs/shool_6.jpg"]  # 替换为你的图像路径
        self.current_image_index = 0

        # 加载第一张图像
        self.show_image()

        # 为图片标签添加点击事件处理函数
        self.image_label.mousePressEvent = self.on_image_click

    def show_image(self):
        """显示当前图像"""
        pixmap = QPixmap(self.image_paths[self.current_image_index])
        # 保持原始比例，并使用高质量缩放
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_image_click(self, event):
        """图片点击事件处理函数"""
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.show_image()
        else:
            QMessageBox.information(self, "提示", "该图片为最后一页")

    def start_letter(self):
        """开始写信"""
        self.button_start.setEnabled(False)  # 禁用按钮
        self.current_text = ""  # 清空当前文字
        self.char_index = 0  # 重置字符索引
        self.timer.start(150)  # 每1ms输出一个字

    def update_letter(self):
        """逐字更新书信内容"""
        if self.char_index < len(self.letter_content):
            # 获取当前字符
            current_char = self.letter_content[self.char_index]
            self.current_text += current_char
            self.label_letter.setText(self.current_text)
            self.char_index += 1

            # 判断是否到达“此致”部分
            if "生活愉快！" in self.current_text:
                # 加快显示速度
                self.timer.setInterval(80)  # 每50ms输出一个字
            else:
                # 正常显示速度
                self.timer.setInterval(150)  # 每100ms输出一个字
        else:
            self.timer.stop()  # 停止定时器
            self.button_next.setEnabled(True)  # 启用进入下一页按钮

    def go_to_next_page(self):
        """跳转到下一页"""
        self.stacked_widget.setCurrentIndex(1)  # 切换到第二页

    def go_to_letter_page(self):
        """返回书信页面"""
        self.stacked_widget.setCurrentIndex(0)  # 切换回第一页

    def go_to_three_page(self):
        """切换到第三页"""
        self.stacked_widget.setCurrentIndex(2)  # 切换到第3页

    def set_label_result_style(self, label):
        """设置标签样式"""
        label.setStyleSheet(
            """
            QLabel {
                background-color: white;  /* 背景为白色 */
                color: black;  /* 字体为黑色 */
                font-size: 16px;
            }
            """
        )
        label.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明

    def set_label_style(self, label):
        """设置标签样式"""
        label.setStyleSheet(
            """
            QLabel {
                background-color: transparent;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: none;  /* 去掉边框 */
            }
            """
        )
        label.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明

    def set_labelpage_style(self, label):
        """设置按钮样式"""
        label.setStyleSheet(
            """
            QLabel {
                background-color: transparent;
                color: black;
                font-size: 16px;
            }
            """
        )
        label.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明

    def on_label_click(self, label):
        """标签点击事件"""
        texts = {
            "label_2x1": """
同学们，我们一起踢足球吧!  ... 时间过得飞快，
太阳就要落山了,让我们进入下一页回想我们在一起的时光吧！""",
            "label_2x2": """
同学们，我们一起跑步吧!  ... 时间过得飞快，
太阳就要落山了,让我们进入下一页回想我们在一起的时光吧！""",
            "label_2x3": """
同学们，我们一起打乒乓球吧!  ... 时间过得飞快，
太阳就要落山了,让我们进入下一页回想我们在一起的时光吧！""",
            "label_2x4": """
同学们，我们一起打篮球吧!  ... 时间过得飞快，
太阳就要落山了,让我们进入下一页回想我们在一起的时光吧！""",
        }
        self.result_text = texts[label.objectName()]
        self.current_text_label = ''
        self.result_char_index = 0
        self.label_result.setText("")  # 清空结果标签
        self.result_timer.start(200)  # 每10ms输出一个字

    def update_result_text(self):
        """逐字更新结果文字"""
        if self.result_char_index < len(self.result_text):
            self.current_text_label += self.result_text[self.result_char_index]
            self.label_result.setText(self.current_text_label)
            self.result_char_index += 1
        else:
            self.result_timer.stop()  # 停止定时器

    def update_label_colors(self):
        """更新标签颜色"""
        # 生成随机颜色
        colors = [QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)).name() for _ in
                  range(4)]
        labels = [self.label_1, self.label_2, self.label_3, self.label_4]
        for label, color in zip(labels, colors):
            label.setStyleSheet(f"color: {color}; background-color: transparent; font-weight: bold; font-size: 16px;")

    def set_background_image(self, widget, image_path):
        """设置背景图像"""
        widget.setStyleSheet(
            f"""
            QWidget {{
                background-image: url({image_path});
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
            }}
            """
        )

    def setup_label(self, label, font, alignment, word_wrap):
        """设置标签的通用属性"""
        label.setFont(font)
        label.setAlignment(alignment)
        label.setWordWrap(word_wrap)

    def setup_button(self, button, font, callback):
        """设置按钮的通用属性"""
        button.setFont(font)
        button.clicked.connect(callback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LetterWindow()
    window.show()
    sys.exit(app.exec_())
