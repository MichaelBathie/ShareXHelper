import glob
import os
import pathlib
import shutil
import getpass
import keyboard
from win10toast import ToastNotifier

USERNAME = getpass.getuser()

p_down = False;
ctrl_down = False

def find_recent_folder():
  #assume default ShareX location
  folder_list = glob.glob('C:\\Users\\{}\\Documents\\Sharex\\Screenshots\\*'.format(USERNAME))
  recent_folder = max(folder_list, key=os.path.getctime)
  #grab the most recent screenshot folder
  return recent_folder[-7:]

def find_recent_file(folder):
  #get the most recent screenshot
  file_list = glob.glob('C:\\Users\\{}\\Documents\\Sharex\\Screenshots\\{}\\*'.format(USERNAME, folder))
  recent_file = max(file_list, key=os.path.getctime)
  file_split = recent_file.split('\\')
  return file_split[len(file_split) - 1]

def move_file(folder, my_file):
  #Check if the temp folder already exists and if not, create it 
  if not(os.path.exists('C:\\Users\\{}\\Documents\\Sharex\\temp'.format(USERNAME))):
    pathlib.Path('C:\\Users\\{}\\Documents\\Sharex\\temp'.format(USERNAME)).mkdir(parents=True, exist_ok=True)

  delete_previous()

  #copy over the newest screenshot
  original = 'C:\\Users\\{}\\Documents\\Sharex\\Screenshots\\{}\\{}'.format(USERNAME, folder, my_file)
  target = 'C:\\Users\\{}\\Documents\\Sharex\\temp\\{}'.format(USERNAME, my_file)

  shutil.copyfile(original, target)

def delete_previous():
  files = glob.glob('C:\\Users\\{}\\Documents\\Sharex\\temp\\*'.format(USERNAME))

  #making sure we empty the temp folder before adding anything new
  if(len(files) > 0):
    for f in files:
        os.remove(f)

def run():
  folder = find_recent_folder()
  my_file = find_recent_file(folder)
  move_file(folder, my_file)
  os.startfile('C:\\Users\\{}\\Documents\\Sharex\\temp'.format(USERNAME))

#########################################################################################################

if __name__ == "__main__":
  toast = ToastNotifier()
  toast.show_toast("ShareX Helper","Process started", duration=30)

  os.chdir('C:\\Users\\{}\\Documents\\GitHub\\ShareXHelper'.format(USERNAME))

  keyboard.add_hotkey('ctrl+alt+p', run)
  while True:
    keyboard.wait('ctrl+alt+p')

