# Audax Labeller

## Introduction

This is a very basic label-producer for Audax brevet cards. It currently has various elements hard-coded that mean that it would require modifying to use anything other than Avery J8161.

## Installation

This is built and tested on Python 3.11. With that installed, run `pip3 install -f requirements.txt`.

## Usage

Download your start sheet from the Organisers area, or format a spreadsheet the same way. Place it in the same folder as the code and modify the 'EVENTS' variable in the code to contain the event number(s) you want to produce labels for.

Run the tool, eg. `python3 labels.py`

## Customising

You can edit the fields that are used in various places. This is primarily in the template, `label_base.html`. Formatting can be changed in `labels.css`.
