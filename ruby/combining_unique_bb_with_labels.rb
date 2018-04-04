require 'RMagick'
require 'json'
require 'csv'


input = '/Users/johnlee/Desktop/ruby-scripts/data/a1253255.csv'

images_url_hash = {}

CSV.foreach(input, :headers => true) do |row|
  p "** running **"

  img = row['image_url']
  img_file = row['_unit_id'] + '.jpg'

  if !images_url_hash.has_key?(img)
    images_url_hash[img] = img_file

    image = Magick::Image.read(img).first
    dt = Magick::Draw.new
    dt.fill_opacity(0)
    dt.stroke('#00ff00')

    if row['annotation'] != nil
      annotation = JSON.parse(row['annotation']) # Array of annotations
      anno = annotation['shapes']
      p anno
      p "********"

      if anno.count > 0
        anno.each do |a|
          # p a['x']
          # p a['y']
          # p a['tag']
          # p "*********************"
          dt.rectangle(a['x'], a['y'], (a['x']+a['width']), (a['y']+a['height']))
          ## To display the labels
          if row['box_item'] != nil
            dt.text(a['x'], a['y'], row['box_item'])
          end
        end
      end

      image_file = row['_unit_id'].to_s + '.jpg'
      dt.draw(image)
      image.write(image_file)
    end
  elsif images_url_hash.has_key?(img)
    current_img_file = images_url_hash[img]
    current_img = Magick::Image.read(current_img_file).first

    dt = Magick::Draw.new
    dt.fill_opacity(0)
    dt.stroke('#00ff00')

    if row['annotation'] != nil
      annotation = JSON.parse(row['annotation']) # Array of annotations
      anno = annotation['shapes']
      p anno
      p "********"

      if anno.count > 0
        anno.each do |a|
          # p a['x']
          # p a['y']
          # p a['tag']
          # p "*********************"
          dt.rectangle(a['x'], a['y'], (a['x']+a['width']), (a['y']+a['height']))
          ## To display the labels
          if row['box_item'] != nil
            dt.text(a['x'], a['y'], row['box_item'])
          end
        end
      end

      dt.draw(current_img)
      current_img.write(current_img_file)
    end
  end
end
