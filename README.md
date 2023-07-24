# modron

🚧 **WIP** 🚧

这是原型。

```commandline
curl -X POST -d "hi" http://127.0.0.1:1414/
```

响应Event(文字，情绪，音频) -> 三个不同的slot。

把项目拆成纯展示和负责处理收发网络请求等两部分，两者不同线程用Queue通信。

处理音频？
https://github.com/jiaaro/pydub