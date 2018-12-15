#!/bin/sh
rm -rf ~/.clocky/*
mkdir -p ~/.clocky/
cp -v ./* ~/.clocky/
mkdir -p ~/.fonts/
cp -v ./*.ttf ~/.fonts/
