import requests
import re

print("Absen-Inator 4000 REMASTERED")

attendees = []
numberOfAbsen = 0

# URL variable for changing between different e-learn because they have the same template for some reason

changeo = 'http://elearning.man2kotamalang.sch.id/'


# Variables and shit

mainUrl = changeo + "studentkelas/absensi/"
b = changeo + "login/do_login"

with open("login2", "r") as f:
    c = f.readlines()

usernames = [x for y in c for x in y.split()][::2]
passwords = [x for y in c for x in y.split()][1::2]

# Function to find link

def findLink(txt):
    return re.search("(?P<url>http?://[^\s]+)", txt).group("url")
def findClass(txt):
    return txt.split('"')[5][6:]

for i in range(len(usernames)):
    form = {"ajaran" : "2021",
            "username" : usernames[0],
            "password" : passwords[0]}

    form.update(username = usernames[i])
    form.update(password = passwords[i])


    # Request session to elearn


    with requests.Session() as rs:

        # Login

        post = rs.post(b, data=form)
        if post.text == "student":

            # Get HTML data from homepage

            homepage = changeo + "student"
            home = rs.post(homepage)
            homeHtml = home.text.split("\n")

            # Find class code

            classes = [findLink(x[0:-1])[len(changeo + "studentkelas/me/"):-1] for x in homeHtml[:200]
                        if "studentkelas" in x and "class" in x]


            # Find class names

            classNames = [findClass(x) for x in homeHtml if "studentkelas" in x and "class" in x]

            # Find account name and prints it

            name = [x[x.index('E-Learning - ')+13:x.index('</')-1] for x in home.text.split("\n")[0:10] if "E-Learning" in x][0]
            print(f"{name}")
            attendees.append(name)

            # For loop; Post hadir request to every class in classes

            for c in range(len(classes)):
                print("Hadir di " + classNames[c] + ".")
                hadir = rs.post(mainUrl + classes[c])

            numberOfAbsen += 1
            print(f"Absen on {name} done.\nNumber of classes: {len(classes)}\nCurrent number of people who are attended: {numberOfAbsen}")

        else:
            print("Bruh something wrong, check your login info.")
print(f"List of attendees:")
[print(s) for s in attendees]
print(f"Number of people who are attended : {numberOfAbsen}")
with open("ppl.txt", 'w') as f:
    [f.writelines(x + '\n') for x in attendees]

print("Wi-Fi not connected! ..or something idk I'm not good at this.")

