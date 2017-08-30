import re
import codecs
import argparse

siteVisionContent = list()
siteVisionPages = dict()
# siteVisionPagesFullPath=dict[]
rowsSV = []

linesLoadedSV = 0
linesLoadedGA = 0
totalHTMLPagesSV = 0
linesParsedGA = 0
totalHTMLPagesVisited = 0
totalHTMLPagesUnvisited = 0

_startup_arguments = None


def parse_startup_argument():
    global _startup_arguments
    parser = argparse.ArgumentParser(
        description='Compare a Sitevision website content index file with a Google Analytics weblog.')
    parser.add_argument('infile_sitevision')
    parser.add_argument('infile_google_analytics')
    parser.add_argument('outfile_result')
    _startup_arguments = parser.parse_args()


def loadSiteVisionPageList():
    global linesLoadedSV
    print('Reading SiteVision log file', end=' ')

#    with open(r'C:\Users\ehis\PycharmProjects\UDemyZeroToHero\sidor magasinet 20170630.txt') as fileListSV:
    with open(_startup_arguments.infile_sitevision) as fileListSV:
        # with codecs.open('C:\Users\ehis\PycharmProjects\UDemyZeroToHero\sidor magasinet 20170630.txt', encoding='ISO-8859-1') as fileListSV:
        line_cnt = 0
        for line in fileListSV:
            #           print line
            rowsSV.append(line.split(' : '))
            line_cnt += 1
            if line_cnt % 100 == 0:
                print('.', end=''),

    fileListSV.close()
    linesLoadedSV = line_cnt
    print('\nLoaded {ll} lines\n'.format(ll=linesLoadedSV))
    return rowsSV


def parseSiteVisionPageList():
    global totalHTMLPagesSV
    print('Parsing SiteVision log file', end=' ')
    line_cnt = 0
    for row in rowsSV:
        try:
            if re.search('\.html$', row[1]):
                line_cnt += 1
                filename = (re.sub(r'http://.*\/', '', row[1])).rstrip('\n')
                siteVisionPages[filename] = [row[0], row[1].rstrip('\n')]
                # print siteVisionPages[filename]
                if line_cnt % 100 == 0:
                    print('.', end='')
        except:
            pass

    totalHTMLPagesSV = len(siteVisionPages)
    print('\nParsed {lp} lines\n'.format(lp=totalHTMLPagesSV))
    return


def parseGoogleAnalyticsLog():
    global totalHTMLPagesVisited, totalHTMLPagesUnvisited, linesParsedGA
    line_cnt = 0

    print('Reading and parsing Google Analytics file', end=' ')
    try:
#        with codecs.open(r'C:\Users\ehis\PycharmProjects\UDemyZeroToHero\GA Magasinet 1703-05.tsv',
#                         encoding='utf-16') as pageList:
        with codecs.open(_startup_arguments.infile_google_analytics, encoding='utf-16') as pageList:
            for logline in pageList:
                        line_cnt += 1
                        if logline[0] == '\'':
                            filename = re.sub(r'.*\/\w*\.', '', logline).rstrip('\n').split()[0]
                            if filename in siteVisionPages:
                                siteVisionPages.pop(filename, None)
                        if line_cnt % 100 == 0:
                            print('.', end='')
    except:
        print("Something went wrong while opening or reading the file")
        print()

    pageList.close()
    linesParsedGA = line_cnt
    totalHTMLPagesUnvisited = len(siteVisionPages)
    totalHTMLPagesVisited = totalHTMLPagesSV - totalHTMLPagesUnvisited
    print('\nParsed {lp} lines'.format(lp=linesParsedGA))
    print('Pages visited during period {lv} lines'.format(lv=totalHTMLPagesVisited))
    print('Pages unvisited during period {lu} lines\n'.format(lu=totalHTMLPagesUnvisited))


def writeResultToFile():
    print('Writing result to file', end=' ')
    line_cnt = 0
#    with open('result.txt', 'w+') as of:
    with open(_startup_arguments.outfile_result, 'w+') as of:
        # for k, v in siteVisionPages.iteritems():
        for k, v in sorted(siteVisionPages.items()):
            of.write('{:40}\t{:80}\t{}\n'.format(k, v[0], v[1]))
            line_cnt += 1
            if line_cnt % 100 == 0:
                print('.', end='')
    print('\nWrite complete')

parse_startup_argument()
print(_startup_arguments.infile_sitevision)
print(_startup_arguments.infile_google_analytics)
print(_startup_arguments.outfile_result)

loadSiteVisionPageList()
# print rowsSV
parseSiteVisionPageList()

parseGoogleAnalyticsLog()
print('Web pages on site:', totalHTMLPagesSV)
print('Pages visited:', totalHTMLPagesVisited)
print('Pages unvisited:', totalHTMLPagesUnvisited)
print('Pages visited {0} out of {1} coverage {2:.2f}%\n'.format(totalHTMLPagesVisited, totalHTMLPagesSV, (
float(totalHTMLPagesVisited) / totalHTMLPagesSV) * 100))
writeResultToFile()
