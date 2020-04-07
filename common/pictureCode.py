# Author:gyk

# 验证码coding
from io import BytesIO
import random
from PIL import Image,ImageFont,ImageDraw


def get_color(arg):
    if arg == 'bg':
        return (random.randint(200,255),random.randint(200,255),random.randint(200,255))
    elif arg == 'l':
        return (random.randint(100,220),random.randint(100,220),random.randint(150,220))
    else:
        return (random.randint(0,100),random.randint(0,100),random.randint(0,100))

# 验证码生成与获取
def gen_code():
    img = Image.new('RGB', (300, 35), get_color('bg'))
    # 把图片放到画板上
    draw=ImageDraw.Draw(img)
    # 生成字体文件,font=None,传一个ttf格式的字体文件, size=1,字体大小
    font=ImageFont.truetype(font='static/font/ss.ttc',size=30)
    code_str=''
    for i in range(5):
        num=str(random.randint(0,9))
        #随机生成一个大写字母
        upper_t= chr(random.randint(65,90))
        # 随机生成一个小写字母
        lower_t=chr(random.randint(97,122))

        t=random.choice([num,upper_t,lower_t])
        code_str+=t

        draw.text((40+i*45,0),t,fill=get_color('f'),font=font)
    '''
        1 生成一个随机字符串:sdafasfasd
        2 在cookie中写入:sessionid:sdafasfasd
        3 在数据库中保存:sdafasfasd  {valid_code:验证码}
    '''
    width = 320
    height = 35
    for i in range(10):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        # 在图片上画线
        draw.line((x1, y1, x2, y2), fill=get_color('l'))

    for i in range(10):
        # 画点
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_color('bg'))

    f=BytesIO()
    img.save(f,'png')
    data=f.getvalue()

    # 返回一张图片
    return data,code_str