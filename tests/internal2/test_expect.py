import mock
import pexpect
import utils
utils.append_home_to_path(__file__)
import tomahawk.expect

class TestCommandWithExpect(object):
    
    def test_01_execute(self):
        target = self._create_object()
        patch = mock.patch('pexpect.spawn.expect')
        patch.start()
        pexpect.spawn.expect.return_value = 0
       #print "target = " + str(target)
        target.execute()
        assert 1 == 'fuga'
    
    def _create_object(self):
        return tomahawk.expect.CommandWithExpect(
            'ssh', [ '-t' ], 'hoge', 'hoge', debug_enabled=True)
