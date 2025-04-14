# 通过焦距计算像素
def calFx(focalLength, frameHeight):
    imageHeight = 1080
    res = focalLength * (imageHeight / frameHeight)
    return res


res = calFx(21, 24)
print(res)
