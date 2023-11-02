from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
import os
from teste import reconhecimento

num=0

class MainApp(MDApp):
    dir = 'captured_images'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
        
    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        self.save_img_button = MDRaisedButton(
            text="Qual a Cédula",
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            size_hint=(None, None)
        )
        self.save_img_button.bind(on_press=self.take_picture)
        layout.add_widget(self.save_img_button)
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.image_frame = None  # Inicialize a imagem de captura
        self.image_counter = 0  # Contador de imagens
        self.image_directory = "captured_images"  # Diretório para salvar imagens

        if not os.path.exists(self.image_directory):
            os.makedirs(self.image_directory)

        self.update_video()
        return layout

    def update_video(self, dt=1.0/30.0):
        ret, frame = self.capture.read()
        self.image_frame = frame

        if self.image_frame is not None:

            # Redimensiona a imagem para manter a proporção 244x244
            target_size = (244, 244)
            frame_height, frame_width, _ = self.image_frame.shape

            # Calcula a escala para redimensionar a imagem mantendo a proporção
            scale_x = target_size[0] / frame_width
            scale_y = target_size[1] / frame_height
            scale = min(scale_x, scale_y)

            # Aplica o zoom à imagem
            zoomed_frame = cv2.resize(self.image_frame, None, fx=scale, fy=scale)

            # Corta o quadrado no centro da imagem
            height, width, _ = zoomed_frame.shape
            if height > width:
                margin = (height - width) // 2
                zoomed_frame = zoomed_frame[margin:margin + width, :]
            elif width > height:
                margin = (width - height) // 2
                zoomed_frame = zoomed_frame[:, margin:margin + height]

            # Converte de volta para o formato BGR
            zoomed_frame = cv2.cvtColor(zoomed_frame, cv2.COLOR_BGR2RGB)

            # Se a imagem não for exatamente 244x244, redimensione-a para 244x244
            if zoomed_frame.shape[0] != 244 or zoomed_frame.shape[1] != 244:
                zoomed_frame = cv2.resize(zoomed_frame, (244, 244))

            # Atualiza a textura da imagem
            buffer = cv2.flip(zoomed_frame, 0).tostring()
            texture = Texture.create(size=(zoomed_frame.shape[1], zoomed_frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buffer, colorfmt='rgb', bufferfmt='ubyte')
            self.image.texture = texture

        Clock.schedule_once(self.update_video, 1.0/30.0)

    def take_picture(self, *args):
        if self.image_frame is not None:
            image_name = os.path.join(self.image_directory, f"image_{self.image_counter}.png")
            cv2.imwrite(image_name, self.image_frame)
            self.image_counter += 1
            reconhecimento()
            
if __name__ == '__main__':
    MainApp().run()