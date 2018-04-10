require 'csv'
require 'json'


input = '/Users/johnlee/Desktop/ruby-scripts/data/entity_test.csv'

CSV.open("test.csv", "wb") do |csv|
  csv << ["_unit_id", "entity_type", "start_char", "end_char", "selected_text", "sentence"]
end

CSV.foreach(input, :headers=>true) do |row|

  unit_id = row['_unit_id']
  sentence = row['sentence']
  labels = row['locations']

  entity_type = ""
  start_char = 0
  end_char = 0
  selected_text = ""

  if labels != nil
    p labels_array = labels.split("\n")
    p "*********"

    labels_array.each do |item|
      items_array = item.split(":")
      entity_type = items_array[2]
      start_char = items_array[1]
      # end_char = items_array[2]
      selected_text = items_array[0]

      CSV.open("test.csv", "a+") do |csv|
        csv << [unit_id, entity_type, start_char, end_char, selected_text, sentence]
      end
    end
  else
    CSV.open("test.csv", "a+") do |csv|
      csv << [unit_id, entity_type, start_char, end_char, selected_text, sentence]
    end
  end
end
