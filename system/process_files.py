import os
import re

def move_and_rename_videos(directory):
    """Moves video files to the parent directory and renames them.

    Args:
        directory: The directory to search for video files.
    """

    video_extensions = ('.mp4', '.mkv', '.avi')

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(video_extensions):
                source_path = os.path.join(root, file)
                parent_dir = os.path.dirname(root)

                # Rename the file using regular expressions
                new_name = re.sub(r'(?<=.)(1080p|720p|2160p|\bx264\b).*?(?=\.)', '', file)                 
                #new_name = re.sub(r'(?<=.)(1080p|720p|2160p)?\.\w+\.', '.', file)               
                #new_name = re.sub(r'(?<=.)(1080p|720p|2160p).*?(?=\.)', '', file)               
                #new_name = re.sub(r'(?:1080p|720p|2160p)\K.*?(?=\.)', '', file) 
                destination_path = os.path.join(parent_dir, new_name)

                # Move the file
                # os.rename(source_path, destination_path)
                print(f"Moved and renamed '{file}' to '{new_name}'")

# Example usage
if __name__ == "__main__":
    directory_to_process = "Tmp"  # Replace with your actual directory
    move_and_rename_videos(directory_to_process)