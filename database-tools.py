import xml.etree.ElementTree
import sys
import copy

#keeping <music><difficulty><fumen_*><difnum> and <playable> together
class fumen:
    difficulty = 0
    playable = -1

#use this for more sane-looking handling of songs when they're in xml format'
class XMLSong:
    def __init__(self, musicTag: xml.etree.ElementTree.Element):
        self.musicTagElement = musicTag

        """
        self._title_name = musicTag.find("info").find("title_name").text
        self._title_yomigana = musicTag.find("info").find("title_yomigana").text
        self._artist_name = musicTag.find("info").find("artist_name").text
        self._artist_yomigana = musicTag.find("info").find("artist_yomigana").text
        self._bpm_max = musicTag.find("info").find("bpm_max").text
        self._bpm_min = musicTag.find("info").find("bpm_min").text
        self._distribution_date = musicTag.find("info").find("distribution_date").text
        self._volume = musicTag.find("info").find("volume").text
        self._bg_no = musicTag.find("info").find("bg_no").text
        self._region = musicTag.find("info").find("region").text
        self._limitation_type = musicTag.find("info").find("limitation_type").text
        self._price = musicTag.find("info").find("price").text
        self._genre = musicTag.find("info").find("genre").text
        self._play_video_flags = musicTag.find("info").find("play_video_flags").text
        self._is_fixed = musicTag.find("info").find("is_fixed").text
        self._version = musicTag.find("info").find("version").text
        self._demo_pri = musicTag.find("info").find("demo_pri").text
        self._license = musicTag.find("info").find("license").text
        self._color1 = musicTag.find("info").find("color1").text
        self._color1 = musicTag.find("info").find("color2").text
        self._color3 = musicTag.find("info").find("color3").text

        self._singleEasy = None
        self._singleHard = None
        self._versusEasy = None
        self._versusHard = None
        """

    @property
    def title_name(self):
        return self.musicTagElement.find("info").find("title_name").text
    @title_name.setter
    def title_name(self, value):
        self.musicTagElement.find("info").find("title_name").text = value

    @property
    def title_yomigana(self):
        return self.musicTagElement.find("info").find("title_yomigana").text
    @title_yomigana.setter
    def title_yomigana(self, value):
        self.musicTagElement.find("info").find("title_yomigana").text = value

    @property
    def artist_name(self):
        return self.musicTagElement.find("info").find("artist_name").text
    @artist_name.setter
    def artist_name(self, value):
        self.musicTagElement.find("info").find("artist_name").text = value

    @property
    def artist_yomigana(self):
        return self.musicTagElement.find("info").find("artist_yomigana").text
    @artist_yomigana.setter
    def artist_yomigana(self, value):
        self.musicTagElement.find("info").find("artist_yomigana").text = value

    @property
    def bpm_max(self):
        return self.musicTagElement.find("info").find("bpm_max").text
    @bpm_max.setter
    def bpm_max(self, value):
        self.musicTagElement.find("info").find("bpm_max").text = value

    @property
    def bpm_min(self):
        return self.musicTagElement.find("info").find("bpm_min").text
    @bpm_min.setter
    def bpm_min(self, value):
        self.musicTagElement.find("info").find("bpm_min").text = value

    @property
    def distribution_date(self):
        return self.musicTagElement.find("info").find("distribution_date").text
    @distribution_date.setter
    def distribution_date(self, value):
        self.musicTagElement.find("info").find("distribution_date").text = value

    @property
    def volume(self):
        return self.musicTagElement.find("info").find("volume").text
    @volume.setter
    def volume(self, value):
        self.musicTagElement.find("info").find("volume").text = value

    @property
    def bg_no(self):
        return self.musicTagElement.find("info").find("bg_no").text
    @bg_no.setter
    def bg_no(self, value):
        self.musicTagElement.find("info").find("bg_no").text = value

    @property
    def region(self):
        return self.musicTagElement.find("info").find("region").text
    @region.setter
    def region(self, value):
        self.musicTagElement.find("info").find("region").text = value

    @property
    def limitation_type(self):
        return self.musicTagElement.find("info").find("limitation_type").text
    @limitation_type.setter
    def limitation_type(self, value):
        self.musicTagElement.find("info").find("limitation_type").text = value

    @property
    def price(self):
        return self.musicTagElement.find("info").find("price").text
    @price.setter
    def price(self, value):
        self.musicTagElement.find("info").find("price").text = value

    @property
    def genre(self):
        return self.musicTagElement.find("info").find("genre").text
    @genre.setter
    def genre(self, value):
        self.musicTagElement.find("info").find("genre").text = value

    @property
    def play_video_flags(self):
        return self.musicTagElement.find("info").find("play_video_flags").text
    @play_video_flags.setter
    def play_video_flags(self, value):
        self.musicTagElement.find("info").find("play_video_flags").text = value

    @property
    def is_fixed(self):
        return self.musicTagElement.find("info").find("is_fixed").text
    @is_fixed.setter
    def is_fixed(self, value):
        self.musicTagElement.find("info").find("is_fixed").text = value

    @property
    def version(self):
        return self.musicTagElement.find("info").find("version").text
    @version.setter
    def version(self, value):
        self.musicTagElement.find("info").find("version").text = value

    @property
    def version(self):
        return self.musicTagElement.find("info").find("version").text
    @version.setter
    def version(self, value):
        self.musicTagElement.find("info").find("version").text = value

    @property
    def demo_pri(self):
        return self.musicTagElement.find("info").find("demo_pri").text
    @demo_pri.setter
    def demo_pri(self, value):
        self.musicTagElement.find("info").find("demo_pri").text = value

    @property
    def license(self):
        return self.musicTagElement.find("info").find("license").text
    @license.setter
    def license(self, value):
        self.musicTagElement.find("info").find("license").text = value

    @property
    def color1(self):
        return self.musicTagElement.find("info").find("color1").text
    @color1.setter
    def color1(self, value):
        self.musicTagElement.find("info").find("color1").text = value

    @property
    def color2(self):
        return self.musicTagElement.find("info").find("color2").text
    @color2.setter
    def color2(self, value):
        self.musicTagElement.find("info").find("color2").text = value

    @property
    def color3(self):
        return self.musicTagElement.find("info").find("color3").text
    @color3.setter
    def color3(self, value):
        self.musicTagElement.find("info").find("color3").text = value

