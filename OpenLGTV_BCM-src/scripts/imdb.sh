#!/bin/sh
LOCKDIR="/var/run/imdb.lock"
# Ugly workaround w LOCKDIR for Haserl bug running the same scripts few times
if ! mkdir "$LOCKDIR" 2>/dev/null
then
    echo "Previous instance of $0 is still running. Exiting..."
    #sleep 1
    #while [ "`pgrep -f imdb.sh | grep -v grep | wc -w`" -ge "2" ]
    #do
#	sleep 0.2
    #done
    exit 2
fi

#[ "`pgrep -f imdb.sh | wc -w`" -ge "2" ] && echo "ALREADY RUNNING" && exit 2
[ -z "$1" ] && echo "Usage: $0 /path/to/movie_file_name.mkv [outdir=info_image_dir] [lang=en] [source=imdb]" && exit 1
outdir1=`dirname "$1"`
filename=`basename "$1"`
[ -f "/mnt/user/cfg/lang" ] && lang="&lang=`cat /mnt/user/cfg/lang`"
[ -f "/mnt/user/cfg/movieinfo_provider" ] && provider="&source=`cat /mnt/user/cfg/movieinfo_provider`"

#Variables (taken from http://playon.unixstorm.org/imdb.php):
#- lang: 'de', 'es', 'fr', 'it', 'pl'
#- source: 'screenrush', 'filmstarts', 'sensacine', 'beyazperde', 'allocine', 'tmdb'
#          (by default IMDB is being used, but currently forced to screenrush because of problems with IMDB API)

#English: screenrush.co.uk
#French:  allocine.fr
#German:  filmstarts.de
#Spanish: sensacine.com
#Turkish: beyazperde.com

# command line
argc=0
for argv in "$@"
do
    [ "${argv#outdir=}"   != "$argv" ] && outdir="${argv#outdir=}"
    [ "${argv#lang=}"     != "$argv" ] && lang="&lang=${argv#lang=}"
    [ "${argv#provider=}" != "$argv" ] && provider="&source=${argv#provider=}"
    argc=$(($argc+1))
done

# TODO: force screenrush instead of IMDB if nothing else was choosen (workaround for IMDB problems)
[ -z "$provider" ] && provider="&source=screenrush"

[ -n "$outdir1" -a -n "$outdir" -a "${outdir:0:1}" != "/" ] && outdir="${outdir1}/${outdir}"
[ -z "$outdir" ] && outdir="$outdir1"

line=`echo "$filename" | \
	sed -e 's/\[[^]]*\]/+/g' \
	    -e 's/([^)]*)/+/g' \
	    -e 's/www[\.!][a-z0-9\.!]*[_+-\ ]/+/gI' \
	    -e 's/[bt][dr]rip/+/gI' \
	    -e 's/cd[12]/+/gI' \
	    -e 's/dvb/+/gI' \
	    -e 's/tvrip/+/gI' \
	    -e 's/hdtv/+/gI' \
	    -e 's/bluray/+/gI' \
	    -e 's/dvd/+/gI' \
	    -e 's/dualaudio/+/gI' \
	    -e 's/retail/+/gI' \
	    -e 's/unrated/+/gI' \
	    -e 's/divx/+/gI' \
	    -e 's/xvid/+/gI' \
	    -e 's/\([+-]\)rip\([^p]\)/\1\2/gI' \
	    -e 's/dd[457][\.]*[1]*/+/gI' \
	    -e 's/x26[34]/+/gI' \
	    -e 's/\./+/g' \
	    -e 's/ /+/g' \
	    -e 's/_/+/g' \
	    -e 's/[+-]scr[+-]/+/gI' \
	    -e 's/\([+-]\)[ry]*\([12][09][0-9][0-9]\)[ry]*/\1\2/gI' \
	    -e 's/\([+-]\)multi\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)NoComp/\1/g' \
	    -e 's/\([+-]\)refined/\1/gI' \
	    -e 's/^[a-z]*the+/+/gI' \
	    -e 's/le[ck]tor/+/gI' \
	    -e 's/\([+-]\)dub*\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)dub*[a-z][a-z]\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)[a-z][a-z]dub*\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)dubbing\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)cut\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)dd\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)5+1\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)r5\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)3d\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)ac3\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)dts\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)sbs\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)[0-9]*p2p\([+-]\)/\1\2/gI' \
	    -e 's/[m]*108[0]*p/+/gI' \
	    -e 's/[m]*7[0-2]*p/+/gI' \
	    -e 's/[m]*48[0]*p/+/gI' \
	    -e 's/\([a-z]\)+I/\1I/g' \
	    -e 's/\([a-z]\)\([A-Z]\)/\1+\2/g' \
	    -e 's/\([+-]\)\([io]n\)\([+-]\)/\1XY\2XY\3/gI' \
	    -e 's/\([+-]\)\([dt]o\)\([+-]\)/\1XY\2XY\3/gI' \
	    -e 's/\([+-]\)[a-uw-z][a-uw-z]\([+-]\)/\1\2/gI' \
	    -e 's/\([+-]\)XY\([io]n\)XY\([+-]\)/\1\2\3/gI' \
	    -e 's/\([+-]\)side[+-]*side/\1/gI' \
	    -e 's/\+[am][vkp][iv34]$//gI' \
	    -e 's/\([+-]\)m2ts/\1/gI' \
	    -e 's/\([+-]\)ts$/\1/gI' \
	    -e 's/\([+-]\)ps3/\1/gI' \
	    -e 's/\([+-]\)XY\(..\)XY/\1\2/g' \
	    -e 's/+*+/+/g' \
	    -e 's/[+]*-/-/g' \
	    -e 's/[-]*-/-/g' \
	    -e 's/[+]*-[+]*/-/g' \
	    -e 's/^[+-]*//g' \
	    -e 's/[+-]*$//g' 2>&1`
