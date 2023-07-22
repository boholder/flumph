# flumph

这是原型。

1. ~~不规则窗口~~
2. ~~窗口位置移动~~
3. 外部HTTP请求触发窗口变化（schedule 轮询队列，生成事件）
4. ~~经典的客户端主动请求服务端通信问题，是怎样解决I/O bound的？~~ non-blocking IO，不过kivy有[自带的异步http请求](https://kivy.org/doc/stable/api-kivy.network.urlrequest.html)，不用自己实现了

用线程是正确的。
~~需要用线程池吗？~~ C2S用kivy自带的模块，不需要自己管理，那就flask一个额外线程，不需要线程池。

curl -X POST -d "hi" http://127.0.0.1:1414/