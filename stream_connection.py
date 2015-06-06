import httplib
import tweepy
import MySQLdb
import time
import json
import urlnorm
import urlparse
import hashlib

#Bounding box for geo restriction
BOUNDING_BOX_SF =  [-123.0137,37.6040,-122.3549,37.8324]
BOUNDING_BOX_USA = [-122.75,36.8,-121.75,37.8]

URL_SHORTENERS = ["bit.do","t.co","lnkd.in","db.tt","qr.ae","adf.ly","goo.gl","bitly.com","cur.lv","tinyurl.com",
                  "ow.ly","bit.ly","adcrun.ch","ity.im","q.gs","viralurl.com","is.gd","vur.me","bc.vc",
                  "twitthis.com","u.to","j.mp","buzurl.com","cutt.us","u.bb","yourls.org","crisco.com","x.co",
                  "prettylinkpro.com","viralurl.biz","adcraft.co","virl.ws","scrnch.me","filoops.info","vurl.bz",
                  "vzturl.com","lemde.fr","qr.net","1url.com","tweez.me","7vd.cn","v.gd","dft.ba","aka.gr","tr.im",
                  "fb.me"]

#DB Connection
conn = MySQLdb.connect("localhost","twitstream","tw1tstream!","twitstream",charset="utf8mb4")
c = conn.cursor()


#consumer key, consumer secret, access token, access secret.
CKEY="Jl9zov3MhbAvPilqyGiHMg9Do"
CSECRET="okXvu9KCmplvIfASj45iS2288J2F3WiWT5D2UpNVmLfhLm3CbQ"
ATOKEN="14811291-lbVlEAtLMYwLmGl2mPqcrmehblbus9wEtBLcCzKu5"
ASECRET="tmT0viQTSUjffdET0rAQPOPQXe9vk7nOdI5DTnyokNB3u"

class listener(tweepy.StreamListener):

    tweet_count = 0

    def on_data(self, data):
        tweet_data = json.loads(data)
        if 'limit' in tweet_data:
            print("Limit:" + str(tweet_data["limit"]))
        else:
            #insert into tweet db
            tweet = tweet_data["text"]
            username = tweet_data["user"]["screen_name"]
            #lat = tweet_data[]
            #long = tweet_data[]

            c.execute("INSERT INTO tweet (time, username, tweet) VALUES (%s,%s,%s)",
                (time.time(), username, tweet))
            tweet_id = c.lastrowid

            # insert full urls into DB
            for url in tweet_data["entities"]["urls"]:

                # process URL
                norm_url = urlnorm.norm(url["expanded_url"])
                norm_url_tuple = urlparse.urlparse(norm_url)

                # unshorten URLs for common URL minimizer services
                if norm_url_tuple[1] in URL_SHORTENERS:
                    norm_url = unshorten_url(norm_url)
                    norm_url_tuple = urlparse.urlparse(norm_url)

                md5_url = hashlib.md5()
                md5_url.update(norm_url.encode("utf-8"))

                c.execute("INSERT INTO url (url, domain, url_hash) VALUES (%s,%s,%s)",
                          (norm_url, norm_url_tuple[1], md5_url.hexdigest()))
                url_id = c.lastrowid
                c.execute("INSERT INTO tweet_urls (tweet_id, url_id) VALUES (%s,%s)",
                          (tweet_id, url_id))



            conn.commit()
            self.tweet_count += 1
            if self.tweet_count % 1000 == 0:
                print self.tweet_count

        return True

    def on_error(self, status):
        print status

def unshorten_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url

def main():
    auth = tweepy.OAuthHandler(CKEY, CSECRET)
    auth.set_access_token(ATOKEN, ASECRET)

    twitstream = tweepy.Stream(auth, listener())
    twitstream.filter(locations=BOUNDING_BOX_SF,languages=["en"])

if __name__=='__main__':
	main()

