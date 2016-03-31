# -*- coding: utf-8 -*-
"""
    This script build `platform`.
    Platform is dictionary
    Using this dictionary you can build Markov chain.

    PavelMSTU@stego.su
    ~I am SOMBE(=Sorry Of My Bad English)
    create in: 2014-08-03
"""
__version__ = "07.09.2014"
__author__ = 'PavelMSTU'
__copyright__ = 'LGPL'

import os
import sys
import xml.dom.minidom as xmlp
import json
import codecs
import datetime

CORRECT_ALPHABET = u' .qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю'

DEBUG = False

DEFAULT_PRINT_CONSOLE_INFO = False

PLATFORM_PATH = os.path.join(u'platform_build', u'dantsova.d@i@.plf')
PLATFORM_PATH_IN = u'platform_in'


from MarkoffLib import safe_chain, load_chain


def make_chain(i, dictlist, print_to_console_info=DEFAULT_PRINT_CONSOLE_INFO):
    """
    Make Markov Chain FROM dictlist

    see also: MakeDict

    return:
        dict where key is word, value is list of list:
            nextword, count
    """
    def PrintPercent(count_TEMP, step, list_old_value):
        """
        print string like 10,45%

        """
        if step==0:
            return None
        old_value = list_old_value[0]
        new_value = count_TEMP / step
        if new_value==old_value:
            return None
        list_old_value[0] = new_value
        per = new_value / 100
        dper = new_value %100
        str_ = '@i@::@per@.@dper@ %'.\
            replace('@i@', str(i)).\
            replace('@per@', str(per)).\
            replace('@dper@', str(dper))
        print str_ + '  append:'+ str(count_TEMP) +"  " + str(datetime.datetime.now())
        return str_
    chain = dict()
    count_ALL = len(dictlist)
    count_TEMP = 0
    step = 1 + count_ALL / (100 * 100)
    list_old_value = [0]

    for pear in dictlist:
        count_TEMP +=1
        word = pear[0]
        nextword = pear[1]

        try:
            word = word.encode('utf8')
            nextword = nextword.encode('utf8')
        except:
            print u'WARNING: cant encode word-nextword : @word@->@nextword@'.\
                replace(u'@word@', word).replace(u'@nextword@', nextword)
            continue

        PrintPercent(count_TEMP, step, list_old_value)

        if word in chain:
            pot = chain[word]
            #pot = list(pot)
            is_exist = False
            for index in range(len(pot)):
            #for nextpot in pot:
                nextpot = pot[index]
                nextword_ch = nextpot[0]
                if nextword == nextword_ch:
                    #index = pot.index(nextword_ch)
                    count = chain[word][index][1]
                    if print_to_console_info and count%100==0 and word!='.':
                        print 'Thera are @count@ ones "@word@"-->"@nextword@" in text!!'.\
                            replace('@word@', word).\
                            replace('@nextword@', nextword).\
                            replace('@count@', str(count))
                        #INFO здесь интересно ставить бряки
                        pass
                    #index = pot.index(nextword_ch)
                    chain[word][index][1] += 1
                    is_exist = True
            if not is_exist:
                if print_to_console_info:
                    print 'in word "@word@" new nextword: "@nextword@"'.\
                        replace('@word@', word).\
                        replace('@nextword@', nextword)
                nextpot = [nextword, 1]
                chain[word].append(nextpot)
        else:
            if print_to_console_info:
                print 'new word "@word@" with new nextword "@nextword@"'.\
                          replace('@word@', word).\
                          replace('@nextword@', nextword)
            nextpot = [nextword, 1]
            pot = [nextpot]
            chain[word] = pot
    if print_to_console_info:
        print "Chain is build. Count pots is @count@".\
            replace('@count@', str(len(chain)))

    return chain


def make_dict(mtext, var_dictlist):
    """
    return
        count of appends



    mtext -- text after Text2MachineText
    var_appendlist -- list of pears word, nextword
        VARIABLE
    """

    words = mtext.split(u' ')
    #words = words.remove(u"")

    i = 0
    count= 0
    #retlist = list()
    while i+1 < len(words):
        word = words[i]
        nextword = words[i+1]
        append = word, nextword
        var_dictlist.append(append)
        count += 1
        #TODO в будущем count не будет равнятся i
        i += 1
    return count


