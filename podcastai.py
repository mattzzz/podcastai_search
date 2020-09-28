
from transformers import pipeline
import bs4
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import math
import speech_recognition as sr



class PodcastAISearch:

    def __init__(self):
        self.script = None

    def transcribe_audio(self, filename):
        """ generates script from podcast in wav format """
        r = sr.Recognizer()

        wav_file = sr.AudioFile(filename)
        with wav_file as source:
            audio = r.record(source)

            # text = r.recognize_google(audio)
            text = r.recognize_sphinx(audio)
            # text = r.recognize_google_cloud(audio)
            # text = r.recognize_bing(audio)
            # text = r.recognize_houndify(audio)
            # text = r.recognize_ibm(audio)
            # text = r.recognize_wit(audio)

        # print(text)
        self.script = text
        return text

    def get_transcript_from_URL(self, URL):
        """ loads a script from https://podscribe.app/ 
            return a list of (time, text) tuples
        """
        if 'podscribe.app' not in URL:
            raise Exception("unsupported podcast transcript URL: " + URL)
        request = urlopen(URL)
        html = request.read()
        soup = BeautifulSoup(html)#, 'lxml')
        div = soup.find_all('a', {'class':'timemark'})

        script = []
        for line in div:
            # print(type(line), dir(line), line)
            # print(line.get('name'))
            ts = line.get('name')
            # print(line.contents)
            # print(line.text)
            for l in line.children:
                # print(line)
                # print(l.text[2:])
                # print(l.next.text)
                dialog = l.next.text
                script.append((ts, dialog))

        self.script = script
        return script

    def get_scores(self, labels):
        """ use NLP sentiment analysis on the podcast text
            returns scores for each time entry
        """
        classifier = pipeline("zero-shot-classification", device=0)

        scores = []
        for s in self.script:
            res = classifier(s[1], labels)
            # print(res)
            scores.append((s[0], res))

        return scores

    def write_results_multi(self, filename, scores):
        with open("results.csv", "wt") as f:
            f.write("time")
            num_classes = len(scores[0][1]['scores'])
            for i in range(num_classes):
                f.write(",prob{}".format(i))
            f.write("\n")
            for s in scores:
                ts = s[0]
                score = s[1]['scores']
                # print(ts, score, end='')
                # print(',')
                f.write('{}'.format(ts))
                
                for i in range(num_classes):
                    f.write(',{}'.format(score[i]))
                f.write('\n')

    def write_results(self, filename, scores):
        with open(filename, "wt") as f:
            f.write("time,prob\n")
            for s in scores:
                f.write('{},{}\n'.format(s[0], s[1]['scores'][0]))



if __name__ == '__main__':

    pcai = PodcastAISearch()

    # pcai.transcribe_audio('elon.wav')

    print("Loading transcript of podcast...")
    URL = 'https://podscribe.app/feeds/http-joeroganexpjoeroganlibsynprocom-rss/episodes/964caf3227b64117b20a82a574742edf#02:25:59'
    pcai.get_transcript_from_URL(URL)

    print("Scoring search terms in transcript of podcast...")
    # scores = pcai.get_scores(script, ["cars", "smoking weed"])
    scores = pcai.get_scores(["cars"])
    pcai.write_results('first.csv', scores)
    scores = pcai.get_scores(["smoking weed"])
    pcai.write_results('second.csv', scores)
    # scores = pcai.get_scores(["space"])
    # write_results('third.csv', scores)

