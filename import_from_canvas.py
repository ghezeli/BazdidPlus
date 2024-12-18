import os

def import_from_canvas(input_file, output_dir):
    """
    Read a single text file containing multiple code files (formatted for canvas) and split them into separate files.

    Args:
        input_file (str): The path to the input text file containing canvas-formatted code.
        output_dir (str): The directory to write the separate files.

    Returns:
        None
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(input_file, 'r', encoding='utf-8-sig') as file:
            data = file.read()

        current_file = None
        file_content = []
        file_count = 0  # شمارش تعداد فایل‌ها

        for line in data.splitlines():
            # بدون تغییر دادن خط‌ها و حفظ تمام فاصله‌ها و خطوط خالی
            if line.startswith("# فایل:"):
                if current_file and file_content:
                    # Write the previous file
                    file_path = os.path.join(output_dir, current_file)
                    with open(file_path, 'w', encoding='utf-8') as output_file:
                        # Join lines and remove the last newline if it exists
                        content = "\n".join(file_content).rstrip("\n")
                        output_file.write(content)
                    print(f"File {current_file} saved.")
                    file_count += 1

                # Start a new file
                current_file = line.split("# فایل:")[1].strip()
                file_content = []
            else:
                file_content.append(line)  # اضافه کردن تمامی خطوط (حتی خالی)

        # Write the last file if exists
        if current_file and file_content:
            file_path = os.path.join(output_dir, current_file)
            with open(file_path, 'w', encoding='utf-8') as output_file:
                # Join lines and remove the last newline if it exists
                content = "\n".join(file_content).rstrip("\n")
                output_file.write(content)
            print(f"File {current_file} saved.")
            file_count += 1

        print(f"Total {file_count} files successfully imported to {output_dir}")
    except Exception as e:
        print(f"Error while importing from canvas: {e}")

if __name__ == "__main__":
    import_from_canvas('canvas_data.txt', '_Stage/')
