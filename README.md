##oh_my_bilibili 是什么？

这是一个可以在本地下载B站弹幕的脚本，主要是为了方便在本地补番的二次元小伙伴们～

##如何使用？

首先安装所需的库
``` bash
$ sudo pip install requests
```
使用方法
```
-f :所要下载弹幕的文件
-l :文件在B站上的地址
```
例如：
```
./bilibili.py -f \[CASO\&SumiSora\]\[LoveLive\!\]\[13\]\[GB\]\[720p\].mp4 -l http://www.bilibili.com/video/av521616/
```
就会下载LoveLive！第一季第13话的弹幕信息

然后就能愉快地补番了~

##Todo
- [x] 下载完成自动打开 
- [ ] 分析文件名自动获取弹幕
- [ ] 优化弹幕排布算法
- [ ] 对于自带字幕的，解析后合并进弹幕字幕
- [ ] balabala 
