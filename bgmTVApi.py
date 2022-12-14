import os
import requests
from requests import exceptions

# 消除ssl告警
requests.packages.urllib3.disable_warnings()

currentPath = os.path.dirname(__file__)
tokenFile = open(os.path.join(currentPath, 'accessToken'), encoding = "utf-8")
token = tokenFile.read().splitlines()[0]
tokenFile.close()

headers = { 'Authorization': f'Bearer {token}', 'Content-Type': 'application/json',  'User-Agent': 'Hiiragi/bangumi-mail-notification' }

def fetchSubjectInfo(subject_name):
  result = {
    'status': False,
    'data': None,
    'message': ''
  }

  try:
      response = requests.get(url=f'https://api.bgm.tv/search/subject/{subject_name}?type=2&responseGroup=medium', verify=False,  headers=headers)
  except exceptions.Timeout as e:
      result['message'] = '番剧信息请求超时：' + str(e.message)
  except exceptions.HTTPError as e:
      result['message'] = '番剧信息http请求错误：' + str(e.message)
  else:
      if response.status_code == 200:
          resJson = response.json()
          if resJson.get('list') is not None:
              result['data'] = resJson.get('list')[0]
              result['status'] = True
      else:
        result['message'] = '番剧信息请求错误：' + str(response.status_code) + ',' + str(response.reason)

  return result

def fetchEpisodeInfo(subject_id, episodeNo):
  result = {
    'status': False,
    'data': None,
    'message': ''
  }

  try:
      response = requests.get(url=f'https://api.bgm.tv/v0/episodes?subject_id={subject_id}', verify=False, headers=headers)
  except exceptions.Timeout as e:
      result['message'] = '剧集信息请求超时：' + str(e.message)
  except exceptions.HTTPError as e:
      result['message'] = '剧集信息http请求错误：' + str(e.message)
  else:
      if response.status_code == 200:
          resJson = response.json()
          if resJson.get('data') is not None:
              for d in resJson.get('data'):
                  if d.get('ep') == int(episodeNo):
                      result['data'] = d
                      result['status'] = True
      else:
        result['message'] = '剧集信息请求错误：' + str(response.status_code) + ',' + str(response.reason)

  return result
