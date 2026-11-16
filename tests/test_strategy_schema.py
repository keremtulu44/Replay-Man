from replayman.strategy_schema import validate_strategy_card

def card():
 e={'operator':'event','operands':['close_break'],'known_at':'bar_close'}
 return {'id':'x','version':'1','universe':{'groups':['bist_equities'],'intervals':['4h'],'volume_required':True},'context':e,'setup':e,'trigger':e,'invalidation':e,'indicators':[],'outcomes':{'horizons':[5,20,60],'benchmark':'XU100_excess','mfe_mae':True,'costs':[0,.001]},'validation':{'chronological_split':[.6,.2,.2],'common_calendar':True,'minimum_symbols':70,'parameter_neighbourhood':True,'preserve_negative_results':True},'execution':'research_only','ob_fvg':'deferred_ob_fvg'}
def test_valid_strategy_card():assert validate_strategy_card(card())==[]
def test_future_visibility_and_volume_misuse_rejected():
 x=card();x['trigger']={**x['trigger'],'known_at':'future'};x['universe']['groups']=['fx'];e=validate_strategy_card(x);assert any('known_at' in z for z in e);assert any('volume_required' in z for z in e)
def test_negative_results_must_be_preserved():
 x=card();x['validation']['preserve_negative_results']=False;assert 'negatif sonuçlar korunmalı' in validate_strategy_card(x)
