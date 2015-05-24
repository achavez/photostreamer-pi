# Photostreamer for the Raspberry Pi

[![CircleCI branch](https://img.shields.io/circleci/project/achavez/photostreamer-pi/rewrite.svg)](https://circleci.com/gh/achavez/photostreamer-pi)

[![Requires.io](https://img.shields.io/requires/github/achavez/photostreamer-pi/rewrite.svg)]()

This branch is a top-to-bottom rewrite of the original photostreamer-pi application, using Django and a proper job queue to handle uploads instead of the previous patchwork of custom code. It will also include an admin that can be used to update settings and allow photographers additional control over what is sent back to photostreamer-server.

Unlike the original version, this version will also have complete test coverage and use Python 3.