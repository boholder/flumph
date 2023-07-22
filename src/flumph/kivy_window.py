# from kivy.app import App
# from kivy.clock import Clock
# from kivy.config import Config
# from kivy.uix.label import Label
# from kivy.uix.popup import Popup
#
# from flumph.outer_event_handler import OuterEventHandler
#
# # TODO 这行必须在下面这些import的前面执行才生效，有办法解决吗
# Config.set('graphics', 'shaped', 1)
#
# from kivy.core.image import Image as CoreImage
# from kivy.core.window import Window
# from kivy.resources import resource_find, resource_add_path
#
# resource_add_path('../../data/')
# test_img_path = resource_find('test.png')
# test_img = CoreImage(test_img_path)
# dialog_img_path = resource_find('dialog_bubble.png')
# dialog_img = CoreImage(dialog_img_path)
#
# outer_event_handler = OuterEventHandler()
#
#
# class MainWindow(App):
#     def build(self):
#         Window.size = test_img.size
#         # Clock.schedule_once(self.set_shape)
#         # Clock.schedule_interval(self.move, 1.0)
#         Clock.schedule_interval(self.consume_outer_event, 1.0)
#         # return Button()
#
#     @staticmethod
#     def set_shape(*args):
#         Window.shape_image = test_img_path
#         Window.shape_mode = 'binalpha'
#
#     @staticmethod
#     def move(*args):
#         Window.left = Window.left + 30
#
#     @staticmethod
#     def consume_outer_event(*args):
#         if event := outer_event_handler.get():
#             print(f'kivy receive: {event}')
#             p = Popup(title='a', content=Label(text=event), auto_dismiss=True, size=dialog_img.size)
#             p.background = 'dialog_bubble.png'
#             p.open()
#
#
# def start_main_window():
#     MainWindow().run()
