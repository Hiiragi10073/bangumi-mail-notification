
import sys
import re
from urllib.parse import quote
import bgmTVApi
import mail
from generateMailContent import generate
from loadYaml import loadYaml

# 获取 qBittorrent 传递的参数
name = sys.argv[1]
path = sys.argv[2]

# 根据路径参数获取分类与番剧名称
category = path.split('/')[2]
subject_name = quote(path.split('/')[3], 'utf-8')

# 番剧信息
subjectInfo = {}
isGetSubjectInfo = False

# 剧集信息
episodeInfo = {}
isGetEpisodeInfo = False

# 错误信息 用于发生请求或者其他错误时，可以通过邮件告知到管理员
errorMsgs = []

# 读取配置文件
config = loadYaml('config.yaml')

mediaUrl = config.get('mediaUrl')
mediaIcon = config.get('mediaIcon')

# 是否是番剧分类，用于判断是否能够在bgmtv中获取信息
isBangumi = category == config.get('bangumiCategory')

# 从标题获取集号的规则
rules = [
    r"(.*) - (\d{1,4}|\d{1,4}\.\d{1,2})(?:v\d{1,2})?(?: )?(?:END)?(.*)",
    r"(.*)[\[ E](\d{1,3}|\d{1,3}\.\d{1,2})(?:v\d{1,2})?(?: )?(?:END)?[\] ](.*)",
    r"(.*)\[第(\d*\.*\d*)话(?:END)?\](.*)",
    r"(.*)\[第(\d*\.*\d*)話(?:END)?\](.*)",
    r"(.*)第(\d*\.*\d*)话(?:END)?(.*)",
    r"(.*)第(\d*\.*\d*)話(?:END)?(.*)",
]

if isBangumi:
    # 获取集号
    episodeNo = 1
    for rule in rules:
        match_obj = re.match(rule, name, re.I)
        if match_obj is not None:
            episodeNo = match_obj.group(2)

    # 获取番剧信息
    subjectRes = bgmTVApi.fetchSubjectInfo(subject_name)
    subjectInfo = subjectRes['data']
    isGetSubjectInfo = subjectRes['status']
    if not isGetSubjectInfo:
        errorMsgs.append(subjectRes['message'])

    # 获取剧集信息
    episodeRes = bgmTVApi.fetchEpisodeInfo(subjectInfo.get('id'), episodeNo)
    episodeInfo = episodeRes['data']
    isGetEpisodeInfo = episodeRes['status']
    if not isGetEpisodeInfo:
        errorMsgs.append(episodeRes['message'])

# 确认邮件标题
mailSubject = ''
if isGetSubjectInfo:
    mailSubject = subjectInfo.get('name_cn') + ' 更新啦！'
else:
    mailSubject = name + ' 下载完成'

# 生成邮件内容
mailContent = ''
if isGetSubjectInfo & isGetEpisodeInfo:
    data = {
        'title': mailSubject,
        'name': episodeInfo.get('name_cn'),
        'image': subjectInfo.get('images').get('large'),
        'summary': subjectInfo.get('summary'),
        'desc': episodeInfo.get('desc'),
        'mediaUrl': mediaUrl,
        'mediaIcon': mediaIcon
    }
    mailContent = generate('./template/email1.html', data)
elif len(errorMsgs) > 0:
    data = {
        'title': mailSubject,
        'name': name,
        'path': path,
        'errorMsgs': errorMsgs
    }
    mailContent = generate('./template/email2.html', data)
else:
    data = {
        'title': mailSubject,
        'name': name,
        'path': path
    }
    mailContent = generate('./template/email3.html', data)

mail.send(mailSubject, mailContent, isBangumi)