def text2machine_text(text, always_point_in_end=True,
                     print_to_console_info=DEFAULT_PRINT_CONSOLE_INFO,
                     uncorrect_symbols = None):
    """
    This function convert human text to machin text.
    Thease mean:
    1) all UP latters goto down. A->a B->b ... Я->я
    2) !, ?, .. --> .
    3) anoter punctiation mark deleted
    4) russian ё->е
    5) '  ' -> ' '
    6) in end always '.' if always_point_in_end
    """
    try:
        text = unicode(text)
        if uncorrect_symbols is not None:
            uncorrect = uncorrect_symbols
        else:
            uncorrect = list()

        text = text.lower()
        #print u"l:"+text
        text = text.replace(u'!', u'.').replace(u'?', u'.')

        if always_point_in_end:
            text += u'.'
        for i in range(7):
            text = text.replace(u'..', u'.')

        text = text.replace(u'.', u' .')

        text = u" " + text + u" "
        for i in range(7):
            text = text.replace(u'  ', u' ')


        text = text.replace(u'ё', u'е')
        text = text[1:-1]
        text_ch = text
        first_print = True
        for letter in text_ch:
            if letter not in CORRECT_ALPHABET:
                #str_letter = str(letter)
                if letter not in uncorrect:
                    if print_to_console_info:
                        if first_print:
                            print u"INFO: Uncorrect symbols::"
                            first_print = False
                        print u"'@L@' (@STR@)".\
                            replace(u'@L@', letter).\
                            replace(u'@STR@', u'TODO') #TODO   )unicode(str_letter))

                    uncorrect.append(letter)

                text = text.replace(letter, u"")

        return text
    except:
        print "ERROR in Text2MachineText. exc_info=" + str(sys.exc_info())
        print text


def get_text_from_fb2(path, uncorrect_symbols=None):
    """
    Get text from *.fb2 file.
    Using this text we can make markov chain
    """
    app_xml = xmlp.parse(path)

    text_strings = app_xml.getElementsByTagName('p')
    alltext = u''
    isfirst = True
    for p in text_strings:
        try:
            text = p.toxml().replace(u'<p>', u'').replace(u'</p>', u'')
            mtext = text2machine_text (text, uncorrect_symbols=uncorrect_symbols)

            if mtext[-1] != u' ' and not isfirst:
                alltext += u' ' + mtext
            else:
                alltext += mtext
            isfirst = False
            #print text
           # print mtext
        except:
            print "ERROR in <p>="+p.toxml
    #print 'EEE'
    return alltext


def get_all_files(path):
    """
    Get all files from path

    return list of all files
    """
    def __is_folder(param):
        if '.' in param:
            return False
        return True
    def __get_iter(path, listfiles):
        """
        get files and insetr it to listfiles,
        get folders and run __get_iter(path, listfiles)
        """
        try:
            for param in os.listdir(path):
                param_add = path + '\\' + param
                if __is_folder(param):
                    __get_iter(param_add, listfiles)
                else:
                    listfiles.append(param_add)
        except:
            print 'WARNING in GetFiles.__get_iter::\n\tpath=@path@; listfiles=@listfiles@'.\
                replace('@path@', str(path))


    try:
        pofig = os.listdir(path)
    except:
        print 'ERROR in GetFiles::\n\t uncorrect path! path=' + str(path)
        return list()

    listfiles = list()
    __get_iter (path, listfiles)


    return listfiles


