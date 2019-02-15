# Tweet dataset adapter

Generate cleared and adopted tweeter dataset for sentimental analysis
from [twitter dataset](https://www.clarin.si/repository/xmlui/handle/11356/1054)
That dataset contains 15 languages but that adapter works only with Russian tweets
You can find that dataset zipped in data.zip


#### Receiving data
```
$ cd data
$ unzip data.zip
```

#### Generated prepared dataset
```
$ python generate.py
```
