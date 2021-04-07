ng build
aws s3 rm s3://farmfresh.com --recursive
aws s3 sync ./dist/EggRoute/ s3://farmfresh.com --acl public-read
#aws cloudfront create-invalidation --distribution-id EO37R0PS8J6V4 --paths "/*"

