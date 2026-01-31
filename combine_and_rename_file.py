import sys
from pathlib import Path

def process_files(target_dir, search_pattern,custom_name):
    root = Path(target_dir)
    
    if not root.exists():
        print(f"❌ Error: ไม่พบ Directory '{target_dir}'")
        return
    
    for folder in [f for f in root.rglob("*") if f.is_dir()]:
        found_files = list(folder.glob(search_pattern))
        
        if not found_files:
            continue
        
        day_name = folder.name
        month_name = folder.parent.name
        file_extension = found_files[0].suffix
        
        new_filename = f"{custom_name}_{month_name}{day_name}{file_extension}"
        output_path = folder/new_filename
        
        if output_path.exists():
            print(f"⏩ skip [{folder.name}]: found '{new_filename}' exist")
            continue
        
        count = len(found_files)
        
        if count > 1:
            with output_path.open('w', encoding='utf-8') as outfile:
                for idx, f_path in enumerate(found_files):
                    if f_path.stat().st_size == 0:
                        print(f"   ⚠️ Skip empty file: {f_path.name}")
                        continue
                    
                    with f_path.open('r', encoding='utf-8') as infile:
                        if idx == 0:
                            content = infile.read()
                            outfile.write(content)
                        else:
                            first_line = infile.readline()
                            if not first_line:
                                continue
                            content = infile.read()
                            outfile.write(content)
                            
                        if not content.endswith('\n'):
                            outfile.write('\n')
            print(f"✏️  Merge all files to : {new_filename}")

                            
        elif count == 1:
            if found_files[0].name != new_filename:
                found_files[0].rename(output_path)
                print(f"✏️  Changed file name to : {new_filename}")
                        

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("\n How to use:")
        print("\n python combine_and_rename.py [Main Directory], [File name pattern] [new_filename]")
        print("\nSample")
        print("python combine_and_rename.py ./my_data \"zbx*.csv\" \"pk_zabbix\"")
    else:
        arg_dir = sys.argv[1]
        arg_pattern = sys.argv[2]
        arg_filename = sys.argv[3]
        process_files(arg_dir, arg_pattern,arg_filename)