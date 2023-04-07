cask "featurebase" do
  version "3.33.0"
  sha256 "5bf8a675ccf36d55bca66424d144ac18a8f21000212cdd77058e52e2fc0fc03f"

  url "https://github.com/FeatureBaseDB/featurebase/releases/download/v#{version}/featurebase-v#{version}-brew-darwin-universal.tgz"
  name "featurebase"
  desc "crazy fast distributed b-tree index with SQL"
  homepage "https://featurebase.com/"

  livecheck do
    url :url
    regex(/^v?\.?(\d+(?:\.\d+)+)$/i)
  end

  binary "featurebase"
end
