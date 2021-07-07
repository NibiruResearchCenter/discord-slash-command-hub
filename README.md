# Discord Slash Command Hub

本项目为 Discord 服务器 Mirror's Edge

## command-hub

此函数接受 Discord Slash Command 请求，返回 pending 状态并将请求消息体存入 Azure Storage Queue

## warm-up

此函数每 15 分钟触发一次，保持整个程序热加载，防止冷启动导致操作时间超过 3000ms 使 Discord 判定请求失败
