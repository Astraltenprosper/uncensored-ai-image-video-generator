#!/usr/bin/env python3
"""
Image Generator Pro - Приложение для безопасной генерации изображений
"""

import sys
import os
import threading
from datetime import datetime
from pathlib import Path
import json

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QCheckBox,
        QScrollArea, QFrame, QMessageBox, QProgressBar, QFileDialog
    )
    from PyQt5.QtCore import Qt, pyqtSignal, QThread, QSize
    from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette
except ImportError:
    print("Установите PyQt5: pip install PyQt5")
    sys.exit(1)

try:
    from PIL import Image, ImageDraw, ImageFont
    import requests
except ImportError:
    print("Установите требуемые библиотеки: pip install pillow requests")
    sys.exit(1)


class SafetyFilter:
    """Проверка безопасности контента"""
    
    NSFW_KEYWORDS = {
        'nude', 'sex', 'porn', 'xxx', 'naked', 'explicit',
        'adult', 'erotic', 'sexual', 'arousal'
    }
    
    VIOLENCE_KEYWORDS = {
        'kill', 'murder', 'blood', 'violence', 'gun', 'bomb',
        'weapon', 'shoot', 'stab', 'hurt', 'harm', 'death'
    }
    
    HATE_KEYWORDS = {
        'hate', 'racism', 'racist', 'nazi', 'terrorist', 'extremist',
        'discrimination', 'bigot', 'offensive', 'slur'
    }
    
    ILLEGAL_KEYWORDS = {
        'bomb', 'explosive', 'drug', 'cocaine', 'heroin', 'meth',
        'stolen', 'counterfeit', 'fake', 'illegal'
    }
    
    @staticmethod
    def check(text, filters):
        """
        Проверка текста на соответствие фильтрам
        
        Args:
            text: текст для проверки
            filters: dict с флагами фильтров
            
        Returns:
            tuple: (safe: bool, reason: str)
        """
        lower_text = text.lower()
        words = set(lower_text.split())
        
        if filters.get('nsfw', True):
            if SafetyFilter.NSFW_KEYWORDS & words:
                return False, "NSFW контент запрещен"
        
        if filters.get('violence', True):
            if SafetyFilter.VIOLENCE_KEYWORDS & words:
                return False, "Контент с насилием запрещен"
        
        if filters.get('hate', True):
            if SafetyFilter.HATE_KEYWORDS & words:
                return False, "Ненавистный контент запрещен"
        
        if filters.get('illegal', True):
            if SafetyFilter.ILLEGAL_KEYWORDS & words:
                return False, "Незаконный контент запрещен"
        
        return True, "OK"


