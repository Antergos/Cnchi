with open("nvidia.txt", "r") as nvidia_txt:
    txt = nvidia_txt.readlines()
    
with open("nvidia-out.py", "w") as nvidia:
    for line in txt:
        line = line.rtrim().split()
        pciid = line.pop(0)
        line = ', '.join(line)
        # NOT FINISHED
