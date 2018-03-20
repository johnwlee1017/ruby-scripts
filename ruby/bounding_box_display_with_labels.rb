require 'RMagick'
require 'json'

file = File.read('some.json')
json = JSON.parse(file)

json.each do |json|
  image = Magick::Image.read(json['url']).first
  dt = Magick::Draw.new
  dt.fill_opacity(0)
  dt.stroke('#00ff00')

  if json['annotation'] != ''
    annotation = JSON.parse(json['annotation']) # Array of annotations
    anno = annotation['shapes']
    p anno
    p "********"

    if anno.count > 0
      anno.each do |a|
        p a['x']
        p a['y']
        p a['tag']
        p "*********************"
        dt.rectangle(a['x'], a['y'], (a['x']+a['width']), (a['y']+a['height']))
        if a['tag'] != nil
          dt.text(a['x'], a['y'], a['tag'])
        end
      end
    end

    image_file = json['_unit_id'].to_s + '.jpg'
    dt.draw(image)
    image.write(image_file)
  end
end
