#import logging
#
#def test_ng(capsys):
#    logging.basicConfig(
#        level = logging.DEBUG)
#    logging.debug("hiho")
#    out, err = capsys.readouterr()
#    assert 1 == 2
#
#def test_ok(capsys):
#    logging.basicConfig(
#        filename = '/tmp/log',
#        level = logging.DEBUG)
#    logging.debug("hiho")
#    out, err = capsys.readouterr()
#    assert 1 == 2
