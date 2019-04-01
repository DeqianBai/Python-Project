#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/4/1



import sys, random, argparse
from PIL import Image, ImageDraw

# create spacing/depth example
def createSpacingDepthExample():
    tiles = [Image.open('test/a.png'), Image.open('test/b.png'),
             Image.open('test/c.png')]
    img = Image.new('RGB', (600, 400), (0, 0, 0))
    spacing = [10, 20, 40]
    for j, tile in enumerate(tiles):
        for i in range(8):
            img.paste(tile, (10 + i*(100 + j*10), 10 + j*100))

# 8.3.2 从随机圆创建平铺图像
def createRandmTile(dims):
    # create image
    img=Image.new('RGB',dims)
    draw=ImageDraw.Draw(img)
    # set the radius of a random circle to 1% of width or height, whichever is smaller
    # dims 是一个元组
    r=int(min(*dims)/100)
    # number of circles
    n=1000
    # draw random circle
    for i in range(n):
        x,y=random.randint(0,dims[0]-r),random.randint(0,dims[1]-r)
        fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        draw.ellipse((x-r,y-r,x+r,y+r),fill)

    return img


# 8.3.1 重复给定的平铺图像
def createTiledImage(tile,dims):
    # create the new image
    img=Image.new('RGB',dims)
    W,H=dims
    w,h=tile.size
    # 计算需要的平铺图形数量
    cols=int(W/w)+1
    rows=int(H/h)+1
    # paste the tiles into the image
    for i in range(rows):
        for j in range(cols):
            img.paste(tile,(j*w,i*h))

    # 输出图像
    return img




# 创建一个深度图像用来测试:
def createDepthMap(dims):
  dmap = Image.new('L', dims)
  dmap.paste(10, (200, 25, 300, 125))
  dmap.paste(30, (200, 150, 300, 250))
  dmap.paste(20, (200, 275, 300, 375))
  return dmap

# 给定深度图（图像）和输入图像，创建具有根据深度移位的像素的新图像

def createDepthShiftedImage(dmap, img):
  # size check
  assert dmap.size == img.size
  # create shifted image
  sImg = img.copy()
  # get pixel access
  pixD = dmap.load()
  pixS = sImg.load()
  # shift pixels output based on depth map
  cols, rows = sImg.size
  for j in range(rows):
    for i in range(cols):
      xshift = pixD[i, j]/10
      xpos = i - 140 + xshift
      if xpos > 0 and xpos < cols:
        pixS[i, j] = pixS[xpos, j]
  # return shifted image
  return sImg



# 8.3.3 创建三维立体画

def createAutostereogram(dmap,tile):
    # covert the depth map to a single channel if needed
    if dmap.mode is not 'L':
        dmap=dmap.convert('L')

    # if no image is specified for a tile, create a random circles tile
    if not tile:
        tile=createRandmTile((100,100))

    # cretae an image using depth map values
    img=createTiledImage(tile,dmap.size)
    # create a shifted image using depth map values
    sImg=img.copy()
    # get access to image pixels by loading the Image object first
    pixD=dmap.load()
    pixS=sImg.load()
    # shift pixels horizontally based on depth map
    cols,rows=sImg.size
    for j in range(rows):
        for i in range(cols):
            xshift=pixD[i,j]/10
            xpos=i-tile.size[0]+xshift
            if xpos>0 and xpos <cols:
                pixS[i,j]=pixS[xpos,j]

    # display the shifted image
    return sImg

# 主函数
def main():
    # use sys.argv if needed
    print('creating autostereogram...')
    # creat parser
    parser=argparse.ArgumentParser(description="Autosterograms...")
    # add expected arguments
    parser.add_argument('--depth', dest='dmFile', required=True)
    parser.add_argument('--tile', dest='tileFile', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    # parse args
    args = parser.parse_args()
    # set outfile
    outFile='as.png'
    if args.outFile:
        outFile=args.outFile

    # set files
    tileFile=False
    if args.tileFile:
        tileFile=Image.open(args.tileFile)
    # open depth map
    dmImg=Image.open(args.dmFile)
    # create stereogram
    asImg=createAutostereogram(dmImg,tileFile)
    # write output
    asImg.save(outFile)


# call main
if __name__=='__main__':
    main()





