import yaml
import os

def loadYaml(path):
  currentPath = os.path.dirname(__file__)
  file = open(os.path.join(currentPath, path), encoding='utf-8')
  configData = file.read()
  file.close()

  config = yaml.safe_load(configData)
  return config