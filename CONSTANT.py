INPUT_IMAGE_SHAPE = (128, 256, 3)
OUTPUT_SHAPE = 94

DATASET_FOLDER = '../card_detection/dataset/card'

MODEL_FOLDER_PATH = "models/"

MODEL_CARD_DETECTION_FOLDER_PATH = "%scardDetection/" % MODEL_FOLDER_PATH
DETECTION_ACCURACY_MODEL_PATH = '%sdetection_model_accuracy.h5' % MODEL_CARD_DETECTION_FOLDER_PATH
DETECTION_MODEL_PATH = '%sdetection_model.h5' % MODEL_CARD_DETECTION_FOLDER_PATH

AGENT_MODEL_FOLDER_PATH = "%sagent/" % MODEL_FOLDER_PATH
AGENT_ACCURACY_MODEL_PATH = '%sagent_model_accuracy.h5' % AGENT_MODEL_FOLDER_PATH
AGENT_MODEL_PATH = '%sagent_model.h5' % AGENT_MODEL_FOLDER_PATH

TENSORBOARD_LOG_DIR = "logs/fit/"
DETECTION_LOG_DIR = '%sdetection/' % TENSORBOARD_LOG_DIR

TENSORBOARD_WRITE_IMAGES = True

LEARN_WITH_AUGMENTATION = True

DATASET_LABEL = ['101', '211', '212', '213', '214', '221', '222', '223', '224', '231', '232', '233', '234', '241',
                 '242', '243', '244', '251', '252', '253', '254', '311', '312', '313', '314', '321', '322', '323',
                 '324', '331', '332', '333', '334', '341', '342', '343', '344', '351', '352', '353', '354', '411',
                 '412', '413', '414', '421', '422', '423', '424', '431', '432', '433', '434', '441', '442', '443',
                 '444', '451', '452', '453', '454', '501', '502', '503', '504', '505', '506', '507', '601', '602',
                 '603', '604', '605', '606', '607', '608', '609', '6010', '6011', '6012', '6013', '6014', '6015',
                 '6016', '6017', '6018', '6019', '6020', '6021', '6022', '6023', '6024', '6025']

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
