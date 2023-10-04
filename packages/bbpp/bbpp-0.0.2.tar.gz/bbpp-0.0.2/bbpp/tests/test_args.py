from pytest import raises

from ..modules.service.argparser import ArgParser


def test_argparser_selects_pipeline():
    args = ArgParser.parse(['-p', 'test'])
    assert args.pipeline == 'test'


def test_argparser_config_requires_username_and_password():
    with raises(SystemExit, match=r'2'):
        ArgParser.parse(['config'])


def test_argparser_config_users_username_and_password():
    args = ArgParser.parse(['config', '-u', 'test', '-p', 'testpwd'])
    assert args.username == 'test'
    assert args.password == 'testpwd'
