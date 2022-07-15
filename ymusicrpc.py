import pypresence
from yandex_music import Client
import configparser

client_id = "978995592736944188"


def get_track():
    try:
        queues = client.queues_list()
        last_queue = client.queue(queues[0].id)
        track_id = last_queue.get_current_track()
        track = track_id.fetch_track()
        return track
    except Exception as e:
        return 0


def get_label():
    try:
        track = get_track()
        title = track.title
        return f"{title}"
    except Exception as e:
        return "No track"


def get_artists():
    try:
        track = get_track()
        artists = "".join(track.artists_name())
        return f"{artists}"
    except Exception as e:
        return "No track"


config = configparser.ConfigParser()
config.read("cfg.ini")
if config.get("yandex", "token") == "None":
    print("Edit token in config.ini")
else:
    TOKEN = config.get("token", "token")

client = Client(TOKEN).init()
curr = get_label()

RPC = pypresence.Presence(client_id)
RPC.connect()
RPC.update(
    details=get_label(),
    state=get_artists(),
    large_image="og-image",
    large_text="Y.M",
)
print(get_label(), "-", get_artists())

while True:
    if get_label() != curr:
        RPC.update(
            details=get_label(),
            state=get_artists(),
            large_image="og-image",
            large_text="Y.M",
        )
        print(get_label(), "-", get_artists())
        curr = get_label()
