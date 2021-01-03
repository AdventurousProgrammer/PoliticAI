from newspaper import Article
#cnn_paper = newspaper.build('https://www.cnn.com/')
cnn_url = 'https://www.cnn.com/2021/01/02/politics/senate-republicans-electoral-college/index.html'
dw_url = 'https://www.dailywire.com/news/ted-cruz-other-gop-senators-sign-letter-announcing-intent-to-vote-against-electors-from-disputed-states-until-election-audit-is-conducted'
#fields = dir(article)
#print(article.meta_description)
'''
for field in fields:
    if 'summary' in field:
        print(field)
'''
cnn_links = [
            'https://www.cnn.com/2021/01/02/politics/senate-republicans-electoral-college/index.html',
             'https://www.cnn.com/2021/01/03/politics/trump-republicans-electoral-college-new-congress-democracy/index.html',
             'https://www.cnn.com/2021/01/01/politics/biden-history-analysis/index.html',
             'https://www.cnn.com/2020/12/19/politics/student-loan-relief-devos-trump-biden/index.html',
             'https://www.cnn.com/2020/12/22/politics/biden-trump-refugee-cap/index.html'
]

dw_links = [
    'https://www.dailywire.com/news/ted-cruz-other-gop-senators-sign-letter-announcing-intent-to-vote-against-electors-from-disputed-states-until-election-audit-is-conducted',
            'https://www.dailywire.com/news/warren-schumer-invoke-econ-101-in-push-to-cancel-50k-in-fed-student-loan-debt-per-borrower',
            'https://www.dailywire.com/news/biden-will-raise-number-of-refugees-admitted-to-u-s-from-15k-to-125k',
            'https://www.dailywire.com/news/the-powerful-consequences-of-2020-election-how-it-could-shape-federal-agencies',
            'https://www.dailywire.com/news/mcconnells-home-vandalized-after-vote-to-enhance-stimulus-checks-blocked'
            ]

for link in cnn_links:
    article = Article(link)
    article.download()
    article.parse()
    article.nlp()
    print(f"Title: {article.title}")
    print()
    print()
    for keyword in article.keywords:
        print(f"Keyword: {keyword}")
    print()
    print()
    print(f"Description: {article.meta_description}")
    print(f"Summary: {article.summary}")
    print()
    print()
#file = open('cnn_links.txt','r')
#lines = file.readlines()
#print(type(lines))
#print(article.summary)

'''
for field in fields:
    if 'description' in field or 'desc' in field:
        print(field)
'''
#print(dir(article))
'''
print("Title: ", article.title)
print("Authors: ", article.authors)
print("Date: ", article.publish_date)
'''
'''
for article in cnn_paper.articles:
    print(article.url)
'''