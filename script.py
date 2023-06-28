import subprocess
import os
import sys
from tidalapi.page import PageItem, PageLink
from tidalapi.mix import Mix
import tidalapi

session = tidalapi.Session()

login, future = session.login_oauth()
subprocess.run(["firefox", login.verification_uri_complete])

future.result()

i = 0
certainIds = open("certain_ids.txt", "w") #Clears the file everytime the script runs
uncertainIds = open("uncertain_ids.txt", "w") #Clears the file everytime the script runs
uncertainAlbums = open("uncertain_albums.txt", "w") #Clears the file everytime the script runs
notFound = open("not_found.txt", "w") #Clears the file everytime the script runs

for artist in os.listdir(sys.argv[1]):
    for a in os.listdir(sys.argv[1] + artist):
        album = a[0:a.find("[") - 1]
        if "-" in album:
            print(album)
        year = a[a.find("[") + 1:a.find("]")]
        home = session.search(artist + " " + album)
        if len(home["albums"]) > 0:
            any = False
            for element in home["albums"]:
                if element.name == album and element.year == int(year) and element.artist.name == artist:
                    print(element.id, end = " ", file = certainIds)
                    i += 1
                    any = True
                    break

            if not any:
                home = session.search(album)
                if len(home["albums"]) > 0:
                    any = False
                    for element in home["albums"]:
                        if element.name == album and element.year == int(year):
                            print(element.id, end = " ", file = uncertainIds)
                            print("Tidal:", element.artist.name + " - " + element.name, "\t\t\tActual:", artist + " - " + album, file = uncertainAlbums)
                            any = True
                            i += 1
                            break
                    
                    if not any:
                        print(artist + " - " + album, file = notFound)
                else:
                    print(artist + " - " + album, file = notFound)
        else:
            home = session.search(album)
            if len(home["albums"]) > 0:
                any = False
                for element in home["albums"]:
                    if element.name == album and element.year == int(year):
                        print(element.id, end = " ", file = uncertainIds)
                        print("Tidal:", element.artist.name + " - " + element.name, "\t\t\tActual:", artist + " - " + album, file = uncertainAlbums)
                        any = True
                        i += 1
                        break
                if not any:
                    print(artist + " - " + album, file = notFound)
            else:
                print(artist + " - " + album, file = notFound)

                

certainIds.close()
uncertainIds.close()
uncertainAlbums.close()
notFound.close()
print(i)
