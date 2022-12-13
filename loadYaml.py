import yaml

def loadYaml(path):
  file = open(path, encoding='utf-8')
  configData = file.read()
  file.close()

  config = yaml.safe_load(configData)
  return config