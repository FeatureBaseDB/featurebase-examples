cask "featurebase" do
  version "3.33.0"
  sha256 "0e94973eb934fe4c64ddefdef7d948e08e39ea4f255313d0c6f0635341e951e3"

  url "https://github.com/FeatureBaseDB/featurebase/releases/download/v#{version}/featurebase-brew-v#{version}-darwin-amd64.tgz"
  name "featurebase"
  desc "crazy fast distributed b-tree index with SQL"
  homepage "https://featurebase.com/"

  livecheck do
    url :url
    regex(/^v?\.?(\d+(?:\.\d+)+)$/i)
  end

  binary "featurebase"
end