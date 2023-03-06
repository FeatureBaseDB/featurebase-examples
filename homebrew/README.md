# FeatureBase Homebrew Cask
This is a Homebrew Cask example for installing featurebase with [Homebrew](https://brew.sh/).

## Copy the Cask File
Copy the `featurebase.rb` cask file to the proper location:

```
git clone https://github.com/FeatureBaseDB/featurebase-examples.git
cd featurebase-examples/homebrew
cp /opt/homebrew/Library/Taps/homebrew/homebrew-cask/Casks/featurebase.rb
```

## Install the Cask File
Using the `brew install` command install the `featurebase` binary without quarantining it on macOS:

```
brew install --no-quarantine featurebase
```

## Run FeatureBase
To run FeatureBase, enter the following:

```featurebase server```

*OUTPUT*:

```
2023-03-06T23:44:48.100589Z INFO:  Molecula Pilosa v3.33.0 (Mar  2 2023 12:06AM, 9386fc7) go1.19.3
2023-03-06T23:44:48.118834Z INFO:  cwd: /Users/kord
2023-03-06T23:44:48.118838Z INFO:  cmd line: featurebase server
2023-03-06T23:44:48.190867Z INFO:  enabled Web UI at :10101
2023-03-06T23:44:48.191180Z INFO:  open server. PID 63873
...
```

## Uninstall FeatureBase
Uninstall the cask using:

```
brew uninstall featurebase
```

