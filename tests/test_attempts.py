import pandas as pd

from replayman.attempts import attach_attempt_outcomes, compare_directional_legs


def bars(n=20):
    close=[100+i for i in range(n)]
    return pd.DataFrame({"ts_utc":pd.date_range("2026-01-01",periods=n,freq="h",tz="UTC"),"open":close,"high":[x+1 for x in close],"low":[x-1 for x in close],"close":close,"volume":100})


def leg(direction,start,end,start_price,end_price,known,eff=.8):
    distance=abs(end_price-start_price); duration=end-start
    return {"direction":direction,"start_position":start,"end_position":end,"known_at_position":known,"start_price":start_price,"end_price":end_price,"distance":distance,"duration_bars":duration,"speed_per_bar":distance/duration,"path_efficiency":eff}


def test_second_up_attempt_success_is_known_at_confirmation():
    frame=bars(); features=pd.DataFrame({"atr":[2.0]*len(frame)})
    legs=pd.DataFrame([leg("up",1,3,100,105,5),leg("down",3,5,105,102,7),leg("up",5,8,102,108,10)])
    result=compare_directional_legs(legs,frame,features)
    assert len(result)==1
    event=result.iloc[0]
    assert event.event=="new_extreme_success"
    assert event.thesis_direction=="up"
    assert event.known_at_position==10
    assert event.distance_ratio==1.2


def test_failed_down_attempt_reverses_thesis():
    frame=bars(); features=pd.DataFrame({"atr":[1.0]*len(frame)})
    legs=pd.DataFrame([leg("down",1,4,110,100,6),leg("up",4,6,100,106,8),leg("down",6,9,106,101,11)])
    event=compare_directional_legs(legs,frame,features).iloc[0]
    assert event.event=="new_extreme_failure"
    assert event.direction=="down"
    assert event.thesis_direction=="up"


def test_future_after_known_time_does_not_change_attempt():
    frame=bars(); features=pd.DataFrame({"atr":[1.0]*len(frame)})
    legs=pd.DataFrame([leg("up",1,3,100,105,5),leg("down",3,5,105,102,7),leg("up",5,8,102,104,10)])
    before=compare_directional_legs(legs,frame,features)
    changed=frame.copy(); changed.loc[11:,"close"]*=10
    after=compare_directional_legs(legs,changed,features)
    pd.testing.assert_frame_equal(before,after)


def test_outcome_uses_thesis_direction():
    frame=bars(); events=pd.DataFrame([{"known_at_position":3,"thesis_direction":"down"}])
    result=attach_attempt_outcomes(events,frame,(5,))
    assert result.iloc[0].directional_return_5 < 0
