from threading import Thread
from subprocess import run as sprun
from time import sleep
import re

CREATE_NO_WINDOW = 0x08000000
cutscene_playing = False
# path to mpv
mpv = "mpv"
# path to cemu log
cemu_log = "./BIN/log.txt"
# path to directory with game files
game_path = r"./GAMES/The Legend of Zelda Breath of the Wild [ALZP01]/"


def play_movie(movie_path):
    global cutscene_playing
    if not cutscene_playing:
        cutscene_playing = True
        sprun([mpv, "--no-osc", "--fs", "--ontop", game_path + movie_path])
        cutscene_playing = False

def play_audio(audio_path):
    global cutscene_playing
    if cutscene_playing:
        sprun([mpv, game_path + audio_path], creationflags=CREATE_NO_WINDOW)

# http://stackoverflow.com/a/5420116
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    movie_thread = Thread()
    log = open(cemu_log, "r")
    log_lines = follow(log)
    for line in log_lines:
        if "FSOpenFile" in line:
            if ".mp4" in line:
                print(line)
                path = re.search(r"(?<=/vol/).*\.mp4", line).group(0)
                movie_thread = Thread(target=play_movie, args=(path,))
                movie_thread.start()
            # elif ".bfstm" in line:
            #     path = re.search(r"(?<=/vol/).*\.bfstm", line).group(0)
            #     t = Thread(target=play_audio, args=(path,))
            #     t.start()
