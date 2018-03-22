require 'RMagick'
require 'json'
require 'csv'


input = '/Users/johnlee/Desktop/ruby-scripts/data/test.csv'
# output = '/Users/johnlee/Desktop/ruby-scripts/'

CSV.foreach(input, :headers => true) do |row|

  img = row['url']
  img_file = row['_unit_id'] + '.jpg'

  image = Magick::Image.read(img).first
  dt = Magick::Draw.new
  dt.fill_opacity(0)
  dt.stroke('#00ff00')

  if row['annotation'] != nil
    annotation = JSON.parse(row['annotation']) # Array of annotations
    anno = annotation['shapes']

    if anno.count > 0
      anno.each do |a|
        dt.rectangle(a['x'], a['y'], (a['x']+a['width']), (a['y']+a['height']))
      end
    end

    image_file = row['_unit_id'].to_s + '.jpg'
    dt.draw(image)
    image.write(image_file)
  end
end
