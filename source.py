#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nchugueva'

import codecs
import HTMLParser
import os
import pprint  # выводит красиво json pprint
import re

import requests


class Parser (HTMLParser.HTMLParser):
    russian_regex = re.compile(ur'^[а-яА-Я]{2,}|а|и|у|в|с|к$')

    stock = []
    statusSearchIngredients = False  # Нашел ли состав

    state = None
    stateDegree = False  # найдена или нет степень препода

    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        self.currentTag = tag

        #if self.currentTag in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        self.stock.append(tag)

    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        if self.stock and self.currentTag == self.stock[-1]:
            self.stock.pop(-1)

    def handle_startendtag(self, tag, attrs):
        #print "Encountered an startend tag :", tag
        pass

    def handle_data(self, data):
        data = data.strip()  # убирает начальные и хвостовые пробелы
        if self.statusSearchIngredients and data:
            print data
            self.statusSearchIngredients = False
        if data and self.stock:
            self.searchIngredients(data)



    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)

        with open("dictionaryDegree.txt", "rb") as dictionaryDegree:
            self.degree = set(self.word(
                dictionaryDegree.read().lstrip(codecs.BOM_UTF8).decode("utf-8"))
            )  # разделили на слова и добавили в словарь

    #В эту переменную я передаю текущий тег
    currentTag = None

    #Метод делит текст в текущем теге на слова
    def word(self, data):
        words = [word for word in re.split(r" |\-|\)|\(|!|\.|:||;|,|/|'|\n|\r" + r'|"', data) if word.strip()]
        return words

    def searchIngredients(self, data):
        words = self.word(data)
        for currentWord in words:
            #print currentWord
            if currentWord == u'Состав':
                print data
                self.statusSearchIngredients = True


def main():

    request = {'key': 'AIzaSyDiRIlJiNSnA4OWe8nxyFTbdzWz_2892ss',
               'cx': '000821473745468610469:qu3bp9lvrlc',
               'q': u'"состав" "4810268017124"',
               'alt': 'json'}
    a = requests.get('https://www.googleapis.com/customsearch/v1', params=request, stream=True).json()
    print len(a['items'])

    for item in a['items']:
        link = item['link']
        print link
        r = requests.get(link)
        print r.status_code
        if r.status_code == requests.codes.ok:
            if r.text.lstrip().startswith('<!DOCTYPE'):
                parser = Parser()
                parser.feed(r.text.replace(u"&nbsp;", u" "))



main()