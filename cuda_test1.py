import torch
import json
import datetime

if torch.cuda.is_available():
  device = torch.device("cuda:0")
  print("GPU")
  print(torch.cuda.current_device())
  print(torch.cuda.device(0))
  print(torch.cuda.get_device_name(0))
else:
  device = torch.device("cpu")
  print("CPU")
