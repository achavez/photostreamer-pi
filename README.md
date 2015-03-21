# Photostreamer for the Raspberry Pi

Photostreamer can attach to a camera (any camera that supports tethering over [PTP](http://en.wikipedia.org/wiki/Picture_Transfer_Protocol) with [gphoto2](http://www.gphoto.org/)) and push thumbnails of photos, as they're shot, to an Amazon S3 server. It's created to work with [photostreamer-server](https://github.com/achavez/photostreamer-server), a Node.js app that can run in Heroku's free tier and allows an editor to view the photos and request the full-resolution versions from the Raspberry Pi.

This repository contains a script that acts as a hook script for gphoto2: creating the thumbnails, sending them to Amazon S3 and notifying photostreamer-server. Another script runs as a cron job, pinging the photostreamer-server and sending full-resolution photos as they're requested.

## Setup

#### Configuring the Pi

The easiest way to setup your Pi to use Photostreamer is using the install script. To use the script:

1. Setup your Pi using NOOBS using the instructions on this page: http://www.raspberrypi.org/help/noobs-setup/
2. Configure your Pi's wifi settings using any of the methods on this page: http://www.raspberrypi.org/documentation/configuration/wireless/
3. Download the installer to the home directory:

  ```
  $ cd ~
  $ wget https://raw.githubusercontent.com/achavez/photostreamer-pi/master/installer.sh
  ```
4. Make the installer executable and run it.

  ```
  $ chmod +x installer.sh
  $ sudo ./installer.sh
  ```
5. Fill out the config file on your Pi at `/home/pi/photostreamer-pi/config.cfg`. For *bucket* you only need to provide the bucket name, not the fully formed bucket URL. Also, feel free to tweak the thumbnail settings if you'd like to reduce the file size that's being sent for each photo.
6. Restart the Pi.

#### Setting up S3

You'll also need to setup a bucket on Amazon S3. Ideally, this is an empty bucket that is used solely for you to push photos to. You can setup the bucket in the [AWS Management Console](http://aws.amazon.com/console/). Once your bucket is setup, you'll want to [add a bucket policy](http://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html) like the one below so the thumbnails you upload are visible on the Web, allowing them to be seen in the viewer app.

```javascript
{
	"Version": "2008-10-17",
	"Statement": [
		{
			"Sid": "AllowPublicRead",
			"Effect": "Allow",
			"Principal": {
				"AWS": "*"
			},
			"Action": "s3:GetObject",
			"Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
		}
	]
}
```

Once the bucket is setup, you'll want to generate credentials so the Pi can access your bucket. The best way to do that is by [creating an IAM user](http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_SettingUpUser.html). You'll need the IAM user's *access key ID* and a *secret access key*. Make sure to give the user write permission on your bucket.

## Usage

Assuming you're connected to wifi, using the Pi to stream photos should be as simple as hooking up a camera and pressing the trigger. The Pi will automatically try to connect to your camera in the background every 10 seconds. And a cron job will run in the background to handle communication with the server and sending the high-resolution versions of your photos when they're requested.

## Troubleshooting

If the photos you're shooting aren't showing up online there are a few things to check:
- Make sure you're connection to the Internet is working. For example, try using the `ping` command, which will yield an error if you're Internet connection isn't working:

  ```
  $ ping -c 5 google.com
  ```
- Check the Photostreamer logs, which are at `/home/pi/photostreamer/logs/photostreamer.log`. You can use the `tail` command to follow them and watch for updates, which may be helpful for debugging in realtime:

  ```
  $ tail -f /home/pi/photostreamer/logs/photostreamer.log
  ```
- Ensure that gphoto2 is able to connect to your camera:

  ```
  $ gphoto2 --auto-detect
  ```
- Also, keep in mind that this project is a work in progress and it's definitely possible that there's an undiscovered bug. If you think you've found one, please [file a bug report](https://github.com/achavez/photostreamer-pi/issues/new) and let us know.

## Development

This is a work in progress and pull requests/suggestions/issues are definitely welcome.

**On a Mac:** It's possible to install gphoto2 on a Mac and play and use any of the code's functionality. However, you'll need to run `killall PTPCamera` after you connect the camera to prevent OSX from taking over the connection with the camera.

## License

The MIT License (MIT)

Copyright (c) 2014 Andrew Chavez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
