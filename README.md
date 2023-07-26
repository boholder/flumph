# modron

🚧 **WIP** 🚧

这是原型。

```commandline
curl -X POST -d "hi" http://127.0.0.1:1414/
```

变换立绘-》先了解Qt组件的生命周期

验证：
响应Event(文字，情绪，音频) -> 三个不同的slot。
文字：弹窗
情绪：变换立绘
音频：播放音频
处理音频？
https://github.com/jiaaro/pydub
https://doc.qt.io/qt-6/audiooverview.html

client的主动请求收发，如何与flask共处？（再加一个线程？）
ui，client，server三者的数据流动是怎样的？

先把文字部分实现齐全再想真正实现多媒体的事

悬浮输入框+气泡回复框
正常聊天对话框
聊天记录（sqlite+加密）

点击身体部位判定区
头身比设定，计算移动的步幅