require 'open-uri'
require 'nokogiri'
require 'json'
require 'date'

doc = Nokogiri::HTML(open("https://wheresthefoodtruck.com/locations/196/"))

trucks = []

doc.css("[class='card rounded-2 overflow-hidden mb-3 shadow-sm']").each do |truck|
  truck_info = {}
  truck_info[:date] =  Date.parse(truck.at_css("[class='text-primary mb-0 px-3 text-center d-flex justify-content-center align-items-center h-100']").content).to_s
  truck_info[:name] = truck.at_css("a").content
  truck_info[:start_time], truck_info[:end_time] = truck.at_css("[class='col-md-3 mb-2 mb-lg-0']").content.split(' - ').map(&:strip)
  trucks << truck_info
end

output = File.open(__dir__ + "/public/foodtrucks.json", "w")
output.puts trucks.to_json
output.close
