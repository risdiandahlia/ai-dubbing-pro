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
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
import threading
import time

Window.clearcolor = (0.06, 0.06, 0.12, 1)

LANGUAGES = {
    'id': {'name': 'Indonesia', 'flag': '🇮🇩'},
    'en': {'name': 'English', 'flag': '🇬🇧'},
    'zh': {'name': '中文', 'flag': '🇨🇳'},
    'ja': {'name': '日本語', 'flag': '🇯🇵'},
    'ko': {'name': '한국어', 'flag': '🇰🇷'},
}

class ModernButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.4, 0.48, 0.92, 1)
        self.color = (1, 1, 1, 1)
        self.font_size = dp(14)
        self.bold = True

class DubbingApp(App):
    def build(self):
        self.title = 'AI Dubbing Pro'
        self.selected_langs = []
        
        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(15))
        with header.canvas.before:
            Color(0.4, 0.48, 0.92, 1)
            RoundedRectangle(pos=header.pos, size=header.size, radius=[dp(15)])
        header.bind(pos=lambda obj, val: setattr(header.canvas.before.children[-1], 'pos', val))
        header.bind(size=lambda obj, val: setattr(header.canvas.before.children[-1], 'size', val))
        header.add_widget(Label(text='[b]🎬 AI Dubbing Pro[/b]\n[size=12]Offline Mode[/size]', markup=True, color=(1,1,1,1), font_size=dp(20), halign='center'))
        root.add_widget(header)
        
        # Content
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(15), padding=dp(5))
        content.bind(minimum_height=content.setter('height'))
        
        # Status
        card = self.create_card('📱 Status')
        card.add_widget(Label(text='[color=4caf50]●[/color] Ready', markup=True, color=(0.8,0.9,0.8,1), size_hint_y=None, height=dp(40)))
        content.add_widget(card)
        
        # Input
        card = self.create_card('📁 Input')
        grid = GridLayout(cols=3, spacing=dp(10), size_hint_y=None, height=dp(100))
        grid.add_widget(ModernButton(text='🎥\nVideo'))
        grid.add_widget(ModernButton(text='🎵\nAudio'))
        grid.add_widget(ModernButton(text='📝\nTeks', background_color=(0.2,0.8,0.4,1)))
        card.add_widget(grid)
        content.add_widget(card)
        
        # Languages
        card = self.create_card('🌍 Bahasa')
        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for code, data in LANGUAGES.items():
            btn = ToggleButton(text=f"{data['flag']}\n{data['name']}", size_hint_y=None, height=dp(80), halign='center', background_normal='', background_color=(0.1,0.1,0.15,1), color=(1,1,1,0.8))
            btn.bind(on_press=lambda x, c=code: self.toggle_lang(c, x))
            grid.add_widget(btn)
        card.add_widget(grid)
        content.add_widget(card)
        
        # Process button
        btn = ModernButton(text='🚀 MULAI DUBBING', size_hint_y=None, height=dp(60), font_size=dp(18), on_press=self.process)
        content.add_widget(btn)
        
        scroll.add_widget(content)
        root.add_widget(scroll)
        
        return root
    
    def create_card(self, title):
        card = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10), size_hint_y=None)
        card.bind(minimum_height=card.setter('height'))
        with card.canvas.before:
            Color(0.12,0.12,0.18,1)
            rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(20)])
            card.rect = rect
        card.bind(pos=lambda obj, val: setattr(card.rect, 'pos', val))
        card.bind(size=lambda obj, val: setattr(card.rect, 'size', val))
        card.add_widget(Label(text=f'[b][color=667eea]{title}[/color][/b]', markup=True, size_hint_y=None, height=dp(30), halign='left', font_size=dp(16)))
        return card
    
    def toggle_lang(self, code, btn):
        if btn.state == 'down':
            self.selected_langs.append(code)
            btn.background_color = (0.3,0.7,0.4,1)
        else:
            self.selected_langs.remove(code)
            btn.background_color = (0.1,0.1,0.15,1)
    
    def process(self, x):
        Popup(title='Info', content=Label(text='Processing...', color=(0,0,0,1)), size_hint=(0.8,0.3)).open()

if __name__ == '__main__':
    DubbingApp().run()
