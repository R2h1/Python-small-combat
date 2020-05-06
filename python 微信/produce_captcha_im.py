#ImageFont字体类，ImageDraw绘图类
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random

# 随机字母:
def rndChar():
    upper_case = chr(random.randint(65, 90))
    lower_case = upper_case.lower()
    #chr()返回对应字符，65-90为大写字母，97-122为小写字母
    return random.choice((upper_case,lower_case))

# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def main():
	# 图片尺寸
	width = 60 * 4
	height = 60

	#创建Image对象，Image.new(mode,size,color),(255,255,255)为白色
	im = Image.new('RGB', (width, height), (255, 255, 255))

	# 创建Font字体对象:
	font = ImageFont.truetype('C:\Windows\Fonts/Arial.ttf', 36)

	# 创建Draw绘画对象:
	draw = ImageDraw.Draw(im)

	# 随机颜色1填充每个像素:
	for x in range(width):
	    for y in range(height):
	        draw.point((x, y), fill=rndColor())

	# 均匀绘制字母文字:
	for t in range(4):
	    draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())

	# 图像模糊:
	im = im.filter(ImageFilter.BLUR)

	#保存
	im.save('code.jpg', 'jpeg')

if __name__ == '__main__':
	main()

