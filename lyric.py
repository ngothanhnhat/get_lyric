# -*- coding: utf-8 -*-
from urllib import request
import chilkat
import codecs
import sys

if __name__ == "__main__":

    # Get url to redirect info song
    args = sys.argv
    url_song = args[1]

    filname = url_song.split(".")[-3].split("/")[-1]
    # url_song = "https://www.nhaccuatui.com/bai-hat/ngam-hoa-le-roi-chau-khai-phong.8eytB4JZeCWk.html"
    key = 'player.peConfig.xmlURL = "'

    fp = request.urlopen(url_song)
    mybytes = fp.read()
    script = mybytes.decode("utf8")
    fp.close()

    s_pos = script.find(key) + len(key)
    e_pos = script.find('";', s_pos)
    url = script[s_pos:e_pos]

    # Get url to download file
    fp = request.urlopen(url)
    mybytes = fp.read()

    res_str = mybytes.decode("utf8")
    fp.close()
    key = "<lyric><![CDATA["
    s_pos = res_str.find(key) + len(key)
    e_pos = res_str.find(']]></lyric>', s_pos)
    lyric_url = res_str[s_pos:e_pos]

    fp = request.urlopen(lyric_url)
    mybytes = fp.read()

    lyric_hex = mybytes.decode("utf8")
    fp.close()

    crypt = chilkat.CkCrypt2()

    success = crypt.UnlockComponent("Anything for 30-day trial")
    if (success != True):
        print("Crypt component unlock failed")
    else:
        crypt.put_CryptAlgorithm('arc4')
        crypt.put_EncodingMode("hex")
        crypt.put_Charset("utf-8")

        lyric_key = "Lyr1cjust4nct".encode('utf-8')
        lyric_key_hex = lyric_key.hex()

        crypt.SetEncodedKey(lyric_key_hex, "hex")
        crypt.put_KeyLength(104)

        lyric = crypt.decryptStringENC(lyric_hex)

        f = codecs.open(filname+".lrc", "w+", "utf-8")
        f.write(lyric)
        f.close()