#!/usr/bin/env python

import subprocess
from pprint import pprint
import re
import sys
import os
import semver

result = subprocess.run(["$HOME/.asdf/bin/asdf list-all 1password-cli"], shell=True, capture_output=True, text=True)
versions = result.stdout.split("\n")
print(f"{len(versions)} versions found")

versions = [version for version in versions if re.search('^\d+\.\d+\.\d+$', version)]
print(f"{len(versions)} released versions found")

# nothing older than 0.5.5 is still downloadable
oldest_acceptable = semver.Version.parse("0.5.5")
versions = [version for version in versions if semver.Version.parse(version) >= oldest_acceptable]
print(f"{len(versions)} plausible versions found")

versions = ['0.5.4', '1.11.0', '2.21.0']

successes = []
failures = []

for v in versions:

  try:
    result = subprocess.run([f"{os.environ['HOME']}/.asdf/bin/asdf install 1password-cli {v}"], shell=True, capture_output=True, text=True)
    result.check_returncode()

    result = subprocess.run([f"echo '1password-cli {v}' > ~/.tool-versions"], shell=True, capture_output=True, text=True)
    result.check_returncode()

    result = subprocess.run([f"op --version 2>&1 | grep '{v}'"], shell=True, capture_output=True, text=True)
    result.check_returncode()

    if re.search(v, result.stdout):
      print("yay")
      successes.append(v)
      continue

    print("Not sure how I got here, probably bad")
    sys.exit(1)

  except subprocess.CalledProcessError as error:
    if result.returncode != 0:
      print(f"Version {v} failed to install")
      print(f"stdout: '{result.stdout.strip()}'")
      print(f"stderr: '{result.stderr.strip()}'")
      failures.append(v)
      continue

print(f"{len(failures)} failed to install")
pprint(failures)

print(f"{len(successes)} successfully installed")
pprint(successes)

if len(failures) > 0:
  sys.exit(1)
