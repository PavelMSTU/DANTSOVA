# -*- coding: utf-8 -*-
"""
    This is module of acrostego.
    You can use it, if platform is build.

    If platform is not build, please use:
    1) collect *.fb2 files in your language
    2) run build_platform
    3) spend a lot of time... (Ha-ha-ha!! MANY TIME!!!)
    4) rejoice!
    5) run this module
    6) rejoice again!

    PavelMSTU@stego.su
    ~I am SOMBE(=Sorry Of My Bad English)
    create in: 2014-08-06
"""

__version__ = "07.09.2014"
__author__ = 'PavelMSTU'
__copyright__ = 'LGPL'

import os
import datetime

from MarkoffLib import load_chain, make_acrotext

# Path to built platform
PLATFORM_PATH = os.path.join(u'platform_build', u'dantsova.d0.plf')

# Correct alphabet of your language
CORRECT_ALPHABET = u'йцукенгшщзхъфывапролджэячсмитьбю'


import random


def test(message):
    random.seed(message)
    platform = load_chain(PLATFORM_PATH)

    if not platform:
        error = u'Not platform in "{0}"'.format(PLATFORM_PATH)
        raise EnvironmentError(error)

    all_text_by_c = dict()
    for c in [8, 10, 12, 20]:
        text = make_acrotext(platform, message, c=c, correct_alphabet=CORRECT_ALPHABET)

        print u"return text. c=@c@ message='@m@'::"\
            .replace(u'@c@', str(c))\
            .replace(u'@m@', message)
        print "::::"
        text2 = text.replace(u'.', u'.\n')
        all_text_by_c[c] = text
        print text2
        print "::::"

    print u'All text by c param:'
    for c in all_text_by_c.keys():
        print u"c={0}. m={1}. text={2}".format(c, message, all_text_by_c[c])

##############
if __name__ == '__main__':
    # Please, enter message here.
    message = u'глокая куздра штеко будланула бокра и кудрячит бокрёнка'

    begin = datetime.datetime.now()
    print "Stego.test() begin" + str(begin)
    test(message=message)
    end = datetime.datetime.now()
    print "All is done" + str(end)
    print "Spend time:" + str(end-begin)