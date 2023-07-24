# modron

🚧 **WIP** 🚧

这是原型。

```commandline
curl -X POST -d "hi" http://127.0.0.1:1414/
```

响应Event(文字，情绪，音频) -> 三个不同的slot。
文字：弹窗
情绪：变换立绘
音频：播放音频

头身比设定，计算移动的步幅和点击的身体部位判定区。

处理音频？
https://github.com/jiaaro/pydub
https://doc.qt.io/qt-6/audiooverview.html