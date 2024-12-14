# Netrunner System Gateway - extract cards and add bleed to the images

The tool to read the [System Gateway PDF from Null Signal Games](https://access.nullsignal.games/Gateway/English/English/SystemGatewayEnglish-A4%20Printable%20Sheets%203x.pdf) to cut the card images into separate PNGs (`/imgs` folder). Then adds the bleed to the card (repeats the outer pixels) and save the images into `/bleed` folder.

The script is scruffy, contributions welcome.

## Setup

Install dependencies:

```
poetry install
```

Create `imgs` and `bleed` directories:

```
mkdir imgs
mkdir bleed
```

## Run

```
poetry run python3 extract.py 
```

The cut images will be in `imgs` and the images with bleed in `bleed`. The images are quite big.