class ImageGeneratorWorker(QThread):
    """Поток для генерации изображений"""
    
    finished = pyqtSignal(str)  # путь к файлу
    error = pyqtSignal(str)
    progress = pyqtSignal(str)
    
    def __init__(self, prompt, style, quality):
        super().__init__()
        self.prompt = prompt
        self.style = style
        self.quality = quality
        
    def run(self):
        """Генерация изображения"""
        try:
            self.progress.emit("Генерируем изображение...")
            
            # Создаем выходную директорию
            output_dir = Path.home() / "Pictures" / "ImageGenerator"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Генерируем изображение
            img_path = self._generate_image(output_dir)
            
            if img_path:
                self.finished.emit(str(img_path))
            else:
                self.error.emit("Ошибка при генерации изображения")
                
        except Exception as e:
            self.error.emit(f"Ошибка: {str(e)}")
    
    def _generate_image(self, output_dir):
        """Создание изображения"""
        try:
            # Используем локальную генерацию с PIL
            size = {
                'standard': 512,
                'hd': 768,
                '4k': 1024
            }.get(self.quality, 512)
            
            img = self._create_generative_image(self.prompt, self.style, size)
            
            # Сохраняем файл
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = output_dir / f"image_{timestamp}.png"
            img.save(filename)
            
            self.progress.emit(f"✅ Изображение сохранено: {filename}")
            return filename
            
        except Exception as e:
            self.error.emit(f"Ошибка генерации: {str(e)}")
            return None
    
    def _create_generative_image(self, prompt, style, size):
        """Создание изображения на основе промпта и стиля"""
        import random
        
        # Генерируем цвета на основе промпта
        hash_val = sum(ord(c) for c in prompt)
        random.seed(hash_val)
        
        # Основные цвета
        color1 = tuple(random.randint(50, 200) for _ in range(3))
        color2 = tuple(random.randint(50, 200) for _ in range(3))
        color3 = tuple(random.randint(100, 255) for _ in range(3))
        
        # Создаем изображение
        img = Image.new('RGB', (size, size), color1)
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Применяем стиль
        if style == 'artistic':
            self._draw_artistic(draw, size, color2, color3)
        elif style == 'cartoon':
            self._draw_cartoon(draw, size, color2, color3)
        elif style == 'abstract':
            self._draw_abstract(draw, size, color1, color2, color3)
        elif style == 'vintage':
            self._draw_vintage(draw, size, color2, color3)
        elif style == 'cyberpunk':
            self._draw_cyberpunk(draw, size, color2, color3)
        else:  # realistic
            self._draw_realistic(draw, size, color2, color3)
        
        # Добавляем текст
        try:
            font_size = size // 20
            # Пытаемся загрузить системный шрифт
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Текст с промптом
        text = f"{style.upper()}\n{prompt[:40]}..."
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        # Фон для текста
        padding = 20
        draw.rectangle(
            [(x - padding, y - padding), (x + text_width + padding, y + text_height + padding)],
            fill=(0, 0, 0, 180)
        )
        
        # Сам текст
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
        return img
    
    @staticmethod
    def _draw_artistic(draw, size, color1, color2):
        """Художественный стиль"""
        for i in range(0, size, 50):
            draw.line([(0, i), (size, i)], fill=color1, width=2)
            draw.line([(i, 0), (i, size)], fill=color2, width=2)
    
    @staticmethod
    def _draw_cartoon(draw, size, color1, color2):
        """Мультяшный стиль"""
        import random
        random.seed(sum(color1) + sum(color2))
        
        for _ in range(15):
            x = random.randint(0, size)
            y = random.randint(0, size)
            r = random.randint(20, 100)
            draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=color1, outline=color2, width=3)
    
    @staticmethod
    def _draw_abstract(draw, size, color1, color2, color3):
        """Абстрактный стиль"""
        import random
        random.seed(sum(color1) + sum(color2) + sum(color3))
        
        for _ in range(20):
            x1, y1 = random.randint(0, size), random.randint(0, size)
            x2, y2 = random.randint(0, size), random.randint(0, size)
            draw.line([(x1, y1), (x2, y2)], fill=color2, width=random.randint(1, 5))
    
    @staticmethod
    def _draw_vintage(draw, size, color1, color2):
        """Винтажный стиль"""
        # Добавляем сепию-подобный эффект
        for i in range(0, size, 100):
            draw.rectangle([(i, 0), (i+50, size)], fill=color1, outline=color2)
    
    @staticmethod
    def _draw_cyberpunk(draw, size, color1, color2):
        """Киберпанк стиль"""
        # Неоновые линии
        for i in range(0, size, 30):
            draw.line([(0, i), (size, i)], fill=color1, width=1)
        for i in range(0, size, 30):
            draw.line([(i, 0), (i, size)], fill=color2, width=1)
    
    @staticmethod
    def _draw_realistic(draw, size, color1, color2):
        """Фотореалистичный стиль"""
        import random
        random.seed(sum(color1) + sum(color2))
        
        # Более сложная композиция
        for _ in range(30):
            x = random.randint(0, size)
            y = random.randint(0, size)
            w = random.randint(10, 100)
            h = random.randint(10, 100)
            draw.rectangle([(x, y), (x+w, y+h)], fill=color1, outline=color2)


