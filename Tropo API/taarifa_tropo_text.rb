require 'json'
require 'restclient'
require 'net/http'
require 'uri'


myCallerID = $currentCall.callerID.to_s
myCalledID = $currentCall.calledID.to_s
wpid = ''                                #variable for the waterID
wpstatus = ''                            #variable for the waterpoint status
wpdamage = ''

#automatic response for incoming text message
say "Thank you for messaging the water point reporting system."


ask "What is the service code.",{       #request information from the caller
  :choices => "[5 DIGITS]",
  :onChoice => lambda { |response|
    wpid = result.value					       #users response to the id question (response.value?)
    },
  :onBadChoice => lambda { |event|
    say "That was not an option"
    },
}

ask "What is the water point status. Press one for working, two for broken.",{
  :choices => "broken, working"
  :onChoice => lambda { |response|
    wpstatus = result.value					       #users response to the id question (response.value?)
    },
  :onBadChoice => lambda { |event|
  say "That was not an option"
  },
}

result = ask "What is the status of the waterpoint? Choose from tab missing or container broken or other", {
  :choices => "tab missing, broken, other"
  :onChoice => lambda { |response|
    wpdamage = result.value
    },
  :onBadChoice => lambda { |event|
    say "That was not an option"
  },
}

message "Thank you for your water point report.", {
  :to => $currentCall.callerID,                            #according to the Tropo documentation it is currently not possible to message back to callerID :(
  :network => 'SMS'                                        #omit this line of code to send a voice mail instead
}

#parsing out info to server

url = "http://444a1993.ngrok.com"
uri = URI.parse(url)
data = {"service_code"=>"wps001","device_id"=>wpid,"status"=>wpstatus,"service_notice"=>wpdamage}
postData=Net::HTTP.post_form(URI.parse('http://444a1993.ngrok.com'),{'data'=>jsonData})

# RestClient.post 'http://localhost:5000/api/requests', { "service_code" => "wps001", "device_id" => wpid,  "status" => wpstatus, "service_notice" => wpdamage }.to_json
