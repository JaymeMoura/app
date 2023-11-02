from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from playsound import playsound
num=0

def reconhecimento():
    global num
    np.set_printoptions(suppress=True)
    model = load_model("keras_Model.h5", compile=False)
    class_names = open("labels.txt", "r").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open('captured_images\image_{}.png'.format(num)).convert("RGB")
    print(num)
    num += 1
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    
    
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)

    class_name = class_names[index].strip()
    print(class_name)

    if class_name == '0 2':
        playsound('voz\p_9845751_850.mp3')
    elif class_name == '1 5':
        playsound('voz\p_9848847_264.mp3')
    elif class_name == '2 10':
        playsound('voz\p_9847673_859.mp3')
    elif class_name == '3 20':
        playsound('voz\p_9847704_898.mp3')
    elif class_name == '4 50':
        playsound('voz\p_9847745_948.mp3')
    elif class_name == '5 100':
        playsound('voz\p_9848818_216.mp3')
    elif class_name == '6 200':
        playsound('voz\p_10179919_163.mp3')
    else:
         playsound('voz\p_9847600_775.mp3')