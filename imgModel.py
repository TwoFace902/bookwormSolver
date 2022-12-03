from pathlib import Path
import tensorflow as tf
import keras
from keras.preprocessing import image
from keras import layers
import random

def loadImage(filename):
  img = image.load_img(filename, color_mode="grayscale", target_size=(100,100))
  # img.show()
  return image.img_to_array(img) == 255

def ltrToNum(c):
  return ord(c[0]) - ord('A')

def shuffleTogether(a,b):
  zipped = [(a[i], b[i]) for i in range(len(a))]
  random.shuffle(zipped)
  a = [x[0] for x in zipped]
  b = [x[1] for x in zipped]
  return (a,b)

def loadImgData():
  imageList = []
  labelList = []

  for letterDir in Path("trainingset").iterdir():
    for imgFile in letterDir.iterdir():
      imageList.append(loadImage(imgFile))
      labelList.append([i == ltrToNum(letterDir.name) for i in range(26)])

  imageList, labelList = shuffleTogether(imageList, labelList)

  return (tf.constant(imageList), tf.constant(labelList))

def buildModel():
  inps = keras.Input(shape=(None,None,1))
  x = layers.Conv2D(filters=26*2, kernel_size=(3,3), activation="relu")(inps)
  x = layers.Conv2D(filters=26*2, kernel_size=(3,3), activation="relu")(x)
  x = layers.Conv2D(filters=26*2, kernel_size=(3,3), activation="relu")(x)
  x = layers.Conv2D(filters=26*2, kernel_size=(10,10), activation="relu")(x)
  x = layers.Conv2D(filters=26*2, kernel_size=(10,10), activation="relu")(x)
  x = layers.GlobalAveragePooling2D()(x)
  otps = layers.Dense(26, activation="sigmoid")(x)
  otps = layers.Dense(26, activation="softmax")(x)
  model = keras.Model(inputs=inps, outputs=otps)
  return model


print("Loading image data...")

images, labels = loadImgData()

print("Loaded image data")

model = buildModel()
model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["acc"])

print("Training...")

# batch size seems to be really important in determining how fast it converges, when I leave batch size at default (32), it converges much slower
# add more epochs to make it train longer
model.fit(images, labels, batch_size=1, epochs=10, validation_split=.2)

print("Done training")

fileLoc = input("Where should I save weights (filename; enter nothing to not save weights)?: ")
if fileLoc != "":
  model.save_weights(fileLoc)
