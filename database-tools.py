import xml.etree.ElementTree
import sys
import copy

#usage:
#The caller maintains its own xml.etree.ElementTree instance representing the entire file, and must call .write(...) itself to save changes made
#Functions generally operate on individual XML tags represented as xml.etree.ElementTree.Element objects

class XMLFumen:
    def __init__(self, fumenTag: xml.etree.ElementTree.Element):
        self.fumenTagElement = fumenTag

    @property
    def difnum(self):
        return self.fumenTagElement.find("difnum").find("bg_no").text
    @difnum.setter
    def difnum(self, value):
        self.fumenTagElement.find("difnum").text = value

    @property
    def playable(self):
        return self.fumenTagElement.find("playable").find("bg_no").text
    @playable.setter
    def playable(self, value):
        self.fumenTagElement.find("playable").text = value


#Handles an individual <music> tag
class XMLSong:
    def __init__(self, musicTag: xml.etree.ElementTree.Element):
        self.musicTagElement = musicTag

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


    @property
    def singleEasy(self):
        return XMLFumen(self.musicTagElement.find("difficulty").find("fumen_1b"))

    @property
    def singleHard(self):
        return XMLFumen(self.musicTagElement.find("difficulty").find("fumen_1a"))

    @property
    def versusEasy(self):
        return XMLFumen(self.musicTagElement.find("difficulty").find("fumen_2b"))

    @property
    def versusHard(self):
        return XMLFumen(self.musicTagElement.find("difficulty").find("fumen_2a"))


#Get the last song ID in the DB excluding tutorial songs (which start at id 90000)
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


#Append a song (as an ElementTree.Element object) to the end of the songlist but before the tutorials, assigning it a new id that is one greater than the last song
def appendSong(rootTag: xml.etree.ElementTree.Element, songToAppend: xml.etree.ElementTree.Element):
    if rootTag.tag != "mdb":
        print("Invalid root tag")
        return

    newSong = copy.deepcopy(songToAppend)
    newSong.attrib["id"] = str(getLastID(rootTag) + 1)
    rootTag.insert(getIndexOfID(rootTag, getLastID(rootTag)) + 1, newSong)

#Create a <music> with no data filled in. Returns an ElementTree.Element instance of the new <music>
def createEmptySongEntry(rootTag: xml.etree.ElementTree.Element):
    newSong = xml.etree.ElementTree.Element("music", {"id": "-1"})

    infoTag = xml.etree.ElementTree.SubElement(newSong, "info")
    xml.etree.ElementTree.SubElement(infoTag, "title_name", {"__type": "str"})
    xml.etree.ElementTree.SubElement(infoTag, "title_yomigana", {"__type": "str"})
    xml.etree.ElementTree.SubElement(infoTag, "artist_name", {"__type": "str"})
    xml.etree.ElementTree.SubElement(infoTag, "artist_yomigana", {"__type": "str"})
    xml.etree.ElementTree.SubElement(infoTag, "bpm_max", {"__type": "u32"})
    xml.etree.ElementTree.SubElement(infoTag, "bpm_min", {"__type": "u32"})
    xml.etree.ElementTree.SubElement(infoTag, "distribution_date", {"__type": "u32"})
    xml.etree.ElementTree.SubElement(infoTag, "volume", {"__type": "u16"})
    xml.etree.ElementTree.SubElement(infoTag, "bg_no", {"__type": "u16"})
    xml.etree.ElementTree.SubElement(infoTag, "region", {"__type": "str"})
    xml.etree.ElementTree.SubElement(infoTag, "limitation_type", {"__type": "u8"})
    xml.etree.ElementTree.SubElement(infoTag, "price", {"__type": "s32"})
    xml.etree.ElementTree.SubElement(infoTag, "genre", {"__type": "u32"})
    xml.etree.ElementTree.SubElement(infoTag, "play_video_flags", {"__type": "u32"})
    xml.etree.ElementTree.SubElement(infoTag, "is_fixed", {"__type": "u8"})
    xml.etree.ElementTree.SubElement(infoTag, "version", {"__type": "u8"})
    xml.etree.ElementTree.SubElement(infoTag, "demo_pri", {"__type": "u8"})
    xml.etree.ElementTree.SubElement(infoTag, "license", {"__type": "str"})
    xml.etree.ElementTree.SubElement(infoTag, "color1", {"__type": "u32"})
    xml.etree.ElementTree.SubElement(infoTag, "color2", {"__type": "u32"})
    xml.etree.ElementTree.SubElement(infoTag, "color3", {"__type": "u32"})

    difficultyTag = xml.etree.ElementTree.SubElement(newSong, "difficulty")
    fumen_1b = xml.etree.ElementTree.SubElement(difficultyTag, "fumen_1b")
    xml.etree.ElementTree.SubElement(fumen_1b, "difnum", {"__type": "u8"})
    xml.etree.ElementTree.SubElement(fumen_1b, "playable", {"__type": "u8"})

    fumen_1a = xml.etree.ElementTree.SubElement(difficultyTag, "fumen_1a")
    xml.etree.ElementTree.SubElement(fumen_1a, "difnum", {"__type": "u8"})
    xml.etree.ElementTree.SubElement(fumen_1a, "playable", {"__type": "u8"})

    fumen_2b = xml.etree.ElementTree.SubElement(difficultyTag, "fumen_2b")
    xml.etree.ElementTree.SubElement(fumen_2b, "difnum", {"__type": "u8"})
    xml.etree.ElementTree.SubElement(fumen_2b, "playable", {"__type": "u8"})

    fumen_2a = xml.etree.ElementTree.SubElement(difficultyTag, "fumen_2a")
    xml.etree.ElementTree.SubElement(fumen_2a, "difnum", {"__type": "u8"})
    xml.etree.ElementTree.SubElement(fumen_2a, "playable", {"__type": "u8"})

    conditionsTag = xml.etree.ElementTree.SubElement(newSong, "conditions")

    return newSong


def test():
    database = xml.etree.ElementTree.parse(sys.argv[1])
    music = database.getroot()

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

    #Generate a completely new <music>
    newSong = XMLSong(createEmptySongEntry(database.getroot()))
    newSong.title_name = "new song"
    newSong.title_yomigana = "nyuu songu"
    newSong.artist_name = "john konami"
    newSong.artist_yomigana = "ja-n 573"
    newSong.bpm_max = "573"
    newSong.bpm_min = "573"
    newSong.distribution_date = "12345678"
    newSong.volume = "1234"
    newSong.bg_no = "573"
    newSong.region = "J"
    newSong.limitation_type = "5"
    newSong.price = "40"
    newSong.genre = "8"
    newSong.play_video_flags = "hi"
    newSong.is_fixed = "1"
    newSong.version = ":33333"
    newSong.demo_pri = "69"
    newSong.license = "licensde!!"
    newSong.color1 = "0xff694200"
    newSong.color2 = "0xff696969"
    newSong.color3 = "0x12345678"
    newSong.singleEasy.difnum = "3"
    newSong.singleEasy.playable = "1"
    newSong.singleHard.difnum = "900"
    newSong.singleHard.playable = "1"
    newSong.versusEasy.difnum = "5"
    newSong.versusEasy.playable = "2 (extremely playable)"
    newSong.versusHard.difnum = "90000"
    newSong.versusHard.playable = "0"
    appendSong(database.getroot(), newSong.musicTagElement)

    #Duplicate of the first song should now be appended to the end of the database with an appropriate ID, while the ID of the original should not have changed
    #'new song' should be appended after that

    database.write("database-modified-test.xml")

test()
