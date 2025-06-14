
#!/bin/bash
# Dependancies
# - img-optimize - https://virtubox.github.io/img-optimize/
# - imagemagick
# - jpegoptim
# - optipng

FOLDER="/Users/ismailefetop/projects/org-blog/ismailefe_org/photography/analog_photos/pics"

# max width
WIDTH=1600

# max height
HEIGHT=1200

#resize png or jpg to either height or width, keeps proportions using imagemagick
find ${FOLDER} -iname '*.jpg' -o -iname '*.png' -exec convert \{} -verbose -resize $WIDTHx$HEIGHT\> \{} \;
img-optimize --std --path ${FOLDER}
