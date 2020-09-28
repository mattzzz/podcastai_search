# podcastai_search

### a quick POC to search podcast text for keyword topics using NLP.


* use speech to text model to transcribe podcast (optional)
* download and parse podcast transcript (optional)
* use huggingface transformer for NLP sentiment analysis of search terms
* uses a very hacky Dash app 


To run:

0. install dependancies in a conda py3 env, pip install -r requirements.txt
1. run podcastai.py, change the code for required search terms. Results are output to csv files.
2. run webapp.py, open in browser and csv output files are plotted.

Please not that the podcast transcript source has 6mins of adverts at the start. This will skew the times compared to youtube version.

To run the speech to text conversion, various methods can be tried. Usually all conversions need audio to be in wav format firstly.
If conversion is needed them ffmpeg can be used for this.

If I get time, I might do the following:
* link the search boxes with the huggingface model
* improve the webapp 

