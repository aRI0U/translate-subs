mkdir -p raw

for ((i=761; i<1000; i++))
do
  echo -e "$i\r"
  wget -nc -q -P raw/ https://raw.githubusercontent.com/x-cord/conan-sources/master/French/ADN/0$i.ass
done
for ((i=1000; i<1038; i++))
do
  echo -e "$i\r"
  wget -nc -q -P raw/ https://raw.githubusercontent.com/x-cord/conan-sources/master/French/ADN/$i.ass
done

echo Done.