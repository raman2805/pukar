#!/bin/bash

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <input_file> <output_file>"
  exit
fi
cat $1 |
awk -F, 'BEGIN{
  header="range,district,station,type,in_charge,contact"
  print header
}
/RANGE/{range=$2}
(!/RANGE/ && $3 != ""){
  printf("%s", range);
  for (i = 3; i <= NF; i++) {
    printf(",%s",$i)
  }
  print ""
}' |
sed -e 's/RANGE//g' -e 's/,[ ]*/,/g' -e 's/[ ]*,/,/g' > $2
