import sys
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages

STYLES = {
    'se': format([56, 158, 5], 'bold'),
    'keyword': format([200, 120, 50], 'bold'),
    'operator': format([150, 150, 150],'bold'),
    'separator': format([220, 220, 255]),
    'idf': format([220, 220, 255], 'bold'),
    'comment': format([128, 128, 128]),
    'let': format([150, 85, 140], 'italic'),
    'numbers': format([100, 150, 190]),
}


class MiniLangHighlighter(QSyntaxHighlighter):
    # key words 
    se = [
        'begin','end',
    ]

    keywords = [
        'while','ewhile','if','eif','else','eelse',
    ]

    operators = [
        '-','*','+','/',
    
        '%',
        '=',
        '~',
        '>',
        '<',
        '<<', # write 
        '>>', # read 
        
        
        ]


    # separator
    separator = [
        '\(', '\)',':',';',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        rules = []

        # Se , Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['se'])
                  for w in MiniLangHighlighter.se]


        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in MiniLangHighlighter.keywords]


        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in MiniLangHighlighter.operators]


        rules += [(r'%s' % b, 0, STYLES['separator'])
                  for b in MiniLangHighlighter.separator]

        # All other rules
        rules += [
            # 'let'
            (r'\let\b', 0, STYLES['let']),

            # identifier
            (r'\b_[a-z]\b', 0, STYLES['idf']),

            # From '&' until a newline
            (r'&[^\n]*', 0, STYLES['comment']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)