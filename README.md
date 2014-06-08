# Photostreamer for the Raspberry Pi

Photostreamer can attach to a camera (any camera that supports tethering over [PTP](http://en.wikipedia.org/wiki/Picture_Transfer_Protocol) with [gphoto2](http://www.gphoto.org/)) and push thumbnails of photos, as they're shot, to an Amazon S3 server. It's created to work with [photostreamer-server](https://github.com/achavez/photostreamer-server), a Node.js app that can run in Heroku's free tier and allows an editor to view the photos and request the full-resolution versions from the Raspberry Pi.

This repository contains a script that acts as a hook script for gphoto2: creating the thumbnails, sending them to Amazon S3 and notifying photostreamer-server. Another script runs as a cron job, pinging the photostreamer-server and sending full-resolution photos as they're requested.

There's also a shell script that can be run on startup, bind to [buttons on the Pi](http://www.adafruit.com/products/1489) and launch the whole process with the click of a button. That means the Pi can be run headless with a battery pack and [attached screen](http://www.adafruit.com/products/1601).

## Setup

#### Configuring the Pi

First things first, you'll need to install gphoto2. It's availabile using Apt, but that version is outdated and doesn't support many of the newer cameras. Fortunately, [gonzalo](https://github.com/gonzalo) has put together a great install script for gphoto2 and the Pi at [github.com/gonzalo/gphoto2-updater](https://github.com/gonzalo/gphoto2-updater), which you'll probably want to use unless you're going to compile it yourself.

After gphoto2 is installed, run `sudo apt-get install pip-python` to install [pip](https://pip.pypa.io/en/latest/index.html).

Next, clone this repository into your home directory. `cd` into the repository and run `sudo pip install -r requirements.txt` to install the required Python packages.

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

#### Configuring the script(s)

...

#### Setting up the buttons

*Optional:* There's a bash script in the repository that can be used to listen to buttons on the Pi and execute photostreaming functions when they're pushed. The script is built to work with the buttons on Adafruit's [PiTFT](http://www.adafruit.com/products/1601), but you should be able to modify it to work with any of the GPIO pins.

To use the script, make sure it's executable by running `sudo chmod 755 buttons.sh` from inside the repository. Then either run the script manually (`sudo bash buttons.sh`).

Even better, add the script to your [rc.local](http://www.raspberrypi.org/documentation/linux/usage/rc-local.md) so it starts every time the Pi boots. To do that, add something like `sudo /home/pi/photostreamer-server/buttons.sh &` to the file somewhere before the `exit 0` line.

## Development

This is a work in progress and pull requests/suggestions/issues are definitely welcome.

**On a Mac:** It's possible to install gphoto2 on a Mac and play and use any of the code's functionality. However, you'll need to run `killall PTPCamera` after you connect the camera to prevent OSX from taking over the connection with the camera.