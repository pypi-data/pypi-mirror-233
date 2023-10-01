import zipfile
import os


def rc_unzip(zipname, dirt_name):
    with zipfile.ZipFile(file=zipname, mode='r') as zf:
        # 解压到指定目录,首先创建一个解压目录
        os.mkdir(dirt_name)
        for old_name in zf.namelist():
            # 获取文件大小，目的是区分文件夹还是文件，如果是空文件应该不好用。
            file_size = zf.getinfo(old_name).file_size
            # 由于源码遇到中文是cp437方式，所以解码成gbk，windows即可正常
            new_name = old_name.encode('cp437').decode('gbk')
            # 拼接文件的保存路径
            new_path = os.path.join(dirt_name, new_name)
            # 判断文件是文件夹还是文件
            if file_size > 0:
                # 是文件，通过open创建文件，写入数据
                with open(file=new_path, mode='wb') as f:
                    # zf.read 是读取压缩包里的文件内容
                    f.write(zf.read(old_name))
            else:
                # 是文件夹，就创建
                os.mkdir(new_path)
