import os
import re
from functools import partial

def getTemplate(filePath):
  currentPath = os.path.dirname(__file__)
  file = open(os.path.join(currentPath, filePath), encoding='utf-8')
  fileData = file.read()
  file.close()
  return fileData

def replaceStr(data, m):
  print(m.group(0))
  param = m.group(0)[2:-2]
  return '{}'.format(data.get(param))

def generate(templatePath, data):
  dataPat = re.compile(r'\{\{(\w*)\}\}')
  return dataPat.sub(partial(replaceStr, data), getTemplate(templatePath))
