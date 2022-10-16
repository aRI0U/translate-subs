mkdir -p raw

for ((i=1; i<1000; i++))
do
  var=$(printf "%04d" "$i")
  echo -e "$var\r"
  wget -nc -q -P raw/ https://raw.githubusercontent.com/x-cord/conan-sources/master/English/Crunchyroll/"$var".ass
done

echo Done.