package main

import (
        "encoding/csv"
        "flag"
        "io"
        "os"
        "os/exec"
        "regexp"
        "runtime"
        "strings"

        "github.com/rs/zerolog"
        "github.com/rs/zerolog/log"
)

//Levels of Logging

//panic (zerolog.PanicLevel, 5)
//fatal (zerolog.FatalLevel, 4)
//error (zerolog.ErrorLevel, 3)
//warn (zerolog.WarnLevel, 2)
//info (zerolog.InfoLevel, 1)
//debug (zerolog.DebugLevel, 0)
//trace (zerolog.TraceLevel, -1)

type DirInfo struct {
        IP_Address string
        Directory  string
        Status     string
}

func grabCSV(fileName string, wordlist string, extent string, fileOut string) {
        m := make(map[string]string)
        
        // Open the file
        csvfile, err := os.Open(fileName)
        if err != nil {
                log.Fatal().Msgf("Couldn't open the csv file: %s", err)
        }

        // Parse the file
        r := csv.NewReader(csvfile)

        // Iterate through the records
        for {
                // Read each record from csv
                record, err := r.Read()
                if err == io.EOF {
                        break
                }
                if err != nil {
                        log.Fatal().Msgf("%s", err)
                }
                log.Debug().Msgf("What is here : %s", record[0])
                m[record[0]] = "Test"
        }

        csvFile, csvError := os.Create(fileOut)

        if err != nil {
                log.Error().Msgf("%s", csvError)
        }
        defer csvFile.Close()

        writer := csv.NewWriter(csvFile)

        var header []string
        header = append(header, "Target IP Address")
        header = append(header, "Directory found")
        header = append(header, "Status code of Directory")
        writer.Write(header)
        writer.Flush()

        for k, _ := range m {
                log.Info().Msgf("Address attempting: %s", k)
                execute(k, wordlist, extent, writer)
        }
}
func execute(ipAddress string, wordlist string, extensions string, writer *csv.Writer) {
        m := make(map[string]DirInfo)

        wordList := ""

        //Checks for wordlist locations
        if wordlist != "" {
                wordList = wordlist
        } else {
                wordList = "/usr/share/SecLists/Discovery/Web-Content/api/api-seen-in-wild.txt"
        }

        //Wordlist being used
        log.Debug().Msgf("Wordlist being used: %s", wordList)

        //Checks for extensions to look for with list
        if extensions != "" {
        } else if (extensions == "None") {
                extensions = "''"
        } else {
                extensions = ".csv,.db,.dbf,.log,.sql,.xml,.exe,.ppt,.pptx,.xls,.xlsx,.bak,.tmp,.doc,.docx,.txt,.pdf"
        }
        
        //Command to do bruteforce
        out, err := exec.Command("gobuster", "dir", "-w", wordList, "-x", extensions, "-u", ipAddress, "--help").Output()
        if err != nil {
                log.Error().Msgf("%s", err)
                log.Error().Msgf("%s", out)
        }

        log.Debug().Msg("Command Successfully Executed")

        //Change output to something parsable
        output := string(out[:])
        outputs := strings.Split(output, "\n")

        //Checks for directory and status code
        re, _ := regexp.Compile(`^(.+?)\s+\(Status\:\s+(\d+)\)`)

        //Loops through all output for data
        for _, v := range outputs {
                if v != "" {
                        log.Debug().Msgf("Raw Data: %s", v)
                        if len(re.FindStringIndex(v)) > 0 {
                                log.Info().Msgf("Directory: %q\tStatus: %q", re.FindStringSubmatch(v)[1], re.FindStringSubmatch(v)[2])
                                //Stores data uniquely for output
                                m[ipAddress+"\\"+re.FindStringSubmatch(v)[1]] = DirInfo{IP_Address: ipAddress, Status: re.FindStringSubmatch(v)[2], Directory: re.FindStringSubmatch(v)[1]}
                        }
                }
        }

        //Writes to a csv
        for _, usance := range m {
                var row []string
                row = append(row, usance.IP_Address)
                row = append(row, usance.Directory)
                row = append(row, usance.Status)
                writer.Write(row)
        }
        writer.Flush()

}

func main() {
        //Setup the logger to show time and a nice color
        log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})

        //Welcome message
        log.Info().Msg("Hello to DirBrute!\n")

        //Grabs flags
        wordlistPath := flag.String("w", "", "Path to wordlist")
        extensions := flag.String("x", "", "Add different file extenstions not included by default (.csv,.db,.dbf,.log,.sql,.xml,.exe,.ppt,.pptx,.xls,.xlsx,.bak,.tmp,.doc,.docx,.txt,.pdf)\nUse 'None' if you do not want to use any extensions")
        csvIn := flag.String("I", "", "CSV file for injestion")
        csvOut := flag.String("O", "", "CSV file for exporting")
        debug := flag.Bool("d", false, "Turn Debugging on")
        //Make it into something usable
        flag.Parse()

        //Set Logging level
        zerolog.SetGlobalLevel(zerolog.InfoLevel)
        if *debug {
                zerolog.SetGlobalLevel(zerolog.DebugLevel)
        }

        //Flag Debugs
        log.Debug().Msgf("\nPath to wordlist: %s\nExtenstions: %s\nCSV Input location: %s\nCSV Output location: %s", *wordlistPath, *extensions, *csvIn, *csvOut)

        log.Debug().Msgf("Checking OS...")
        switch os := runtime.GOOS; os {
        case "darwin":
                log.Fatal().Msg("Running on OS X. I do not know how to run on this system. Exiting")
        case "linux":
                log.Info().Msg("Running on Linux. Continuing Program")
        default:
                log.Fatal().Msgf("%s. I do not know how to run on this system. Exiting\n", os)
        }
        grabCSV(*csvIn, *wordlistPath, *extensions, *csvOut)
}
