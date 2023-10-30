import os

count = 0

success = 1
while success:
  file_path = ("C:/Users/jsff/Desktop/TCC/Gen3/frames/iluminacao_total/iluminacao_total_ligado%d.xml" % count)
  if os.path.isfile(file_path):
    os.remove(file_path)
    print(count)
    count += 1
    print("File has been deleted")
  else:
    print(count)
    count += 1
    print("File does not exist")