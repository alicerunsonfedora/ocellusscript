#!/bin/sh
echo "Deploying to docs..."
mkdocs build -d docs
echo "ocls.marquiskurt.net" >> docs/CNAME
touch docs/.nojekyll
