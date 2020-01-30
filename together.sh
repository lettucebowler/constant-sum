#!/usr/bin/env #!/usr/bin/env bash
for i in {2..128..2}
do
  cat $i-* >> $i
done
