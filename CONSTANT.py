INPUT_IMAGE_SHAPE = (128, 256, 3)
OUTPUT_SHAPE = 94

MODEL_FOLDER_PATH = "models/"
MODEL_CARD_DETECTION_FOLDER_PATH = "%scardDetection/" % MODEL_FOLDER_PATH
DETECTION_ACCURACY_MODEL_PATH = '%sdetection_model_accuracy.h5' % MODEL_CARD_DETECTION_FOLDER_PATH
DETECTION_MODEL_PATH = '%sdetection_model.h5' % MODEL_CARD_DETECTION_FOLDER_PATH
TENSORBOARD_LOG_DIR = "logs/fit/"

'''
    класс карт: 
0-нет
1-шальная
2-заводила
3-наворот
4-приход
5-карта дохлого
6-сокровище

        тип:
0-нет/без типа
1-кумар
2-мрак
3-порча
4-трава
5-угар

    карта:
0-нет
1-25 - номер в типе
'''
