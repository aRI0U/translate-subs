mkdir -p raw

for ((i=761; i<1038; i++))
do
  var=$(printf "%04d" $i)
  echo -e "$var\r"
  wget -nc -q -P raw/ https://raw.githubusercontent.com/x-cord/conan-sources/master/French/ADN/"$var".ass
done

echo Done.