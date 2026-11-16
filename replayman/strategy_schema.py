"""ATK P8-P12 strateji kartı ve süreç sözleşmesi doğrulayıcıları."""
from __future__ import annotations
from typing import Any
ALLOWED_KNOWN_AT={'bar_close','confirmed_pivot','completed_higher_timeframe'}
REQUIRED={'id','version','universe','context','setup','trigger','invalidation','outcomes','validation'}

def validate_strategy_card(card:dict[str,Any])->list[str]:
 errors=[]
 for key in sorted(REQUIRED-set(card)):errors.append(f'eksik alan: {key}')
 universe=card.get('universe',{})
 if not universe.get('groups'):errors.append('universe.groups boş olamaz')
 if not universe.get('intervals'):errors.append('universe.intervals boş olamaz')
 if universe.get('volume_required') and any(x in {'fx','bist_indices','global_indices'} for x in universe.get('groups',[])):errors.append('temsili/merkezi olmayan hacim grubu volume_required olamaz')
 for name in ('context','setup','trigger','invalidation'):
  expr=card.get(name,{})
  if expr.get('known_at') not in ALLOWED_KNOWN_AT:errors.append(f'{name}.known_at geçersiz')
  if not expr.get('operands'):errors.append(f'{name}.operands boş olamaz')
 for ind in card.get('indicators',[]):
  if ind.get('known_at') not in ALLOWED_KNOWN_AT:errors.append(f"indikatör {ind.get('id','?')} known_at geçersiz")
  if 'external' in ind.get('data_requirements',[]) and not ind.get('implementation'):errors.append('harici veri indikatörü implementation ister')
 v=card.get('validation',{})
 if v.get('chronological_split') != [0.6,0.2,0.2]:errors.append('chronological_split [0.6,0.2,0.2] olmalı')
 if v.get('preserve_negative_results') is not True:errors.append('negatif sonuçlar korunmalı')
 if int(v.get('minimum_symbols',0))<1:errors.append('minimum_symbols pozitif olmalı')
 o=card.get('outcomes',{})
 if not o.get('horizons') or any(int(x)<1 for x in o.get('horizons',[])):errors.append('pozitif outcome horizons gerekli')
 if card.get('execution') not in {'research_only','deferred_execution_portfolio'}:errors.append('execution araştırma veya deferred olmalı')
 return errors

def strategy_card_is_valid(card:dict[str,Any])->bool:return not validate_strategy_card(card)
