require 'RMagick'
require 'json'

file = File.read('40_IoU_results(2nd run).json')
json = JSON.parse(file)

json.each do |json|
  image = Magick::Image.read(json['image_url']).first
  dt = Magick::Draw.new
  dt.fill_opacity(0)
  dt.stroke('#00ff00')

  annotation = JSON.parse(json['annotation']) # Array of annotations

  if annotation.count > 0
    annotation.each do |a|
      dt.rectangle(a['x'], a['y'], (a['x']+a['width']), (a['y']+a['height']))
    end
  end

  image_file = json['_unit_id'].to_s + '.jpg'
  dt.draw(image)
  image.write(image_file)
end
