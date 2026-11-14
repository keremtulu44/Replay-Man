#!/usr/bin/env bash
# Erdem'in commit'ini bekler.
#
# - Yalnızca izlenen dala fetch yapar; yerel branch değiştirmez/oluşturmaz,
#   merge/pull yapmaz, working tree'ye dokunmaz. Sadece remote-tracking ref güncellenir.
# - Yeni commit bulunca log'a COMMIT_RECEIVED yazar, erdem.md varsa basar ve çıkar.
#
# Ortam değişkenleri:
#   INTERVAL       kontrol aralığı (saniye), varsayılan 60
#   MAX_MINUTES    azami bekleme (dakika), varsayılan 360; 0 = sınırsız
#   BASE           karşılaştırılacak commit, varsayılan mevcut HEAD
#   WATCH_BRANCH   izlenecek dal, varsayılan mevcut dal
#
# Bayraklar:
#   --once   tek kontrol yap ve çık (duman testi)

set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

ONCE=0
[ "${1:-}" = "--once" ] && ONCE=1

INTERVAL="${INTERVAL:-60}"
MAX_MINUTES="${MAX_MINUTES:-360}"
BRANCH="${WATCH_BRANCH:-$(git branch --show-current)}"
BASE="${BASE:-$(git rev-parse HEAD)}"
REMOTE_REF="refs/remotes/origin/${BRANCH}"
ERDEM_FILE="agentlar/erdem.md"

if ! git check-ref-format --branch "$BRANCH" >/dev/null 2>&1; then
  echo "WATCH_ERROR: geçerli dal adı okunamadı" >&2
  exit 1
fi
if ! git rev-parse --verify --quiet "${BASE}^{commit}" >/dev/null; then
  echo "WATCH_ERROR: BASE yerelde geçerli bir commit değil" >&2
  exit 1
fi

remote_head() { git rev-parse --verify --quiet "$REMOTE_REF"; }

# Dar fetch refspec'i başka dalı izlesek bile yalnızca onun uzak izleme ref'ini
# günceller. Yerel dal/working tree değişmez. timeout takılmayı sınırlar.
fetch_branch() {
  local refspec="+refs/heads/${BRANCH}:${REMOTE_REF}"
  if command -v timeout >/dev/null 2>&1; then
    timeout 90 git fetch --quiet origin "$refspec"
  else
    git fetch --quiet origin "$refspec"
  fi
}

report_new_commits() {
  local remote="$1"
  echo "COMMIT_RECEIVED $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "branch=${BRANCH}"
  echo "base=${BASE}"
  echo "remote=${remote}"
  echo "--- yeni commit'ler ---"
  git --no-pager log --oneline --no-decorate "${BASE}..${remote}"
  echo "--- değişen dosyalar ---"
  git --no-pager diff --stat "${BASE}" "${remote}"
  if git cat-file -e "${remote}:${ERDEM_FILE}" 2>/dev/null; then
    echo "--- ${ERDEM_FILE} (remote:${BRANCH}) ---"
    git --no-pager show "${remote}:${ERDEM_FILE}"
    echo "--- erdem.md sonu ---"
  else
    echo "NOT: ${ERDEM_FILE} bu commit'te yok"
  fi
  echo "WATCH_DONE"
}

echo "WATCH_START $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "branch=${BRANCH} base=$(git rev-parse --short "$BASE") interval=${INTERVAL}s max_minutes=${MAX_MINUTES} once=${ONCE}"

started=$(date +%s)
failures=0
checks=0

while :; do
  checks=$((checks + 1))

  if fetch_branch; then
    failures=0
    remote="$(remote_head || true)"
    if [ -n "${remote}" ] && [ "$remote" != "$BASE" ]; then
      report_new_commits "$remote"
      exit 0
    fi
    echo "waiting check=${checks} $(date -u '+%H:%M:%S') head=${BASE:0:7} yeni_commit=yok"
  else
    failures=$((failures + 1))
    echo "FETCH_RETRY ${failures}/10 $(date -u '+%H:%M:%S') fetch başarısız, tekrar denenecek"
    if [ "$failures" -ge 10 ]; then
      echo "WATCH_ERROR: art arda 10 fetch başarısız (ağ veya GitHub bağlantısı)" >&2
      exit 1
    fi
  fi

  if [ "$ONCE" -eq 1 ]; then
    echo "WATCH_ONCE_DONE yeni_commit=yok"
    exit 0
  fi

  if [ "$MAX_MINUTES" -gt 0 ]; then
    now=$(date +%s)
    if [ $((now - started)) -ge $((MAX_MINUTES * 60)) ]; then
      echo "WATCH_TIMEOUT ${MAX_MINUTES} dakika içinde yeni commit gelmedi"
      exit 0
    fi
  fi

  sleep "$INTERVAL"
done
