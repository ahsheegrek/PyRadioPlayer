import sys
import os
import PySimpleGUI as sg
import random
import load_stations
import radioPlayerClass
from pynput import keyboard

themes = sg.theme_list()

# 起動時にランダムなテーマを選択
theme = random.choice(themes)

# テーマを固定したい場合は以下で指定
#theme = sg.theme("DarkTeal1")

#stations.jsonを読み込む(実行ファイルと同じパスにあること)
dirname = os.path.dirname(sys.argv[0])
file_path = os.path.join(dirname, 'stations.json')
stations = load_stations.load_stations(file_path)

#GUIの作成
sg.theme(theme)

layout = [    [sg.Frame(title='Now Playing', layout=[        [sg.Text(size=(32, 1), key='-CURRENT-STATION-', font=("Helvetica", 12), justification='center')],
        [sg.Column([            [sg.Button(station_name, key=station_name, size=(30, 1), font=("Helvetica", 12))] for station_name in stations.keys()
        ], scrollable=True, vertical_scroll_only=True, size=(300, 700))], #ウインドウが長すぎて切れてしまう場合はここの700を減らす
        ])],
        [sg.Frame(title='Volume', layout=[            [sg.Slider(range=(0, 100), default_value=100, size=(35, 30), orientation='h', key='-VOLUME-', enable_events=True)]
        ])],
        [sg.Push(), sg.Button('RANDOM STATION', key='-PLAY-RANDOM-', size=(35, 1), font=("Helvetica", 12)), sg.Push()],
        [sg.Push(), sg.Button('Mute', key='-MUTE-', size=(35, 1), font=("Helvetica", 12), bind_return_key=True), sg.Push()]
        
]

window = sg.Window('Radio Player', layout)

#radioPlayerClassのインスタンスを作成
radio_player = radioPlayerClass.RadioPlayer(window)

#メインループ
def on_press(key): #メディアキーの再生でミュートをトグル
    try:
        if key == keyboard.Key.media_play_pause:
            window.write_event_value('-MUTE-', '')
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

while True:
    event, values = window.read(timeout=100)
    if event == sg.WINDOW_CLOSED:
        break

    if event in stations.keys():
        radio_player.play_station(event, stations[event], values['-VOLUME-'] / 100)

    if event == '-VOLUME-':
        if radio_player.player.audio_get_mute():
            radio_player.player.audio_set_volume(0)
        else:
            radio_player.play_station(radio_player.station_name, radio_player.station_url, values['-VOLUME-'] / 100)

    if event == '-MUTE-':
        if radio_player.player.audio_get_mute():
            radio_player.player.audio_toggle_mute()
            window['-MUTE-'].update('Mute')
        else:
            radio_player.player.audio_toggle_mute()
            window['-MUTE-'].update('Unmute')
    if event == '-PLAY-RANDOM-':
        random_key = random.choice(list(stations.keys()))
        radio_player.play_station(random_key, stations[random_key], values['-VOLUME-'] / 100)

window.close()