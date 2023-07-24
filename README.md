# modron

🚧 **WIP** 🚧

这是原型。

1. 不规则窗口
2. 窗口位置移动
3. 外部HTTP请求触发窗口变化（schedule 轮询Queue，生成GUI事件）
4. 经典的客户端主动请求服务端通信问题，是怎样解决I/O bound的？ non-blocking IO
5. 方便创建新的窗口

把项目拆成纯展示和负责处理3，4的网络请求两部分，两者用Queue通信。

curl -X POST -d "hi" http://127.0.0.1:1414/
