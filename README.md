# bangumi-mail-notification

番剧下载更新提醒脚本

### 说明

这个东西是在自建番剧影音服务器中由于 qBittorrent 的下载完成通知的模板过于简陋以及 JellyFin 的新增内容通知与下载完成的时机有一定偏差（模板有时候也不好看）而自学了两天 python 做出来用于给自己一个比较美观的邮件通知，并且可以搭配一些使用邮件触发的应用使用。

### 使用场景

这个脚本使用的 bgm.tv 的 api 用于获取番剧与剧集信息，如果想使用其他站点的 api，请自行修改。

### 使用方式

1. 将文件夹直接放到 qBittorrent 可以访问到的路径中
2. 修改 config.yaml 文件中的配置
3. 在 https://next.bgm.tv/demo/access-token 生成一个 Access Token, 并写入到 accessToken 文件中
4. （可选）修改邮件模板和主题以及其他个性配置
5. 确保 qBittorrent 的环境中有 python3 和 requests 包
6. 在 qBittorrent 的下载完成时执行的输入框中填 `python3 <这里填路径>/bangumi-mail-notification/app.py "%N" "%D"`
7. 测试

### config.yaml 配置介绍

```yaml
email:
  from: ['邮件来源显示名称', 'example@163.com'] # 发送方
  user: example@example.com # 发送邮件的账户 同发送方
  passwd: xxxxxxxxxxxxxx # 发送邮件的密码（非邮件账户密码）
  smtp: smtp.163.com # smtp 邮件服务器
  port: 465 # 端口 ssl 为 True 时填 465
  ssl: True # 是否使用 ssl 加密
  # 配置收件人，同发送方
  to: [['收件人1名称', example1@163.com'], ['收件人2名称', example2@163.com']]

# 需要进行剧集信息搜索的分类名称（qBittorrent的分类）
bangumiCategory: Bangumi

# 媒体库的地址与图标url
mediaUrl: https://media.example.com
mediaIcon: https://picbed.example.com/media.png
```
