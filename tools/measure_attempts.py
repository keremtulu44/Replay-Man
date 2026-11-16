"""İlk/ikinci swing denemelerini bütün OHLCV evreninde ölçer."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

from replayman.attempts import attach_attempt_outcomes, compare_directional_legs
from replayman.replay import causal_features, load_bars
from replayman.swings import multi_level_swings, swing_legs

ROOT=Path("data/ohlcv"); OUT=Path("research/measurements/attempts")
HORIZONS=(5,20,40,60)

def positive_rate(x):
    x=x.dropna(); return float((x>0).mean()) if len(x) else float("nan")

def discover(): return sorted(ROOT.glob("*/*/*/bars/*.csv"))

def main():
    OUT.mkdir(parents=True,exist_ok=True); parts=[]
    for path in discover():
        bars=load_bars(path); features=causal_features(bars)
        events=compare_directional_legs(swing_legs(multi_level_swings(bars,features),bars),bars,features)
        results=attach_attempt_outcomes(events,bars,HORIZONS)
        if results.empty: continue
        results.insert(0,"group",path.parts[-5]); results.insert(1,"asset_id",str(bars.get("asset_id",pd.Series([path.parts[-4]])).iloc[0])); results.insert(2,"interval",path.stem)
        parts.append(results)
    all_events=pd.concat(parts,ignore_index=True)
    all_events.event_ts=pd.to_datetime(all_events.event_ts,utc=True)
    # XU100 benchmark
    benchmarks=[]
    for path in discover():
        if path.parts[-4]!="IDX_XU100": continue
        bars=load_bars(path); part=pd.DataFrame({"interval":path.stem,"event_ts":bars.ts_utc})
        for h in HORIZONS: part[f"benchmark_return_{h}"]=bars.close.shift(-h).div(bars.close).sub(1)
        benchmarks.append(part)
    all_events=all_events.merge(pd.concat(benchmarks,ignore_index=True),on=["interval","event_ts"],how="left")
    sign=all_events.thesis_direction.map({"up":1,"down":-1})
    for h in HORIZONS: all_events[f"directional_excess_{h}"]=all_events[f"directional_return_{h}"]-sign*all_events[f"benchmark_return_{h}"]
    rank=all_events.groupby(["asset_id","interval"]).event_ts.rank(method="first",pct=True)
    all_events["time_split"]=pd.cut(rank,[0,.6,.8,1],labels=["train","validation","test"],include_lowest=True)
    all_events["distance_band"]=pd.cut(all_events.distance_ratio,[-float("inf"),.7,1.0,1.3,float("inf")],labels=["much_weaker","weaker","similar","stronger"])
    all_events["speed_band"]=pd.cut(all_events.speed_ratio,[-float("inf"),.7,1.0,1.3,float("inf")],labels=["much_slower","slower","similar","faster"])
    all_events["duration_band"]=pd.cut(all_events.duration_ratio,[-float("inf"),.7,1.0,1.5,float("inf")],labels=["shorter","similar","longer","much_longer"])
    all_events.to_csv(OUT/"attempt_events.csv",index=False)
    keys=["group","interval","time_split","event","direction","thesis_direction"]
    def aggregate(grouped):
        spec={"observations":("asset_id","size"),"assets":("asset_id","nunique")}
        for h in HORIZONS:
            spec.update({f"ready_{h}":(f"directional_return_{h}","count"),f"median_return_{h}":(f"directional_return_{h}","median"),f"win_rate_{h}":(f"directional_return_{h}",positive_rate),f"ready_excess_{h}":(f"directional_excess_{h}","count"),f"median_excess_{h}":(f"directional_excess_{h}","median"),f"excess_win_rate_{h}":(f"directional_excess_{h}",positive_rate)})
        return grouped.agg(**spec).reset_index()
    aggregate(all_events.groupby(keys,observed=True)).to_csv(OUT/"attempt_time_split_study.csv",index=False)
    context=[]
    for dim in ("distance_band","speed_band","duration_band"):
        part=aggregate(all_events.groupby(keys+[dim],observed=True)).rename(columns={dim:"band"}); part.insert(len(keys),"context_dimension",dim); context.append(part)
    pd.concat(context,ignore_index=True).to_csv(OUT/"attempt_context_study.csv",index=False)
    symbol=aggregate(all_events.groupby(["group","asset_id","interval","event","direction","thesis_direction"],observed=True))
    symbol.to_csv(OUT/"attempt_symbol_results.csv",index=False)
    summary={"schema_version":1,"events":len(all_events),"assets":int(all_events.asset_id.nunique()),"series":int(all_events.groupby(['asset_id','interval']).ngroups),"event_counts":all_events.event.value_counts().to_dict(),"source_rule":"Cilt 2 Bölüm 9-10: ikinci deneme ve beklenen yeni uç"}
    (OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
