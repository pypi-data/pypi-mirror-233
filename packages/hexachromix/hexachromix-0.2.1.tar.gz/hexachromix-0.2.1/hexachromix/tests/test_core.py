from unittest import TestCase
from hexachromix.core import HexachromixState

class TestCore(TestCase):
    def setUp(self):
        self.longMessage = True


    def test_hfen(self):
        #test init with 3 vars -- board:list=[0]*19, player:int=0, variant:str="MRY"
        #test init with hfen
        pass


    # Test MCTS functions.

    def test_get_current_team(self):
        pass

    def test_get_legal_moves(self):
        pass

    def test_make_move(self):
        pass

    def test_is_terminal(self):
        # Not terminal.
        hfens = (
            '3/4/5/4/3 R MRY',
            '3/4/5/4/3 R MR',
            'GC1/BMRC/2R1c/MMYY/1BY C MRY',
        )
        for hfen in hfens:
            self.assertFalse(HexachromixState(hfen=hfen).is_terminal(), hfen)

        # Terminal.
        hfens = (
            'R2/R3/R4/R3/R2 Y MRY',
            '1bR/Yb1y/mYCrM/Bygy/YC1 B MRY',
        )
        for hfen in hfens:
            self.assertTrue(HexachromixState(hfen=hfen).is_terminal(), hfen)

    def test_get_reward(self):
        pass
