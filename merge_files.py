import os


def generate_project_structure(root_dir, output_file):
    # باز کردن فایل برای نوشتن
    with open(output_file, 'w', encoding='utf-8') as file:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # نوشتن فولدرها
            file.write(f"Directory: {dirpath}\n")
            file.write("Subdirectories:\n")
            for dirname in dirnames:
                file.write(f"  - {dirname}\n")
            file.write("Files:\n")
            # نوشتن فایل‌ها
            for filename in filenames:
                file.write(f"  - {filename}\n")

            file.write("\n" + "-" * 50 + "\n\n")

            # نوشتن محتویات فایل‌های متنی
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if filename.endswith('.txt') or filename.endswith('.py') or filename.endswith('.md') or filename.endswith('.json'):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as content_file:
                            content = content_file.read()
                            file.write(f"Content of {filename}:\n")
                            file.write(content)  # تمام محتوا بدون محدودیت
                            file.write("\n\n")
                    except Exception as e:
                        file.write(f"Could not read {filename}: {e}\n")
            file.write("=" * 50 + "\n")


# مثال استفاده از کد
generate_project_structure("_Stage", "project_merged_code.txt")