def make_report_and_save(path, chain, good_books, bad_books, begintime, endtime, uncorrect):
    """

    """
    fw = codecs.open(path+u".report.txt", 'w', encoding='utf8')

    goodfiles = u""
    badfiles = u""
    for file_ in good_books:
        goodfiles += file_ + u"\n"
    for file_ in bad_books:
        badfiles += file_ + u"\n"

    uncorrectstr = u""
    for unc in uncorrect:
        uncorrectstr += u"u'" + unc + u"',"
    uncorrectstr = u"[" + uncorrectstr[:-1] + u"]"

    report = u"""Платформа для алгоритма DONЦОVA #1.
            Дата создания: @date@
            Потраченное время:
            @spend_time@

            Количество слов (= Количество узлов в цепи Маркова):
            @count_words@

            Количество обработанных книг:
            @good_books@

            Количество книг, обработанные с ошибкой:
            @bad_books@

            Список некоректных символов:
            @uncorrectstr@

            Файлы:
            @goodfiles@
            Файлы без ошибок:
            @badfiles@
            """.\
        replace(u'@date@', str(datetime.datetime.now())).\
        replace(u'@count_words@',  str(len(chain))).\
        replace(u'@spend_time@', str(endtime-begintime)).\
        replace(u'@good_books@', str(good_books)).\
        replace(u'@bad_books@', str(bad_books)).\
        replace(u'@goodfiles@', goodfiles).\
        replace(u'@badfiles@', badfiles).\
        replace(u'@uncorrectstr@', uncorrectstr)
    fw.write(report)
    fw.close()


def build_platform_chunk(i, files, path):
    dict_list = list()
    uncorrect = list()

    count = 0

    begintime = datetime.datetime.now()

    #files = list()
    count_books = 0
    good_books = list()
    bad_books = list()

    for file in files:
        try:
            alltext = get_text_from_fb2(file, uncorrect_symbols=uncorrect)
            count += make_dict(alltext, var_dictlist=dict_list)
            count_books +=1
            #if print_to_console_info:
            print u"@i@::@count_books@. From file @file@ append @count@ pears".\
                    replace(u'@i@', str(i)).\
                    replace(u'@file@', file).\
                    replace(u'@count@', str(count)).\
                    replace(u'@count_books@', str(count_books))
            print str(datetime.datetime.now())
            good_books.append(file)
        except:
            print u"ERROR in file @file@. err=@err@".\
                replace(u'@file@', file).\
                replace(u'@err@', str(sys.exc_info()))
            bad_books.append(file)

    # TO DO
    #dict_list = dict_list[0:10000]


    print "Now MakeChain: " + str(datetime.datetime.now())

    chain = make_chain(i,dict_list)

    print "Now safe: " + str(datetime.datetime.now())
    safe_chain(chain, path)

    endtime = datetime.datetime.now()

    make_report_and_save (path, chain, good_books, bad_books, begintime, endtime, uncorrect)

    if DEBUG:
       # pot_first = chain['я']
        new_chain = load_chain(path)
        pot_second = new_chain[u'я']
       # print "pot before safe:" + str(pot_first)
        print "pot after safe:" + str(pot_second)
        #INFO тут уместнее поставить бряку и сравнить ручками через отладчик
        pass
    print 'All work to buld platform is END!'


def build_platform(path_out, path_in, count_chunk=1):
    """
    Function for building pldtform by *.fb2 files.

    Attention: this function can be work VERY SLOW...
    Ye, i am tórmozz(=brake-man), i must write this function by pure C,
    but... it is lazily...

    :param path_out: path to output platform building by this function.
    :param path_in: path to main folder.
    Folder can includes more folders, subfolders and subsubfolders and (sub)*folders...
    All files of folders must be *.fb2 files.
    Files must be in russian or english language.
    If you want use another language, please:
        1) check, thet alphabet of your language includes into utf-8 format
        2) change CORRECT_ALPHABET. (Ye!.. There is a trouble, if you are chanise ;)) )

    :param count_chunk: you can build more then one platform, if you want.
    *) if something is unclear, you can write to pavelmstu@stego.su (only serbian, russian or english, please)
    """
    files = get_all_files(path_in)

    step = len(files)/count_chunk
    files_chunklist = list()
    for i in range(count_chunk):
        if i<count_chunk-1:
            files_chunk = files[i*step: (i+1)*step]
        else:
            files_chunk = files[i*step:]
        files_chunklist.append(files_chunk)

    for i in range(count_chunk):
        path_chunk = path_out\
            .replace(u'@i@', unicode(i))
        build_platform_chunk(i, files_chunklist[i], path_chunk)


############
if __name__ == "__main__":
    build_platform(PLATFORM_PATH, PLATFORM_PATH_IN)

