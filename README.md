# modron

🚧 **WIP** 🚧

这是原型。

```commandline
curl -d "hi" http://127.0.0.1:1414/
```


client的主动请求收发，如何与flask共处？（再加一个线程？）
全部用asyncio，跑在主线程外另一个线程里。
https://gist.github.com/boholder/fbc681b1cab464614ee1a7cf80412261
flask换成`quart`，
https://github.com/pallets/quart
暂时用`openai`的依赖，
https://github.com/openai/openai-python#async-api
之后可替换成 `httpx[http2]`
https://www.python-httpx.org/http2/

如何实现quart和主动请求的兼容：
用一个后台任务来跑监听并发送QT界面放入Queue的主动请求，收到请求放入响应Queue。
https://stackoverflow.com/questions/70075859/scheduling-periodic-function-call-in-quart-asyncio
https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html
https://pgjones.gitlab.io/quart/how_to_guides/background_tasks.html

ui，client，server三者的数据流动是怎样的？
openai的流式响应api是什么网络原理？在当前架构的主动请求中能否实现？

------------------------------------------------------

转正式开发：
- [ ] 配pre-commit，把这个加到IDE commit trigger里。
- [ ] 配Github Action，测试和发版。
- [ ] 加上 `CONTRIBUTING.md` 和 `SECURITY.md`
- [ ] 写个非常简单的README

先把文字部分实现齐全再想真正实现多媒体的事
在对未来多角色多用户兼容的前提下设计（以这两个实体为附加属性对其他元素做封装）

悬浮输入框+气泡回复框
正常聊天对话框

聊天记录（sqlite+加密）
在对未来多角色多用户兼容的前提下设计表结构（只需要聊天记录表一张表？）
关于“用户”和“LLM角色”的属性，先熟悉一下open ai（或者llm-kira）是如何解决用户和角色（对话？）问题的？
https://www.google.com/search?q=chat+room+database+design

响应Event(文字，情绪，音频) -> 三个不同的slot。
文字：弹窗
情绪：变换立绘
变换立绘-》重新paint，先了解Qt组件的生命周期
音频：播放音频
处理音频？
https://github.com/jiaaro/pydub
https://doc.qt.io/qt-6/audiooverview.html

点击身体部位判定区
头身比设定，计算移动的步幅

更好看的UI
`QIcon.fromTheme`

------------------------------------------------------

1. 不规则窗口
2. 窗口位置移动
3. 外部HTTP请求触发窗口变化（schedule 轮询Queue，生成GUI事件）
4. 经典的客户端主动请求服务端通信问题，是怎样解决I/O bound的？ non-blocking IO
5. 方便创建新的窗口