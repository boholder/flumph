# flumph

这是原型。

1. 不规则窗口
2. 窗口位置移动
3. 外部HTTP请求触发窗口变化（schedule 轮询Queue，生成GUI事件）
4. 经典的客户端主动请求服务端通信问题，是怎样解决I/O bound的？ non-blocking IO
5. 方便创建新的窗口

用线程是正确的。
需要用线程池吗？

curl -X POST -d "hi" http://127.0.0.1:1414/