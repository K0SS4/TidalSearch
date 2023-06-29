import subprocess
import os
import sys
import tidalapi

if len(sys.argv) < 2:
    print("At least 1 argument needed!")
    exit()

session = tidalapi.Session()

login, future = session.login_oauth()
print("Visit:", "https://" + login.verification_uri_complete, "to authenticate.")

future.result()

print()
print("Searching...")
i = 0
certainIds = open("certain_ids.txt", "w") #Clears the file everytime the script runs
uncertainIds = open("uncertain_ids.txt", "w") #Clears the file everytime the script runs
uncertainAlbums = open("uncertain_albums.txt", "w") #Clears the file everytime the script runs
notFound = open("not_found.txt", "w") #Clears the file everytime the script runs

dir = ""
if sys.argv[1][len(sys.argv[1]) - 1] != '/':
    dir = sys.argv[1] + '/'
else:
    dir = sys.argv[1]

for artist in os.listdir(dir):
    for a in os.listdir(dir + artist):
        album = a[0:a.find("[") - 1]
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
print()
print("Found: ", i)
