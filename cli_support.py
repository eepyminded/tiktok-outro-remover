import argparse
import file_looper
import ending_remover

parser = argparse.ArgumentParser("Removing outros of tiktok videos")

parser.add_argument("input_folder", help = "Folder in which to remove videos' endings")
parser.add_argument("-r", "--remove_original_video", help = "Option to let you remove original video after removing output", action = "store_false", dest = "remove_original")
parser.add_argument("-s", "--skip-original-video", help = "If video was already converted and has ORIGINAL string inside of the name, it will be skipped", action = "store_true", dest = "skip_original")
parser.add_argument("-o", "--output-folder", help = "Output folder for converted files", default = False, dest = "output_folder")

args = parser.parse_args()

same_output_val = True

# im not implementing it yet
ignore_progress_queue = True

if not args.output_folder:
    args.output_folder = args.input_folder
else:
    same_output_val = False

try:
    file_looper.loop_through_files(directory = args.input_folder, keep_original_video = args.remove_original,
                                  keep_has_original_in = args.skip_original, same_output_dir_var = same_output_val,
                                  output_dir= args.output_folder, ignore_progress_queue = True, progress_queue = "whatever")

except ending_remover.RemovalError:
    print("ERROR: The app can't convert your videos because to lack of permissions.")
except ending_remover.ConversionError as e:
    print(f"ERROR: The app can't convert your videos because of: {e}")
except PermissionError as e:
    print(f"{e}")
except file_looper.NotStringError:
    print("so uhm we've got a weird error, ")
except file_looper.InvalidPathError:
    print("")