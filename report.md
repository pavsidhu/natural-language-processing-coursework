# Natural Language Processing Report

## Overview

Throughout this report, I test my program on the `test_untagged` dataset released on week 8 of the assignment. To run the program, there are instructions in the `README.md`.

### Part One: Email Tagging

#### Paragraph Tagging

To tag paragraphs, I looked through the dataset to find patterns in to construct a Regex pattern to identify them. I noticed that most paragraphs start with a line break \n and either a capital letter, number or a group of symbols. All paragraphs end with a period too.

I tested my solution and noticed it was also tagging the header as a paragraph. I made a utility function to split the header and abstract,  so that I could tag the abstract. In the end, I achieved an F1 score of 0.58.

My paragraph tagger is still less than perfect, due to inconsistencies in email formatting, it was difficult to achieve a higher score.

#### Sentence Tagging

I tagged sentences using `sent_tokenize()` in NLTK. This was very good at splitting text into sentences. It accounted for periods in names such as `Prof.`. While the function worked well, it would overtag. This lead to a lower F1 score.

To fix this issue, I decided to only tag sentences within paragraphs. Though it ignores sentences outside of paragraphs, it was very accurate at tagging sentences inside paragraphs. This increased my F1 score enough to keep this approach in my final solution.

The training data tagged sentences with a period outside of the sentence. This caused issues with `sent_tokenize()` since it would include a period in the sentences. To fix this, I removed the last character from tokenised sentences if they denoted the end of a sentence i.e. a period or question mark.

My sentence tagger achieved a score of 0.73. To improve sentence tagging, I would look further into tagging sentences outside of paragraphs using regex.

####Time Tagging

The majority of emails contained a `Time` header. This proved very useful in tagging the times of seminars. I used regex to find start times and optional end times (if a hyphen was present) in the `Time` header.

Using this data, I generate a list of regex that could match any potential formats of the time. This includes variations in the time suffix (AM or PM), whether it included minutes, differences in spacing and also word variations such as noon for 12 pm. Additionally, I handled edge cases like 12-1pm too.

Using the generated regex patterns, I look for occurrences of the times in the text and tag them. I achieved an F1 score of 0.96 for the start time and 0.90 for the end time.

While I achieved a high score, there were cases of emails that did not have all the information in the `Time` header. I would handle cases where the start or end time are not mentioned in the header if I were to improve the tagger.

####Speaker Tagging

Speakers were more difficult to identify and tag. I used a three tier approach, using regex, tagged data from the training set and named-entity recognition to tag the speaker.

My first method using regex searched for occurrences of `Speaker:` or `Who:` in the email. This was very efficient at finding names.

If the regex was unsuccessful, I used the tagged data from the original training set to find speakers. This was very accurate at tagging speakers since they were already speakers in other emails.

My last resort if all else failed was to use the Stanford NER tagger to find names in the email. I tried tagging the emails one by one though this was very slow. As the tagger was a .jar file, the Java Virtual Machine starts and stops each time, slowing down the process. To combat this, I tried running a local Stanford NER tagger server; this quickly grew complicated. I instead I tagged all the emails beforehand which significantly improved tagging time.

After the Stanford tagger finds names, I chunk them together and remove duplicates of the same name. I now have a list of names that could be potential speakers. To lower the list of names, I removed the name in the PostedBy header from the name list which made things easier.

I then check if the name appears in the `Topic` header or is part of a sentence such as `{{ name }} will be speaking about` or `presenting {{ name }}`. If these both fail then I assume there is no speaker in the email.

In the end, I achieved an F1 score of 0.40. To develop upon this tagger, I would use smarter ways of identifying names using Wikification, since the Stanford tagger can miss names.

####Location Tagging

My location tagger uses four methods to find the location on the seminar.

The first step uses regex to find locations listed as `Place:` or `Where:`. This picks up locations very well yet most of the locations are hidden within sentences so I needed a better approach.

Next, I use the previously tagged data from the training set and search for the locations in the text. This works very well as locations are repeated often.

My third step searches for patterns in location names. There were cases where locations were locations in the form `building room-number` such as `WeH 5409`. This worked well for specific cases.

My last step involved using the Stanford NER tagger to find locations. Locations are chunked with a grammar using NLTK. I then extract the locations and use the Bing Search API to search for the locations. I check the search results and check if the top three results are from Carnegie Mellon University. The first location that is successful is tagged. This worked in a sizable number of cases.

I achieved an F1 score of 0.54. I missed out on opportunities to identify locations using a POS tagger and sentence patterns since several locations were followed after `in`. I would add this to improve my tagger in the future.

### Part Two: Ontology Classification

Before beginning the ontology I looked through the emails in the test set and looked for ways to segregate the emails into topics.

I created a function to fetch all the topic headers and output the word frequencies found. While I found this to be good to generate ontology ideas, I did not find it useful for the classification algorithm.

My first attempt was to use fastText to find similarities between words. Though its command line utility was fast, it's Python library was not mature enough to use and missed methods to find nearest neighbours for words. Unofficial libraries and wrappers for fastText were available, including a wrapper in Gensim, however in practice they were too slow to use.

I ended up using Word2vec to represent words as vectors and compared the similarities between them using Gensim. This was much faster to use than fastText.

I started using the topic headers to classify the emails. I removed common words using the stop words corpus in NLTK and compared the rest of the words with each node in the tree. The node with the highest average similarity is chosen as the ontology. I realised that the topic header did not provide enough information the classify emails, so I used the abstract instead. This worked a bit better.

I noticed that some emails have a `Type` header such as `cmu.cs.robotics`. I used this to classify emails too. Problems arise once a valid type header is found as it automatically returns the topic rather than trying to find a more specific ontology in the tree. To improve this I would use the `Type` header to restrict the search in the tree rather than returning the node.

My tree was very small and I wanted to expand it to have more specific ontologies. I decided to use WordNet to generate branches in the tree. While this increased the depth of the tree, it did not add very useful information to the tree. If I were to rebuild the tree, I would make use of WordNet to find lemmas of more specific words in the text that may link back to a topic such as Computer Science.

The results I got from this solution were satisfactory, though there is much room for improvement. Emails are classified, though general topics such as computing or art are chosen over more precise ontologies in the WordNet generated branches. This was due to my tree generation algorithm choosing less than ideal nodes and Word2vec not prioritising certain words over more general words.

## Conclusion

My overall F1 score was 0.69. This is a satisfactory score. My ontology tagger worked for general topics such as computing, art or science, however, more specific classifications are not often used.