#	    #-e 's/19[2-9][0-9]/+/g' \
#	    #-e 's/20[0-1][0-9]/+/g' \

#echo "line:$line filename:$filename outdir:$outdir"

first="${line%%-*}"
without_first="${line#*-}"
second="${without_first%%-*}"
without_first_second="${without_first#*-}"
third="${without_first_second%%-*}"
last="${line##*-}"
#echo -e "Filename: $filename\nParsed:   $line"
#echo "FIRST: $first SECOND: $second THIRD: $third LAST: $last"
try1="$line"
try1a="${line%-*}"
try2="${line%+*}"
try3="$first"
try4="$second"
try5="${first%+*}"
try6="${second%+*}"
try7="$third"
try8="${third%+*}"
try9="$last"
try10="${last%+*}"
try="01$try1"
[ "${#try4}" -gt "4" -a "$try4" != "$try1" -a "$try4" != "$try3" -a "$((${#try3}-${#try4}))" -lt "6" ] && try="$try 04$try4" && try4_used=1 # try second arg if it's -gt than 4 and smaller than first by max 5 chars
[ "${#try1a}" -gt "4" -a "$try1a" != "$try1" ] && try="$try 1a$try1a" && try1a_used=1
[ "${#try2}" -gt "4" -a "$try2" != "$try1" -a "$try2" != "$try5" ] && try="$try 02$try2" && try2_used=1
[ "${#try3}" -gt "3" -a "$try3" != "$try1" -a "$try3" != "$try2" -a "$try3" != "$try1a" ] && try="$try 03$try3" && try3_used=1
[ "${#try4}" -gt "3" -a "$try4" != "$try1" -a "$try4" != "$try3" -a -z "$try4_used" ] && try="$try 4x$try4" && try4_used=1
[ "${#try6}" -gt "4" -a "$try6" != "$try2" -a "$try6" != "$try4" -a "$try6" != "$try5" -a "$((${#try6}-${#try5}))" -lt "4" ] && try="$try 06$try6" && try6_used=1 # try cut second arg if it's -gt than 4 and smaller than first by max 3 chars
[ "${#try5}" -gt "3" -a "$try5" != "$try3" -a "$try5" != "$try2" ] && try="$try 5x$try5"
[ "${#try6}" -gt "3" -a "$try6" != "$try4" -a "$try6" != "$try2" -a -z "$try6_used" ] && try="$try 6x$try6"
[ "${#try7}" -gt "4" -a "$try7" != "$try1" -a "$try7" != "$try4" ] && try="$try 7x$try7"
[ "${#try8}" -gt "3" -a "$try8" != "$try7" -a "$try8" != "$try2" -a "$try8" != "$try6" ] && try="$try 08$try8"
[ "${#try9}" -gt "3" -a "$try9" != "$try1" -a "$try9" != "$try7" ] && try="$try 09$try9"
[ "${#try10}" -gt "3" -a "$try10" != "$try2" -a "$try10" != "$try8" ] && try="$try 10$try10"
[ -z "$try2_used" ] && try="$try 2y$try2"
[ -z "$try3_used" -a "$try3" != "$try1" -a "${#try3}" -lt "4" ] && try="$try 3y$try3"
[ -z "$try4_used" -a "$try4" != "$try3" -a "${#try4}" -lt "4" ] && try="$try 4y$try4"
echo "TRY: $try"
count=1
#exit 0
rm -f "${filename}.jpg"
[ -n "${outdir}" ] && mkdir -p "${outdir}" || outdir=.
for name in ${try//-/+}
do
    name="${name:2}"
    #url="http://playon.unixstorm.org/IMDB/movie.php?mode=sheet&backdrop=yes${lang}&name=${name}"
    #url="http://playon.unixstorm.org/IMDB/movie.php?mode=sheet&backdrop=y&box=dvd&font=tahoma&genres=y&post=y&tagline=y&time=hours${lang}&name=${name}"
    url="http://playon.unixstorm.org/IMDB/movie_beta.php?source=screenrush&mode=sheet&backdrop=y&box=dvd&font=tahoma&genres=y&post=y&tagline=y&time=hours${lang}${provider}&name=${name}"
    #echo "URL: $url"
    wget -q "$url" -O "${outdir}/${filename}.jpg"
    size=`stat -c '%s' "${outdir}/${filename}.jpg" 2>/dev/null || echo 0`
    [ "$size" -gt "50000" ] && echo "Succeed: filename: \"$filename\" name: \"$name\" trycount: $count outimage: \"${outdir}/${filename}.jpg\"" && break
    rm -f "${outdir}/${filename}.jpg"
    count="$((${count}+1))"
done

rmdir "$LOCKDIR"
