import os

dir_list = []
output_dir_general = "./output"
output_dir = ""

if os.path.exists(output_dir_general):
    pass
else:
    os.makedirs(output_dir_general)

for root, path, files in os.walk("./"):
        for file in files:
            if ".fna" in file:
                dir_list.append(os.path.join("./",file))
prokka_command = ""
for i in dir_list:
    output_dir = output_dir_general + "/" + i[2:-4]
    print("\r", "working on:", i, end="", flush=True)
    prokka_command = "prokka --outdir "+output_dir+" "+i
    os.system(prokka_command)