class ImageGeneratorApp(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.current_image = None
        self.init_ui()
        
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("🎨 Image Generator Pro")
        self.setGeometry(100, 100, 1200, 700)
        
        # Общий стиль
        self.setStyleSheet(self._get_stylesheet())
        
        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Левая панель (контролы)
        left_panel = self._create_left_panel()
        
        # Правая панель (превью)
        right_panel = self._create_right_panel()
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
    def _create_left_panel(self):
        """Создание левой панели с контролами"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        
        # Заголовок
        title = QLabel("⚙️ Параметры")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)
        
        # Уведомление о безопасности
        safety_info = QFrame()
        safety_layout = QVBoxLayout(safety_info)
        safety_msg = QLabel("🛡️ Безопасность: Все запросы проверяются на соответствие фильтрам безопасности")
        safety_msg.setWordWrap(True)
        safety_msg.setStyleSheet("color: #93c5fd; background: rgba(59, 130, 246, 0.1); padding: 10px; border-radius: 5px;")
        safety_layout.addWidget(safety_msg)
        layout.addWidget(safety_info)
        
        # Описание изображения
        layout.addWidget(QLabel("Описание изображения:"))
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Опишите, какое изображение вы хотите сгенерировать...")
        self.prompt_input.setMaximumHeight(120)
        layout.addWidget(self.prompt_input)
        
        # Стиль
        layout.addWidget(QLabel("Стиль:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems([
            "realistic", "artistic", "cartoon", "abstract", "vintage", "cyberpunk"
        ])
        layout.addWidget(self.style_combo)
        
        # Качество
        layout.addWidget(QLabel("Качество:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["standard", "hd", "4k"])
        layout.addWidget(self.quality_combo)
        
        # Фильтры безопасности
        layout.addWidget(QLabel("🔍 Фильтры безопасности:"))
        
        self.filters = {}
        self.filters['nsfw'] = QCheckBox("Блокировать NSFW контент")
        self.filters['nsfw'].setChecked(True)
        layout.addWidget(self.filters['nsfw'])
        
        self.filters['violence'] = QCheckBox("Блокировать насилие")
        self.filters['violence'].setChecked(True)
        layout.addWidget(self.filters['violence'])
        
        self.filters['hate'] = QCheckBox("Блокировать ненавистный контент")
        self.filters['hate'].setChecked(True)
        layout.addWidget(self.filters['hate'])
        
        self.filters['illegal'] = QCheckBox("Блокировать незаконный контент")
        self.filters['illegal'].setChecked(True)
        layout.addWidget(self.filters['illegal'])
        
        layout.addSpacing(20)
        
        # Кнопки
        self.generate_btn = QPushButton("🚀 Сгенерировать изображение")
        self.generate_btn.setFont(QFont('Arial', 11, QFont.Bold))
        self.generate_btn.setMinimumHeight(45)
        self.generate_btn.clicked.connect(self.generate_image)
        layout.addWidget(self.generate_btn)
        
        self.clear_btn = QPushButton("↺ Очистить")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_btn)
        
        self.download_btn = QPushButton("⬇️ Скачать изображение")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.clicked.connect(self.download_image)
        self.download_btn.setEnabled(False)
        layout.addWidget(self.download_btn)
        
        layout.addStretch()
        
        # Инфо
        info = QLabel("v1.0 - Безопасная генерация изображений")
        info.setStyleSheet("color: #64748b; font-size: 11px;")
        layout.addWidget(info)
        
        return frame
    
    def _create_right_panel(self):
        """Создание правой панели с превью"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        
        title = QLabel("📸 Результат")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)
        
        # Превью изображения
        self.preview_label = QLabel()
        self.preview_label.setMinimumSize(400, 400)
        self.preview_label.setStyleSheet(
            "border: 2px dashed #475569; border-radius: 10px; "
            "background: rgba(15, 23, 42, 0.6);"
        )
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setText("🖼️\n\nЗдесь появится ваше изображение")
        layout.addWidget(self.preview_label)
        
        # Прогресс
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Сообщения
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: #cbd5e1; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        return frame
    
    def generate_image(self):
        """Генерация изображения"""
        prompt = self.prompt_input.toPlainText().strip()
        
        if not prompt:
            self.show_error("Пожалуйста, напишите описание изображения")
            return
        
        # Проверка безопасности
        filters = {k: v.isChecked() for k, v in self.filters.items()}
        safe, reason = SafetyFilter.check(prompt, filters)
        
        if not safe:
            self.show_error(reason)
            return
        
        # Отключаем кнопки
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(50)
        
        # Запускаем генерацию в отдельном потоке
        self.worker = ImageGeneratorWorker(
            prompt,
            self.style_combo.currentText(),
            self.quality_combo.currentText()
        )
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.progress.connect(self.update_status)
        self.worker.start()
    
    def on_generation_finished(self, image_path):
        """Обработка завершения генерации"""
        self.current_image = image_path
        self.progress_bar.setValue(100)
        
        # Загружаем изображение
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaledToWidth(400, Qt.SmoothTransformation)
        self.preview_label.setPixmap(scaled_pixmap)
        
        self.download_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        self.show_success("✅ Изображение успешно сгенерировано!")
    
    def on_generation_error(self, error_msg):
        """Обработка ошибки генерации"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.show_error(f"❌ {error_msg}")
    
    def update_status(self, message):
        """Обновление статуса"""
        self.status_label.setText(message)
    
    def download_image(self):
        """Скачивание изображения"""
        if not self.current_image:
            return
        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Сохранить изображение", "", "PNG (*.png);;JPG (*.jpg)"
        )
        
        if file_path:
            import shutil
            shutil.copy(self.current_image, file_path)
            self.show_success(f"✅ Изображение сохранено: {file_path}")
    
    def clear_all(self):
        """Очистка всех данных"""
        self.prompt_input.clear()
        self.preview_label.setText("🖼️\n\nЗдесь появится ваше изображение")
        self.preview_label.setPixmap(QPixmap())
        self.status_label.clear()
        self.download_btn.setEnabled(False)
        self.current_image = None
    
    def show_error(self, message):
        """Показать сообщение об ошибке"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: #fca5a5; font-size: 12px;")
    
    def show_success(self, message):
        """Показать успешное сообщение"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: #bbf7d0; font-size: 12px;")
    
    def _get_stylesheet(self):
        """CSS стили для приложения"""
        return """
            QMainWindow {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            }
            
            QFrame {
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 10px;
                padding: 15px;
            }
            
            QLabel {
                color: #e2e8f0;
            }
            
            QTextEdit, QLineEdit, QComboBox {
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(148, 163, 184, 0.3);
                border-radius: 6px;
                color: #e2e8f0;
                padding: 8px;
                font-size: 11px;
            }
            
            QTextEdit:focus, QLineEdit:focus, QComboBox:focus {
                border: 1px solid #06b6d4;
                background: rgba(15, 23, 42, 0.9);
            }
            
            QPushButton {
                background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 10px;
            }
            
            QPushButton:hover {
                background: linear-gradient(135deg, #0891b2 0%, #2563eb 100%);
            }
            
            QPushButton:pressed {
                background: linear-gradient(135deg, #0e7490 0%, #1d4ed8 100%);
            }
            
            QPushButton:disabled {
                background: #64748b;
                color: #94a3b8;
            }
            
            QCheckBox {
                color: #cbd5e1;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 1px solid rgba(148, 163, 184, 0.3);
                background: rgba(15, 23, 42, 0.6);
            }
            
            QCheckBox::indicator:checked {
                background: #06b6d4;
                border: 1px solid #06b6d4;
            }
            
            QProgressBar {
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(148, 163, 184, 0.3);
                border-radius: 6px;
                text-align: center;
                color: #e2e8f0;
            }
            
            QProgressBar::chunk {
                background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
                border-radius: 4px;
            }
        """


def main():
    """Главная функция"""
    app = QApplication(sys.argv)
    window = ImageGeneratorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
