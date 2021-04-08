#!/bin/bash

# Break on error
set -e

ASSETS="src/assets"
ROBOTS="src/robots"
NODE_MODULES="node_modules"
PUBLIC="public/"
PUBLIC_ROBOTS="robots/"
FONT_AWESOME=$NODE_MODULES/font-awesome

# Install packages
npm ci

# Clean
echo [INFO] Cleaning
rm -rf $PUBLIC
mkdir $PUBLIC
rm -rf $PUBLIC_ROBOTS
mkdir $PUBLIC_ROBOTS

# Copy font awesome to public
echo [INFO] Copying font awesome
cp -r $FONT_AWESOME/fonts $PUBLIC
mkdir -p $PUBLIC/stylesheets && cp $FONT_AWESOME/css/font-awesome.min.css $PUBLIC/stylesheets

# Copy robots.txt and sitemap.xml
echo [INFO] Copying robots.txt and sitemap.xml
cp $ROBOTS/* $PUBLIC_ROBOTS

# Copy images
echo [INFO] Copying images
cp -r $ASSETS/images $PUBLIC

# Copy javascript
echo [INFO] Copying javascript
cp -r $ASSETS/javascript $PUBLIC

# Copy stylesheets
echo [INFO] Copying stylesheets
cp -r $ASSETS/stylesheets $PUBLIC