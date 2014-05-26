require 'json'
require 'restclient'
require 'net/http'
require 'uri'


myCallerID = $currentCall.callerID.to_s
myCalledID = $currentCall.calledID.to_s
wpid = ''                                #variable for the waterID
wpstatus = ''                            #variable for the waterpoint status
wpdamage = ''

#wait(200)

say "Thank you for calling the water point reporting system."

say "question one"

ask "What is the service code.",       #request information from the caller
{
    :choices => "[5 DIGITS]",     				  #define choices for caller
    :terminator => '#',
    :timeout => 15.0,                    #waits for 15 seconds before hanging up automatically
    :mode => "dtmf",                      #responses are collected by touch-tone input or 'speech' or 'any'
    :interdigitTimeout => 5,              #timeout between digits entered, triggers onBadChoice
    :attempts => 3,                      #will ask 3 times and wait timeout between requests before nomatch or noinput
 #   :bargein => 'true',                   #allows the user to interrupt the TTS/ audio output
    :onChoice => lambda { |response|
        wpid = result.value					       #users response to the id question (response.value?)
        say "You entered" + result.value
    },
    :onBadChoice => lambda { |response|
        say "Sorry, I didn't get that."
    },
}

say "question two"

ask "What is the water point status. Press one for working, two for broken.",
{
    :choices => "1,2",
    :terminator => '#',
    :timeout => 15.0,
    :mode => "dtmf",
#    :interdigitTimeout => 5,
#    :attempts => 3,
#    :bargein => 'true',
    :onChoice => lambda { |response|
        wpstatus = result.value
        say "You entered" + result.value
    },
    :onBadChoice => lambda { |wpstatus|
        say "Sorry, I didn't get that."
    },
}

say "question 3"

result = ask "What is wrong with the waterpoint. Press one for tab missing, two for cracked container, three for other.",
{
  :choices => "1,2,3",
  :terminator => '#',
  :timeout => 20.0,
  :mode => "dtmf",
#  :interdigitTimeout => 5,
#  :attempts => 3,
#  :bargein => 'false',
  :onChoice => lambda { |response|
      wpdamage = result.value
      say "You entered" + result.value
    },
    :onBadChoice => lambda { |wpdamage|
      say "Sorry, I didn`t get that."
    },
}

  #got this far reliably

  message "Thank you for your water point report.", {
    :to => $currentCall.callerID,                            #according to the Tropo documentation it is currently not possible to message back to callerID :(
    :network => 'SMS'                                        #omit this line of code to send a voice mail instead
    #can just say "say something …………"
  }

url = "http://444a1993.ngrok.com"
uri = URI.parse(url)
data = {"service_code"=>"wps001","device_id"=>wpid,"status"=>wpstatus,"service_notice"=>wpdamage}
postData=Net::HTTP.post_form(URI.parse('http://444a1993.ngrok.com'),{'data'=>jsonData})

# RestClient.post 'http://localhost:5000/api/requests', { "service_code" => "wps001", "device_id" => wpid,  "status" => wpstatus, "service_notice" => wpdamage }.to_json


if wpstatus == '1'
   say "Thank you for your report. Water Point " + wpstatus + " is now reported as working. Drink up!"
   wpstatus = 'Working'
else
   say "Thank you for your report. Water Point " + wpstatus + " is now reported as broken. Sad face."
   wpstatus = 'Broken'
end

# This next part was just for demo

"

# message "New report from:" + myCallerID + " WaterPoint ID: " + wpid + " Status: "+ wpstatus, {
  #  :to => "+12155555555",
  #  :network => 'SMS'}
