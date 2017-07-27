require 'open-uri'
require 'nokogiri'
require 'json'
require 'date'

doc = Nokogiri::HTML(open("https://bruz-beers.squarespace.com/eats/"))

trucks = []

doc.css("[class='entry-title-wrapper']").each do |truck|
  truck_info = {}
  truck_info[:name] = truck.at_css("a").content
  truck_info[:date] =  Date.parse(truck.at_css("[class='event-meta-heading eventlist-meta-date']").content).to_s
  truck_info[:start_time], truck_info[:end_time] = truck.at_css("[class='event-time-12hr']").content.strip.split(" –  ")
  trucks << truck_info
end

output = File.open(__dir__ + "/public/foodtrucks.json", "w")
output.puts trucks.to_json
output.close