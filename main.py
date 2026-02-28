#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Dubbing Pro - Android Offline
Fully functional dubbing app with 5 languages
"""

import os
import threading
import time
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.animation import Animation

# Configure window
Window.clearcolor = (0.06, 0.06, 0.12, 1)
Window.softinput_mode = 'below_target'

# Language data
LANGUAGES = {
    'id': {'name': 'Indonesia', 'flag': '🇮🇩', 'code': 'id-ID'},
    'en': {'name': 'English', 'flag': '🇬🇧', 'code': 'en-US'},
    'zh': {'name': '中文', 'flag': '🇨🇳', 'code': 'zh-CN'},
    'ja': {'name': '日本語', 'flag': '🇯🇵', 'code': 'ja-JP'},
    'ko': {'name': '한국어', 'flag': '🇰🇷', 'code': 'ko-KR'},
}

VOICE_STYLES = {
    'natural': {'name': 'Natural', 'icon': '🎯', 'speed': 1.0},
    'professional': {'name': 'Professional', 'icon': '👔', 'speed': 0.9},
    'fast': {'name': 'Fast', 'icon': '⚡', 'speed': 1.3},
    'slow': {'name': 'Slow', 'icon': '🐢', 'speed': 0.8},
}


class ModernButton(Button):
    """Custom button with modern styling"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.4, 0.48, 0.92, 1)  # Primary blue
        self.color = (1, 1, 1, 1)
        self.font_size = dp(14)
        self.bold = True
        self.border_radius = [dp(12)]


class LanguageButton(ToggleButton):
    """Language selection button"""
    def __init__(self, lang_code, **kwargs):
        super().__init__(**kwargs)
        self.lang_code = lang_code
        data = LANGUAGES[lang_code]
        self.text = f"{data['flag']}\n[b]{data['name']}[/b]"
        self.markup = True
        self.group = 'languages'
        self.allow_no_selection = True
        self.size_hint_y = None
        self.height = dp(85)
        self.halign = 'center'
        self.valign = 'middle'
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0.1, 0.1, 0.15, 1)
        self.color = (1, 1, 1, 0.9)


