Setting up the Pi
-----
First things first, you'll need to install gphoto2. It's availabile using `apt-get`, but that version is outdated and doesn't support many of the newer cameras. Fortunately, @gonzalo has put together a great install script for gphoto2 and Pi at [github.com/gonzalo/gphoto2-updater](https://github.com/gonzalo/gphoto2-updater)

After gphoto2 is installed, run `sudo apt-get install graphicsmagick pip-python` to install the remaining dependencies.

Setting up S3
-----
```
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

Testing on a Mac
-----
It's possible to install gphoto2 on a Mac and play with the code locally. However, you'll need to run `killall PTPCamera` after you connect the camera to prevent OSX from taking over the connection with the camera.