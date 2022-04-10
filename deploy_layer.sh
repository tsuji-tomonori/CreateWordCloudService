ROOT="layer"
FONT="${ROOT}/font"
REQUIREMENTS="${ROOT}/requirements/python/"

rm -rf ${ROOT}
mkdir -p ${ROOT}

mkdir -p ${FONT}
# git clone https://github.com/blagarde/midori.git ${FONT}
git clone https://github.com/fontdasu/ShipporiAntique.git ${FONT}

mkdir ${REQUIREMENTS}
pip install -r requirements.txt -t ${REQUIREMENTS}