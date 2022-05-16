# Image Upload API
Allows uploading and storage images in JPG and PNG format.

Every user is assigned to certain Tier, which allows storing images in certain sizes. Beside that Premium Tier provide additional functionality.

Basic Tier:
- store 200px high thumbnail

Premium Tier:
- store 200px high thumbnail
- store 400px high thumbnail
- store image in original size
 
Premium Tier:
- store 200px high thumbnail
- store 400px high thumbnail
- store image in original size
- allows generating temporary links to image for unregistered users

All endpoints reached through web browser require user to log in first.

**DISCLAIMER:**

Users, Tiers and Thumbnails are currently created by Admin via Django Admin Panel

## API Endpoints

### Get single image from database
Image name can be checked through "Get all the images from database" endpoint. They are changed relative to originally uploaded image to fit application requirements.
#### HTTP request
```
GET http://example.com/<image_name>
```
#### cURL
```
curl -X GET -u username:password http://example.com/<image_name>
```

### Get all the images from database
#### HTTP request
```
GET http://example.com/images/
```
#### cURL
```
curl -X GET -u username:password http://example.com/images/
```

### Add image to database 
#### HTTP request
```
POST http://example.com/add/
```
#### cURL
```
curl -X POST -u username:password -F "image_name=@<path_to_image>" http://example.com/add/
```

### Generate temporary link to image
#### HTTP request
Image name can be checked through "Get all the images from database" endpoint. They are changed relative to originally uploaded image to fit application requirements.

API allows generating links for unregistered users, that expire in 30 to 30 000 seconds. 
```
GET http://example.com/tmp-gen/<image_name>/<time_in_seconds>
```
#### cURL
```
curl -X GET -u username:password http://example.com/tmp-gen/<image_name>/<time_in_seconds>
```