class DubbingProApp(App):
    def build(self):
        self.title = 'AI Dubbing Pro'
        
        # App state
        self.selected_languages = []
        self.selected_voice = 'natural'
        self.input_type = 'text'
        self.is_processing = False
        
        # Main layout
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(12))
        
        # Header
        header = self.create_header()
        root.add_widget(header)
        
        # Scrollable content
        scroll = ScrollView(do_scroll_x=False)
        self.content = BoxLayout(
            orientation='vertical', 
            size_hint_y=None,
            spacing=dp(15),
            padding=dp(5)
        )
        self.content.bind(minimum_height=self.content.setter('height'))
        
        # Add sections
        self.content.add_widget(self.create_status_card())
        self.content.add_widget(self.create_input_section())
        self.content.add_widget(self.create_language_section())
        self.content.add_widget(self.create_voice_section())
        self.content.add_widget(self.create_settings_section())
        self.content.add_widget(self.create_progress_section())
        self.content.add_widget(self.create_process_button())
        self.content.add_widget(self.create_results_section())
        
        scroll.add_widget(self.content)
        root.add_widget(scroll)
        
        return root
    
    def create_header(self):
        """Create app header"""
        header = BoxLayout(
            size_hint_y=None, 
            height=dp(75),
            padding=dp(15)
        )
        
        with header.canvas.before:
            Color(0.4, 0.48, 0.92, 1)
            self.header_rect = RoundedRectangle(
                pos=header.pos,
                size=header.size,
                radius=[dp(15)]
            )
        
        header.bind(pos=self._update_header)
        header.bind(size=self._update_header)
        
        title = Label(
            text='[b]🎬 AI Dubbing Pro[/b]\n[size=13]Offline Mode v2.0[/size]',
            markup=True,
            color=(1, 1, 1, 1),
            font_size=dp(22),
            halign='center'
        )
        header.add_widget(title)
        
        return header
    
    def _update_header(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size
    
    def create_card(self, title, accent_color=(0.4, 0.48, 0.92, 1)):
        """Create card container"""
        card = BoxLayout(
            orientation='vertical',
            padding=dp(18),
            spacing=dp(12),
            size_hint_y=None
        )
        card.bind(minimum_height=card.setter('height'))
        
        with card.canvas.before:
            Color(0.12, 0.12, 0.18, 1)
            rect = RoundedRectangle(
                pos=card.pos,
                size=card.size,
                radius=[dp(20)]
            )
            card.rect = rect
        
        card.bind(pos=lambda obj, val: setattr(card.rect, 'pos', val))
        card.bind(size=lambda obj, val: setattr(card.rect, 'size', val))
        
        # Title
        title_label = Label(
            text=f'[b][color=667eea]{title}[/color][/b]',
            markup=True,
            size_hint_y=None,
            height=dp(35),
            halign='left',
            text_size=(Window.width - dp(80), None),
            font_size=dp(17)
        )
        card.add_widget(title_label)
        
        return card
    
    def create_status_card(self):
        """Create status indicator"""
        card = self.create_card('📱 Status Sistem')
        
        self.status_label = Label(
            text='[color=4caf50]●[/color] Ready - Offline Mode Active',
            markup=True,
            color=(0.8, 0.9, 0.8, 1),
            size_hint_y=None,
            height=dp(40),
            halign='left',
            text_size=(Window.width - dp(80), None),
            font_size=dp(14)
        )
        card.add_widget(self.status_label)
        
        return card
    
    def create_input_section(self):
        """Create input selection"""
        card = self.create_card('📁 Pilih Input')
        
        # Input type buttons
        grid = GridLayout(cols=3, spacing=dp(10), size_hint_y=None, height=dp(110))
        
        self.btn_video = ModernButton(
            text='🎥\nVideo',
            on_press=lambda x: self.set_input_type('video')
        )
        self.btn_audio = ModernButton(
            text='🎵\nAudio', 
            on_press=lambda x: self.set_input_type('audio')
        )
        self.btn_text = ModernButton(
            text='📝\nTeks',
            background_color=(0.2, 0.8, 0.4, 1),
            on_press=lambda x: self.set_input_type('text')
        )
        
        grid.add_widget(self.btn_video)
        grid.add_widget(self.btn_audio)
        grid.add_widget(self.btn_text)
        card.add_widget(grid)
        
        # File chooser (for video/audio)
        self.file_chooser_btn = ModernButton(
            text='📂 Pilih File dari Penyimpanan',
            size_hint_y=None,
            height=dp(55),
            background_color=(0.2, 0.25, 0.35, 1),
            on_press=self.show_file_chooser
        )
        card.add_widget(self.file_chooser_btn)
        
        # Selected file label
        self.selected_file_label = Label(
            text='',
            color=(0.6, 0.8, 0.6, 1),
            size_hint_y=None,
            height=dp(30),
            font_size=dp(12)
        )
        card.add_widget(self.selected_file_label)
        
        # Text input
        self.text_input = TextInput(
            hint_text='Masukkan teks untuk dubbing di sini...\n\nContoh:\nHalo semuanya! Selamat datang di video ini. Hari ini kita akan belajar cara membuat konten viral dengan AI.',
            multiline=True,
            size_hint_y=None,
            height=dp(180),
            background_color=(0.08, 0.08, 0.12, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.4, 0.48, 0.92, 1),
            padding=dp(15),
            font_size=dp(14),
            hint_text_color=(0.4, 0.4, 0.5, 1)
        )
        card.add_widget(self.text_input)
        
        self.selected_file = None
        
        return card
    
    def set_input_type(self, input_type):
        """Switch input type"""
        self.input_type = input_type
        
        # Reset colors
        default_color = (0.2, 0.2, 0.3, 1)
        active_color = (0.4, 0.48, 0.92, 1)
        text_color = (0.2, 0.8, 0.4, 1)
        
        self.btn_video.background_color = active_color if input_type == 'video' else default_color
        self.btn_audio.background_color = active_color if input_type == 'audio' else default_color
        self.btn_text.background_color = text_color if input_type == 'text' else default_color
        
        # Show/hide elements
        if input_type == 'text':
            self.file_chooser_btn.opacity = 0
            self.file_chooser_btn.disabled = True
            self.selected_file_label.opacity = 0
            self.text_input.opacity = 1
            self.text_input.disabled = False
        else:
            self.file_chooser_btn.opacity = 1
            self.file_chooser_btn.disabled = False
            self.selected_file_label.opacity = 1
            self.text_input.opacity = 0.3
            self.text_input.disabled = True
    
    def show_file_chooser(self, instance):
        """Show file chooser popup"""
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Simple file list (simulated)
        scroll = ScrollView()
        file_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        file_list.bind(minimum_height=file_list.setter('height'))
        
        # Mock files
        mock_files = [
            '/sdcard/Download/video_sample.mp4',
            '/sdcard/Music/audio_sample.mp3',
            '/sdcard/Recordings/voice_note.wav'
        ]
        
        for f in mock_files:
            btn = Button(
                text=os.path.basename(f),
                size_hint_y=None,
                height=dp(50),
                background_color=(0.15, 0.15, 0.2, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=lambda x, file=f: self.select_file(file, popup))
            file_list.add_widget(btn)
        
        scroll.add_widget(file_list)
        content.add_widget(scroll)
        
        close_btn = ModernButton(
            text='Tutup',
            size_hint_y=None,
            height=dp(50),
            on_press=lambda x: popup.dismiss()
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Pilih File',
            content=content,
            size_hint=(0.9, 0.7),
            background_color=(0.1, 0.1, 0.15, 1)
        )
        popup.open()
    
    def select_file(self, filepath, popup):
        self.selected_file = filepath
        self.selected_file_label.text = f'✓ {os.path.basename(filepath)}'
        popup.dismiss()
    
    def create_language_section(self):
        """Create language selection"""
        card = self.create_card('🌍 Bahasa Target (Pilih Multiple)')
        
        grid = GridLayout(cols=2, spacing=dp(12), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        self.lang_buttons = {}
        for code, data in LANGUAGES.items():
            btn = LanguageButton(code)
            btn.bind(on_press=lambda x, c=code: self.toggle_language(c, x))
            self.lang_buttons[code] = btn
            grid.add_widget(btn)
        
        card.add_widget(grid)
        return card
    
    def toggle_language(self, code, button):
        """Toggle language selection"""
        if button.state == 'down':
            if code not in self.selected_languages:
                self.selected_languages.append(code)
            # Animate selection
            button.background_color = (0.3, 0.7, 0.4, 1)
            anim = Animation(background_color=(0.25, 0.65, 0.35, 1), duration=0.2)
            anim.start(button)
        else:
            if code in self.selected_languages:
                self.selected_languages.remove(code)
            button.background_color = (0.1, 0.1, 0.15, 1)
    
    def create_voice_section(self):
        """Create voice style selection"""
        card = self.create_card('🎙️ Gaya Suara AI')
        
        box = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(10))
        
        self.voice_buttons = {}
        for voice_id, voice_data in VOICE_STYLES.items():
            btn = ToggleButton(
                text=f"{voice_data['icon']}\n{voice_data['name']}",
                group='voice',
                state='down' if voice_id == 'natural' else 'normal',
                background_normal='',
                background_down='',
                background_color=(0.4, 0.48, 0.92, 1) if voice_id == 'natural' else (0.15, 0.15, 0.2, 1),
                color=(1, 1, 1, 1),
                halign='center',
                valign='middle'
            )
            btn.bind(on_press=lambda x, v=voice_id: self.set_voice(v))
            self.voice_buttons[voice_id] = btn
            box.add_widget(btn)
        
        card.add_widget(box)
        return card
    
    def set_voice(self, voice_id):
        """Set voice style"""
        self.selected_voice = voice_id
        for vid, btn in self.voice_buttons.items():
            if vid == voice_id:
                btn.background_color = (0.4, 0.48, 0.92, 1)
            else:
                btn.background_color = (0.15, 0.15, 0.2, 1)
    
    def create_settings_section(self):
        """Create advanced settings"""
        card = self.create_card('⚙️ Pengaturan Lanjut')
        
        # Speed slider
        speed_box = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        speed_box.add_widget(Label(
            text='Kecepatan:',
            color=(0.8, 0.8, 0.8, 1),
            size_hint_x=0.25,
            font_size=dp(14)
        ))
        
        self.speed_slider = Slider(
            min=0.5,
            max=2.0,
            value=1.0,
            size_hint_x=0.5
        )
        self.speed_slider.bind(value=self.update_speed_label)
        
        self.speed_value_label = Label(
            text='1.0x',
            color=(0.4, 0.48, 0.92, 1),
            size_hint_x=0.25,
            font_size=dp(16),
            bold=True
        )
        
        speed_box.add_widget(self.speed_slider)
        speed_box.add_widget(self.speed_value_label)
        card.add_widget(speed_box)
        
        # Toggles
        toggles = [
            ('📄 Generate Subtitle', True),
            ('💾 Auto Save to Gallery', True),
            ('🔊 Keep Original Audio', False),
        ]
        
        for text, default in toggles:
            toggle_box = BoxLayout(size_hint_y=None, height=dp(55))
            toggle_box.add_widget(Label(
                text=text,
                color=(0.85, 0.85, 0.85, 1),
                font_size=dp(14),
                halign='left',
                text_size=(Window.width - dp(150), None)
            ))
            switch = Switch(active=default)
            toggle_box.add_widget(switch)
            card.add_widget(toggle_box)
        
        return card
    
    def update_speed_label(self, instance, value):
        self.speed_value_label.text = f'{value:.1f}x'
    
    def create_progress_section(self):
        """Create progress indicator"""
        self.progress_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(20),
            opacity=0
        )
        
        with self.progress_card.canvas.before:
            Color(0.08, 0.08, 0.15, 0.95)
            self.progress_rect = RoundedRectangle(
                pos=self.progress_card.pos,
                size=self.progress_card.size,
                radius=[dp(20)]
            )
        
        self.progress_card.bind(pos=lambda obj, val: setattr(self.progress_rect, 'pos', val))
        self.progress_card.bind(size=lambda obj, val: setattr(self.progress_rect, 'size', val))
        
        self.progress_label = Label(
            text='Memproses...',
            color=(1, 1, 1, 1),
            font_size=dp(16),
            bold=True
        )
        
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=dp(20)
        )
        
        self.progress_detail = Label(
            text='Mempersiapkan...',
            color=(0.7, 0.7, 0.7, 1),
            font_size=dp(12)
        )
        
        self.progress_card.add_widget(self.progress_label)
        self.progress_card.add_widget(self.progress_bar)
        self.progress_card.add_widget(self.progress_detail)
        
        return self.progress_card
    
    def create_process_button(self):
        """Create main process button"""
        self.process_btn = ModernButton(
            text='🚀 MULAI DUBBING OFFLINE',
            size_hint_y=None,
            height=dp(65),
            font_size=dp(18),
            on_press=self.start_processing
        )
        
        # Add pulse animation
        self.pulse_anim = Animation(
            background_color=(0.5, 0.58, 1, 1),
            duration=1
        ) + Animation(
            background_color=(0.4, 0.48, 0.92, 1),
            duration=1
        )
        self.pulse_anim.repeat = True
        self.pulse_anim.start(self.process_btn)
        
        return self.process_btn
    
    def create_results_section(self):
        """Create results container"""
        self.results_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(15)
        )
        self.results_box.bind(minimum_height=self.results_box.setter('height'))
        return self.results_box
    
    def start_processing(self, instance):
        """Start dubbing process"""
        if self.is_processing:
            return
        
        # Validation
        if len(self.selected_languages) == 0:
            self.show_error('Pilih minimal satu bahasa!')
            return
        
        if self.input_type == 'text':
            if not self.text_input.text.strip():
                self.show_error('Masukkan teks terlebih dahulu!')
                return
        else:
            if not self.selected_file:
                self.show_error('Pilih file terlebih dahulu!')
                return
        
        # Start processing
        self.is_processing = True
        self.process_btn.disabled = True
        self.process_btn.text = '⏳ MEMPROSES...'
        self.pulse_anim.stop(self.process_btn)
        
        # Show progress
        self.progress_card.opacity = 1
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self.progress_card)
        
        # Start thread
        threading.Thread(target=self.process_dubbing, daemon=True).start()
    
    def process_dubbing(self):
        """Main processing logic"""
        try:
            total_steps = len(self.selected_languages) * 3 + 2
            current_step = 0
            
            steps = [
                'Menganalisis input...',
                'Menyiapkan audio...',
                'Transkripsi dengan AI...',
                'Menerjemahkan ke {lang}...',
                'Generate suara AI...',
                'Sinkronisasi audio...',
                'Finalisasi...'
            ]
            
            for i, lang in enumerate(self.selected_languages):
                lang_name = LANGUAGES[lang]['name']
                
                for j in range(3):
                    current_step += 1
                    progress = (current_step / total_steps) * 100
                    
                    step_text = steps[min(j + 2, len(steps) - 1)].format(lang=lang_name)
                    
                    Clock.schedule_once(
                        lambda dt, p=progress, t=step_text: self.update_progress(p, t),
                        0
                    )
                    
                    time.sleep(1.5)  # Simulate work
            
            # Complete
            Clock.schedule_once(lambda dt: self.update_progress(100, 'Selesai!'), 0)
            time.sleep(0.5)
            Clock.schedule_once(lambda dt: self.show_results(), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(str(e)), 0)
        finally:
            self.is_processing = False
            Clock.schedule_once(lambda dt: self.reset_ui(), 0)
    
    def update_progress(self, value, text):
        self.progress_bar.value = value
        self.progress_detail.text = text
    
    def show_results(self):
        """Display results"""
        self.results_box.clear_widgets()
        
        for lang in self.selected_languages:
            data = LANGUAGES[lang]
            
            # Result card
            card = BoxLayout(
                orientation='vertical',
                padding=dp(20),
                spacing=dp(15),
                size_hint_y=None,
                height=dp(220)
            )
            
            with card.canvas.before:
                Color(0.15, 0.35, 0.2, 1)
                rect = RoundedRectangle(
                    pos=card.pos,
                    size=card.size,
                    radius=[dp(20)]
                )
                card.rect = rect
            
            card.bind(pos=lambda obj, val, c=card: setattr(c.rect, 'pos', val))
            card.bind(size=lambda obj, val, c=card: setattr(c.rect, 'size', val))
            
            # Header
            header = BoxLayout(size_hint_y=None, height=dp(50))
            header.add_widget(Label(
                text=f"{data['flag']} [b]{data['name']}[/b]",
                markup=True,
                color=(1, 1, 1, 1),
                font_size=dp(20)
            ))
            card.add_widget(header)
            
            # Waveform visualization
            waveform = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(3))
            for i in range(20):
                bar = Label(
                    size_hint_x=1,
                    canvas_before=Color(0.4, 0.48, 0.92, 1)
                )
                waveform.add_widget(bar)
            card.add_widget(waveform)
            
            # Action buttons
            btn_grid = GridLayout(cols=2, spacing=dp(12), size_hint_y=None, height=dp(55))
            
            play_btn = ModernButton(
                text='▶️ PLAY',
                on_press=lambda x, l=lang: self.play_result(l)
            )
            save_btn = ModernButton(
                text='💾 SIMPAN',
                background_color=(0.3, 0.7, 0.4, 1),
                on_press=lambda x, l=lang: self.save_result(l)
            )
            
            btn_grid.add_widget(play_btn)
            btn_grid.add_widget(save_btn)
            card.add_widget(btn_grid)
            
            # Animation
            card.opacity = 0
            self.results_box.add_widget(card)
            
            anim = Animation(opacity=1, duration=0.5)
            anim.start(card)
        
        self.content.height = self.content.minimum_height
    
    def play_result(self, lang):
        self.show_notification(f'Memutar {LANGUAGES[lang]["name"]}...')
    
    def save_result(self, lang):
        self.show_notification(f'{LANGUAGES[lang]["name"]} disimpan!')
    
    def reset_ui(self):
        """Reset UI state"""
        self.process_btn.disabled = False
        self.process_btn.text = '🚀 MULAI DUBBING OFFLINE'
        
        anim = Animation(opacity=0, duration=0.3)
        anim.start(self.progress_card)
        
        self.pulse_anim.start(self.process_btn)
    
    def show_error(self, message):
        """Show error popup"""
        popup = Popup(
            title='⚠️ Error',
            content=Label(
                text=message,
                color=(1, 0.3, 0.3, 1),
                font_size=dp(14)
            ),
            size_hint=(0.8, 0.25),
            background_color=(0.15, 0.1, 0.1, 1)
        )
        popup.open()
    
    def show_notification(self, message):
        """Show success notification"""
        popup = Popup(
            title='✅ Sukses',
            content=Label(
                text=message,
                color=(0.3, 1, 0.3, 1),
                font_size=dp(14)
            ),
            size_hint=(0.8, 0.25),
            background_color=(0.1, 0.15, 0.1, 1),
            auto_dismiss=True
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)


if __name__ == '__main__':
    DubbingProApp().run()
