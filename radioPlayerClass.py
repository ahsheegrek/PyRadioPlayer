import vlc
import streamlink

#ラジオ局の再生とボリューム調整
class RadioPlayer:
    def __init__(self, window):
        self.instance = vlc.Instance("--no-video") # 映像は再生されないようにする
        self.player = self.instance.media_player_new()
        self.station_url = None
        self.station_name = None
        self.window = window

    def play_station(self, station_name, station_url, volume):
        if self.station_url != station_url:
            self.stop_station()
            self.station_url = station_url
            if "youtube.com" in self.station_url: # YouTube Liveの場合
                streams = streamlink.streams(self.station_url)
                stream_url = streams['audio'].url if 'audio' in streams else streams['best'].url
                
                media = self.instance.media_new(stream_url)
                self.player.set_media(media)
            elif "radiko.jp" in self.station_url: #radikoの場合
                streams = streamlink.streams(self.station_url)
                stream_url = streams['best'].url
                
                media = self.instance.media_new(stream_url)
                self.player.set_media(media)
            else: #その他普通のインターネットラジオの場合
                media = self.instance.media_new(station_url)
            self.player.set_media(media)
            self.station_name = station_name
        self.player.play()
        self.player.audio_set_volume(int(volume * 100))
        
        self.window['-CURRENT-STATION-'].update(f'{station_name}') #Now Playingに現在の再生局を表示

    def stop_station(self):
        if self.player.is_playing():
            self.player.stop()