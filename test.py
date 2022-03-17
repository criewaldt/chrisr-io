import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(dir_path, "output")
f = os.listdir(output_path)

print(f)