#Get the last song ID excluding tutorial songs (start at id 90000)
def getLastID(rootTag: xml.etree.ElementTree.Element):
    lastID = -1
    for song in rootTag:
        if lastID < int(song.attrib["id"]) and int(song.attrib["id"]) < 90000:
            lastID = int(song.attrib["id"])

    return lastID

#Since songs get removed, IDs do not necessarily reflect their index in the database. Returns -1 if the ID is not found
def getIndexOfID(rootTag: xml.etree.ElementTree.Element, id):
    index = -1
    for song in rootTag:
        index += 1
        if song.attrib["id"] == str(id):
            return index

    return index

#Append a song to the end of the songlist but before the tutorials, assigning it an id that is one greater than the last song
def appendSong(rootTag: xml.etree.ElementTree.Element, songToAppend: xml.etree.ElementTree.Element):
    if rootTag.tag != "mdb":
        print("Invalid root tag")
        return

    newSong = copy.deepcopy(songToAppend)
    newSong.attrib["id"] = str(getLastID(rootTag) + 1)
    rootTag.insert(getIndexOfID(rootTag, getLastID(rootTag)) + 1, newSong)

database = xml.etree.ElementTree.parse(sys.argv[1])

music = database.getroot()

if music.tag != "mdb":
    print("Database root tag is not 'mdb', is this a Dancerush database?")
    exit()

def test():
    song = XMLSong(music[0])
    print(song.title_name)
    print(song.title_yomigana)
    print(song.artist_name)
    print(song.artist_yomigana)
    print(song.bpm_max)
    print(song.bpm_min)
    print(song.distribution_date)
    print(song.volume)
    print(song.bg_no)
    print(song.region)
    print(song.limitation_type)
    print(song.price)
    print(song.genre)
    print(song.play_video_flags)
    print(song.is_fixed)
    print(song.version)
    print(song.demo_pri)
    print(song.license)
    print(song.color1)
    print(song.color2)
    print(song.color3)

    song.title_name = "bitch song"
    song.title_yomigana = "bichi uta"
    song.artist_name = "hoe"
    song.artist_yomigana = "ho"
    song.bpm_max = "420"
    song.bpm_min = "69"
    song.distribution_date = "today bitch"
    song.volume = "9001"
    song.bg_no = "573"
    song.region = "the republic of ligma"
    song.limitation_type = "9999"
    song.price = "one hundred emoji"
    song.genre = "69"
    song.play_video_flags = "hello"
    song.is_fixed = "song broke"
    song.version = ":3"
    song.demo_pri = "999"
    song.license = "you got a license for that song"
    song.color1 = "0xff694200"
    song.color2 = "0xff696969"
    song.color3 = "0x12345678"

    #First song should now contain all those attributes

    appendSong(database.getroot(), music[0])

    #Duplicate of the first song should now be appended to the end of the database with an appropriate ID, while the ID of the original should not have changed

    database.write("database-modified-test.xml")

test()
