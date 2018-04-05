require 'RMagick'
require 'json'
require 'csv'


input = '/Users/johnlee/Desktop/ruby-scripts/data/f1252067.csv'
# output = '/Users/johnlee/Desktop/ruby-scripts/'

CSV.foreach(input, :headers => true) do |row|
  p "** running **"

  image = Magick::Image.read(row['image_url']).first
  ## Draw bounding box
  bb = Magick::Draw.new
  bb.fill_opacity(0)
  bb.stroke('#00ff00')

  ## Draw text
  tt = Magick::Draw.new
  tt.text_undercolor('#D3D3D380')  # Optional text background

  if row['annotation'] != nil
    annotation = JSON.parse(row['annotation']) # Array of annotations
    anno = annotation['shapes']
    p anno
    p "********"

    if anno.count > 0
      anno.each do |a|
        bb.rectangle(a['x'], a['y'], (a['x']+a['width']), (a['y']+a['height']))
        ## To display the labels
        if a['tag'] != nil
          tt.text(a['x'], a['y'], a['tag'])
        end
      end
    end

    image_file = row['_unit_id'].to_s + '.jpg'
    bb.draw(image)
    tt.draw(image)
    image.write(image_file)
  end
end
