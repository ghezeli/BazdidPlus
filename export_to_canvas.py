import os

def export_to_canvas(input_dir, output_file, exclude_files=None):
    """
    Combine multiple code files into a single text file formatted for canvas.

    Args:
        input_dir (str): The directory containing the code files to combine.
        output_file (str): The path to the output text file for canvas.
        exclude_files (list): A list of file names to exclude from the output.

    Returns:
        None
    """
    if exclude_files is None:
        exclude_files = []

    try:
        with open(output_file, 'w', encoding='utf-8') as output_file_obj:
            for file_name in sorted(os.listdir(input_dir)):
                file_path = os.path.join(input_dir, file_name)

                # Check if the file is in the exclude list
                if os.path.isfile(file_path) and file_name not in exclude_files:
                    output_file_obj.write(f"# فایل: {file_name}\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as input_file:
                            output_file_obj.write(input_file.read())
                    except UnicodeDecodeError:
                        # اگر خطای کدگذاری اتفاق افتاد، از کدگذاری دیگری استفاده می‌کنیم
                        with open(file_path, 'r', encoding='ISO-8859-1') as input_file:
                            output_file_obj.write(input_file.read())
                    output_file_obj.write("\n\n")

        print(f"Canvas-compatible file successfully created at {output_file}")
    except Exception as e:
        print(f"Error while exporting to canvas: {e}")

if __name__ == "__main__":
    # اضافه کردن فایل‌هایی که نمی‌خواهید در خروجی قرار بگیرند
    exclude_files = ['errors.log']  # اینجا لیست فایل‌های مورد نظر را قرار دهید
    export_to_canvas('_Stage/', 'canvas_data.txt', exclude_files)
