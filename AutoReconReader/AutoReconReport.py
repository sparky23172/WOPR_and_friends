import os
import re
import logging


logging.basicConfig(level=logging.DEBUG)

def checks():
    # Checking to see if the expected directories are found
    logging.debug("Checking directories for files")
    reportDir = os.listdir("report")
    exploitDir = os.listdir("exploit")
    lootDir = os.listdir("loot")
    scansDir = os.listdir("scans")

    # Print raw ls
    logging.debug("\n\nReport: {}\nExploit: {}\nLoot: {}\nScans: {}".format(reportDir, exploitDir, lootDir, scansDir))


    if reportDir:
        logging.info("Report has content")
        logging.info("Please note, there aren't any command assosiated with this folder yet")
    else:
        pass

    if exploitDir:
        logging.info("Exploit has content")
        logging.info("Please note, there aren't any command assosiated with this folder yet")
    else:
        pass

    if lootDir:
        logging.info("Loot has content")
        logging.info("Please note, there aren't any command assosiated with this folder yet")
    else:
        pass

    if scansDir:
        logging.info("Scans has content")
        scans(scansDir)
    else:
        pass

def scans(scansDir):
    logging.info("Entering scans directory")
    logging.debug(scansDir)
    
    # Variables for information
    versionsAll = {}
    feroxbusterAll = {}
    commentAll = []
    robot = False

    if "_full_tcp_nmap.txt" in scansDir:
        print("\n\n")
        logging.info("Scanning _full_tcp_nmap.txt for versions\n")
        f = open("scans/_full_tcp_nmap.txt", "r")
        file = f.readlines()
        for line in file:
            # logging.debug(line)

            # Grab Port, service running, and version
            versions = re.findall("(\d+)\/.+?\s+\w+\s+(\w+)\s+[a-z-A-Z]+\s+(.+)\n",line)
            if versions:
                # logging.debug(versions)
                versionsAll[versions[0][0]] = {"port":versions[0][0],"service":versions[0][1],"version":versions[0][2]}
                logging.debug(versions)
        f.close()

    for things in scansDir:
        if "feroxbuster.txt" in things:
            print("\n\n")
            logging.info("Grabbing feroxbuster information\n")
            for ferox in scansDir:
                if "feroxbuster.txt" in ferox:
                    f = open("scans/{}".format(ferox), "r")
                    file = f.readlines()
                    for line in file:
                        directory = re.findall("(\d+).+?\d+\w+\s+\d+\w+\s+(http.+)",line)
                        smallDir = re.findall(".+/(.+)$",str(directory[0][1]))
                        logging.info("Directory Found: {}".format(smallDir[0]))
                        logging.info("Whole URL: {}\n".format(directory[0][1]))

                        feroxbusterAll[smallDir[0]] = {"dir": smallDir[0], "url": directory[0][1], "status_code":directory[0][0]}
                        # print(line)
                    f.close()
                else:
                    pass

        if "http_index.html" in things:
            print("\n\n")
            logging.info("Looking for comments in index.html\n")
            for index in scansDir:
                if "http_index.html" in index:
                    f = open("scans/{}".format(index), "r")
                    file = f.readlines()
                    for line in file:
                        comment = re.findall("(\<\!\-\-.+?\-\-\>)",line)
                        if comment:
                            commentAll.append(comment)
                            print(comment)
                    f.close()


        if "robots.txt" in things:
            print("\n\n")
            logging.info("Looking for robots.txt\n")
            for index in scansDir:
                if "robots.txt" in index:
                    f = open("scans/{}".format(index), "r")
                    file = f.readlines()
                    for line in file:
                        comment = re.findall("HTTP\/1\.\d{1}\s+(\d{3})",line)
                        if comment:
                            status = re.findall("(40\d|50\d)",comment[0])
                            if status:
                                logging.info("Robots.txt page not found")
                            else:
                                logging.info("Robots.txt page found. Please check")
                                robot = True

                    f.close()



    logging.debug(versionsAll)
    logging.debug(feroxbusterAll)
    logging.debug(commentAll)
    logging.debug("Robots.txt page found: {}".format(robot))

def main():
    print("Whats up!")

    curdir = os.listdir()
    if "report" in curdir and "exploit" in curdir and "loot" in curdir and "scans" in curdir:
        logging.debug("We in it")
        checks()
    else:
        logging.fatal("Please put me in the directory that has AutoRecon's output. I can not find it here.... \nCurrent Location: {}".format(os.getcwd()))


if __name__ ==  "__main__":
    main()

