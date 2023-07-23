from requests import get
from glob import glob
import os

stitch_regex = '"^[a-z/]+$"'

# Notes on matches:
# All matches in skyrising's set have filenames of the form <from>#<to>.match
# which makes it easy to parse out the version numbers.
# Fabric ruins this, though, using <from>-<to>.match. The issue comes when trying
# to parse out the version numbers, as the version numbers can contain dashes.
# Take '1.14.3-pre1-1.14.3-pre2.match' for example. The version numbers are
# '1.14.3-pre1' and '1.14.3-pre2', but parsing out the version numbers from the
# filename would give '1.14.3' and 'pre1-1.14.3-pre2'.
# The solution that I arbitrarily chose: find a `-1.` and re-add the `1.` to the
# 'to' version number. This doesn't work for snapshots, but if there's a snapshot,
# there's a `w` in whichever part is the snapshot.
# Then there's the special versions. Exactly sixteen matches are between "combat"
# or "experimental" versions (with some other version as well), which causes immense
# pain. Let's just worry about those later.

# (not to mention that there are some random 1.13 matches in fabric's set)

# Pre-1.3
matches: dict[str, tuple[str, str]] = {}
for match in glob('matches/matches/client/**/*.match', recursive=True):
    f, t = os.path.basename(match)[:-6].split('#')
    if f in matches:
        print('Duplicate match for %s -> %s: %s' % (f, t, matches[f]))
        continue

    matches[f] = t, match

# 1.3 client -> merged
matches['12w30e'] = '1.3-pre-07261249', 'matches/matches/cross/1.3/client-12w30e#merged-1.3-pre-07261249.match'

# 1.3 thru 1.14 first snapshot
for match in glob('matches/matches/merged/**/*.match', recursive=True):
    f, t = os.path.basename(match)[:-6].split('#')
    if f in matches:
        print('Duplicate match for %s -> %s: %s' % (f, t, matches[f]))
        continue

    matches[f] = t, match

# 1.14+
for match in glob('fabric-intermediaries/matches/*.match', recursive=True):
    if '1.13' in match or 'combat' in match or 'experimental' in match:
        print('Skipping special match %s' % match)
        continue
    basename = os.path.basename(match)[:-6]
    if 'w' in basename:
        parts = basename.split('-')
        snapshot = [p for p in parts if 'w' in p][0]
        f, t = snapshot, '-'.join([p for p in parts if p != snapshot])
        if not basename.startswith(snapshot):
            f, t = t, f

    if f in matches:
        print('Duplicate match for %s -> %s: %s' % (f, t, matches[f]))
        continue

    matches[f] = t, match

stitch_jar = 'stitch.jar'
if not os.path.exists(stitch_jar):
    print('Downloading stitch...')
    with open(stitch_jar, 'wb') as f:
        with get('https://maven.fabricmc.net/net/fabricmc/stitch/0.6.2/stitch-0.6.2-all.jar', stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

versions_with_previous_match = [v for _, (v, _) in matches.items()]
versions_without_previous_match = [k for k, _ in matches.items() if k not in versions_with_previous_match]

current_item = versions_without_previous_match[0]
while current_item in matches.keys():
    f = current_item
    t, match = matches[f]
    input_location = 'matches/versions/%s/client.jar' % f
    output_location = 'matches/versions/%s/client.jar' % t
    intermediary_in = 'intermediary/%s.tiny' % f
    intermediary_out = 'intermediary/%s.tiny' % t

    if os.path.exists(intermediary_out):
        print('Intermediary for %s -> %s already exists, skipping...' % (f, t))
        current_item = t
        continue

    print('Generating intermediary for %s -> %s' % (f, t))
    function = 'java -jar %s updateIntermediary %s %s %s %s %s -p %s' % (
        stitch_jar, input_location, output_location, intermediary_in, intermediary_out, match, stitch_regex
    )

    ret = os.system(function)
    if ret != 0:
        print('Failed to generate intermediary for %s -> %s (exit code %d)' % (f, t, ret))
        exit(1)
    
    current_item = t
